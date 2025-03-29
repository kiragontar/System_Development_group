import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Booking, Screening, Ticket, Seat, Cinema, City, SeatAvailability
from main_components.enums import PaymentStatus
import uuid
from datetime import datetime, timedelta
from main_components.services.ticket_service import TicketService
import logging 
from typing import List

logging.basicConfig(level=logging.INFO)

class BookingNotFoundError(Exception):
    pass

class BookingTimeoutError(Exception):
    pass


class BookingService:
    def __init__(self, session: Session, ticket_service: TicketService):
        self.session = session
        self.ticket_service = ticket_service

    def create_booking(self, seat_ids : List[str], customer_name:str, customer_email:str = None, customer_phone:str = None, screening_id : int = None) -> Booking:
        """Creates a new booking."""
        bookings = []
        try:
            booking_id = str(uuid.uuid4())

            # Bookings can only be booked up to one week in advance of a screening.
            # Validate screening date.
            screening = self.session.query(Screening).filter_by(screening_id=screening_id).first()
            if not screening:
                raise ValueError(f"Screening with ID {screening_id} not found.")
            one_week_ahead = datetime.now().date() + timedelta(days=7) # Get date one week ahead.
            if screening.date > one_week_ahead: # Meaning screening date is more than one week ahead.
                raise ValueError("Bookings can only be made up to one week in advance.")
            
            for seat_id in seat_ids:
                # Check if seat is available
                seat_availability = self.session.query(SeatAvailability).filter_by(seat_id=seat_id, screening_id=screening_id).first()
                if not seat_availability or seat_availability.seat_availability == 0:
                    raise ValueError(f"Seat with ID {seat_id} is not available for screening {screening_id}.")

                # Check for duplicate seat_id for the same booking_id
                existing_booking = self.session.query(Booking).filter_by(booking_id=booking_id, seat_id=seat_id).first()
                if existing_booking:
                    raise ValueError(f"Seat {seat_id} already booked for booking {booking_id}")
            
                booking = Booking(booking_id=booking_id, seat_id=seat_id, customer_name=customer_name, customer_email=customer_email, customer_phone=customer_phone)
                self.session.add(booking)
                bookings.append(booking)

            # Second loop: Update seat availability after all seats are checked.
            for seat_id in seat_ids:
                seat_availability = self.session.query(SeatAvailability).filter_by(seat_id=seat_id,screening_id=screening_id).first()
                seat_availability.seat_availability = 0

            self.session.commit()  # Commit after updating availability.


            # Get cinema from seatid (using the first seat_id).
            if seat_ids:
                seat = self.session.query(Seat).filter_by(seat_id=seat_ids[0]).first()
                if seat:
                    seat_type = seat.seat_type
                    cinema_id = seat.cinema_id
                    cinema = self.session.query(Cinema).filter_by(cinema_id=cinema_id).first()
                    if cinema:
                        city = self.session.query(City).filter_by(city_id=cinema.city_id).first()
                        if city:
                            if datetime.now().hour < 12:
                                ticket_price = city.price_morning
                            elif datetime.now().hour < 18:
                                ticket_price = city.price_afternoon
                            else:
                                ticket_price = city.price_evening

                        if seat_type == 'Upper':
                            ticket_price = ticket_price * 1.2
                        elif seat_type == 'VIP':
                            ticket_price = (ticket_price * 1.2) * 1.2
                        # Create ticket for all seats from booking.
                        for seat_id in seat_ids:
                            ticket = Ticket(booking_id=booking_id, seat_id=seat_id, ticket_price=ticket_price, payment_status= PaymentStatus.PAID)
                            self.session.add(ticket)
                        self.session.commit()
            return bookings
        except Exception as e:
            self.session.rollback()
            logging.error(f"Failed to create booking: {e}")
            print(f"Unexpected error occured : {e}")
            return None
        

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
    
    def get_bookings_by_customer(self, customer_name: str) -> list[Booking]:
        """Retrieves all bookings for a customer."""
        bookings = self.session.query(Booking).filter_by(customer_name=customer_name).all()
        return bookings
    
    def get_bookings_by_screening(self, screening_id: int) -> list[Booking]:
        """Retrieves all bookings for a screening."""
        bookings = self.session.query(Booking).join(SeatAvailability).filter(SeatAvailability.screening_id == screening_id).all()
        return bookings

    def update_booking(self, booking_id: str, customer_name: str = None, customer_email: str = None, customer_phone: str = None) -> Booking:
        """Updates a booking's details."""
        try:
            booking = self.session.query(Booking).filter_by(booking_id=booking_id).first()
            if not booking:
                raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")
            if customer_name:
                booking.customer_name = customer_name
            if customer_email:
                booking.customer_email = customer_email
            if customer_phone:
                booking.customer_phone = customer_phone
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logging.error(f"Failed to update booking {booking_id}: {e}")
        return booking

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancels a booking by its ID."""
        bookings = self.session.query(Booking).filter_by(booking_id=booking_id).all()
        if not booking:
            raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")
        try:
            # Get seat_id from the first booking
            seat_id = bookings[0].seat_id
            # Get screening id from seat id and booking id from seat_availability table.
            seat_availability = self.session.query(SeatAvailability).filter_by(booking_id=booking_id, seat_id=seat_id).first()
            if not seat_availability:
                logging.error(f"SeatAvailability not found for booking {booking_id} and seat {seat_id}")
                return False
            screening_id = seat_availability.screening_id
            # Get screening from screening id
            screening = self.session.query(Screening).filter_by(screening_id=screening_id).first()
            if screening:
                # collect date and start time of screening:
                date = screening.date
                start_time = screening.start_time
                # collect date and time currently
                current_date = datetime.now().date()
                current_time = datetime.now().time()
                # Current date and time should be less than screening date and time to cancel booking.
                if current_date < date or (current_date == date and current_time < start_time):
                    # Get all tickets for this booking once.
                    tickets = self.ticket_service.get_tickets_by_booking(booking_id=booking_id)
                    # Get ticket ids from tickets
                    ticket_ids = [ticket.ticket_id for ticket in tickets]
                    # Update payment status of tickets to refunded
                    self.ticket_service.update_payment_status(ticket_ids, PaymentStatus.REFUNDED)
                    for booking in bookings:
                        # Delete booking
                        self.session.delete(booking)
                    self.session.commit()
                    logging.info(f"Booking {booking_id} cancelled successfully.")
                    return True
                else:
                    logging.warning(f"Booking {booking_id} cannot be cancelled as the screening has already started.")
                    return False
        except Exception as e:
            self.session.rollback()
            logging.error(f"Failed to cancel booking {booking_id}: {e}")
            return False

        
    