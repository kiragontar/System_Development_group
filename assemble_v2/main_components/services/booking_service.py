import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Booking, Screening, Ticket, Seat, Screen, Cinema, City
from main_components.enums import PaymentStatus
import uuid
from datetime import datetime, timedelta
from main_components.services.seat_service import SeatService
from main_components.services.pricing_service import PricingService
from main_components.services.ticket_service import TicketService
import logging 

logging.basicConfig(level=logging.INFO)

class BookingNotFoundError(Exception):
    pass

class BookingTimeoutError(Exception):
    pass

class InvalidScreeningError(Exception):
    pass

class NoSeatsSelectedError(Exception):
    pass

class BookingService:
    def __init__(self, session: Session, seat_service: SeatService, ticket_service: TicketService, pricing_service: PricingService):
        self.session = session
        self.seat_service = seat_service
        self.pricing_service = pricing_service
        self.ticket_service = ticket_service

    def create_booking(self, screening_id: int, price: float, seats: list, customer_name:str, customer_email:str = None, customer_phone:str = None) -> Booking:
        """Creates a new booking."""
        screening = self.session.query(Screening).filter_by(screening_id=screening_id).first()
        if not screening:
            raise InvalidScreeningError("Screening not found")
        if not seats:
            raise NoSeatsSelectedError("No seats selected")

        booking_id = str(uuid.uuid4())
        total_price = 0.0
        booking = Booking(screening_id=screening_id, price=price, seats=seats, customer_name=customer_name, customer_email=customer_email, customer_phone=customer_phone)
        booking.booking_id = booking_id
        booking.seats = seats
        self.session.add(booking)
        self.session.flush()

        screen = self.session.query(Screen).filter_by(screen_id=screening.screen_id, cinema_id=screening.cinema_id).first()
        cinema = self.session.query(Cinema).filter_by(cinema_id=screen.cinema_id).first()
        city_obj = self.session.query(City).filter_by(city_id= cinema.city_id).first()
        if city_obj:
            city = city_obj.name
        else:
            city = "DefaultCity"
        for seat in seats:
            # Determine time of day from screening start time
            start_hour = screening.start_time.hour
            if 8 <= start_hour < 12:
                time_of_day = "Morning"
            elif 12 <= start_hour < 17:
                time_of_day = "Afternoon"
            else:
                time_of_day = "Evening"

            # Get price from PricingService
            try: 
                ticket_price = self.pricing_service.get_price(city, seat.seat_class, time_of_day)
                total_price += ticket_price
            except ValueError as e:
                print(f"Error getting price : {e}")
                total_price = -1
                break

            ticket = self.ticket_service.create_ticket(
                booking_id=booking_id,
                seat_id=seat.seat_id,
                screening_id=screening_id,
                original_ticket_price= ticket_price
            )
        if total_price == -1:
            self.session.rollback()
            raise ValueError("Could not get price for one or more seats.")

        booking.price = total_price
        self.session.commit()
        return booking

    def get_all_bookings(self) -> list[Booking]:
        """Retrieves all bookings."""
        bookings = self.session.query(Booking).all()
        return bookings

    def get_booking_by_id(self, booking_id: str) -> Booking:
        """Retrieves a booking by its ID."""
        booking = self.session.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")
        return booking

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancels a booking by its ID."""
        booking = self.session.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")
        try:
            if booking.payment_status == PaymentStatus.PAID:
                booking.payment_status = PaymentStatus.REFUNDED
                tickets = self.ticket_service.get_tickets_by_booking(booking_id=booking_id) #Collect all tickets from booking to update seat availability.
                if tickets:
                    screening = self.session.query(Screening).filter_by(screening_id = booking.screening_id).first() # Get screening for booking.
                    if screening:
                        upper_seats_count = sum(1 for seat in booking.seats if seat.seat_class == 'Upper')
                        lower_seats_count = sum(1 for seat in booking.seats if seat.seat_class == 'Lower')
                        vip_seats_count = sum(1 for seat in booking.seats if seat.seat_class == 'VIP')

                        screening.upper_hall_sold -= upper_seats_count
                        screening.lower_hall_sold -= lower_seats_count
                        screening.vip_sold -= vip_seats_count

                        for ticket in tickets:
                            self.seat_service.update_seat_availability(ticket.seat_id, True)
                        self.session.add(screening)
                self.session.commit()
                logging.info(f"Booking {booking_id} cancelled.")
                return True
            else: # Booking has not been paid:
                booking.payment_status = PaymentStatus.Failed
                self.session.commit()
                logging.info(f"Booking {booking_id} cancelled. Payment failed.")
                return True
        except Exception as e:
            self.session.rollback()
            logging.error(f"Failed to cancel booking {booking_id}: {e}")
            return False

        
    def place_booking(self, booking_id: str, timeout_minutes: int = 30) -> bool:
        """Checks timeout, places booking, updates seat availability, and generates tickets."""
        booking = self.session.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")
        try:
            if booking.payment_status == PaymentStatus.PENDING:
                if (datetime.now() - booking.booking_time) < timedelta(minutes=timeout_minutes): # Booking is within timeout.
                    booking.payment_status = PaymentStatus.PAID
                    tickets = self.ticket_service.get_tickets_by_booking(booking_id=booking_id) # Get all tickets for this booking
                    if tickets:
                        screening = self.session.query(Screening).filter_by(screening_id=booking.screening_id).first() 
                        if screening:
                            self.session.refresh(screening)
                            for ticket in tickets:
                                seat = self.session.query(Seat).filter_by(seat_id=ticket.seat_id).first()
                                if seat:
                                    if seat.seat_class == 'Lower':
                                        screening.lower_hall_sold += 1
                                    elif seat.seat_class == 'Upper':
                                        screening.upper_hall_sold += 1
                                    elif seat.seat_class == 'VIP':
                                        screening.vip_sold += 1
                                    self.seat_service.update_seat_availability(ticket.seat_id, False)
                            self.session.add(screening)
                    self.session.flush() # Added flush
                    self.session.refresh(screening) # Added refresh
                    self.session.commit()
                    logging.info(f"Booking {booking_id} placed successfully.")
                    return True  # Still pending, within timeout
                else:
                    logging.info(f"Booking {booking_id} timed out and was marked as FAILED.")
                    booking.payment_status = PaymentStatus.FAILED # Change to failed instead of cancel
                    self.session.commit()
                    raise BookingTimeoutError(f"Booking {booking_id} timed out.")
            elif booking.payment_status == PaymentStatus.PAID:
                logging.info(f"Booking {booking_id} is already paid.")
                return True
            elif booking.payment_status == PaymentStatus.FAILED:
                logging.warning(f"Booking {booking_id} payment has failed.")
                return False
            else:
                logging.warning(f"Booking {booking_id} is refunded or in an invalid state.")
                return False
        except Exception as e:
            self.session.rollback()
            logging.error(f"Failed to place booking {booking_id}: {e}")
