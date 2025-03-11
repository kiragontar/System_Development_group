from sqlalchemy.orm import Session
from models import Booking, PaymentStatus
import uuid
from datetime import datetime, timedelta


class BookingService:
    def __init__(self, session: Session):
        self.session = session

    def create_booking(self, screening_id: str, price: float, seats: list, customer_name:str, customer_email:str = None, customer_phone:str = None) -> Booking:
        """Creates a new booking."""
        booking_id = str(uuid.uuid4())
        booking = Booking(screening_id=screening_id, price=price, seats=seats, customer_name=customer_name, customer_email=customer_email, customer_phone=customer_phone)
        booking.booking_id = booking_id
        self.session.add(booking)
        self.session.commit()
        return booking

    def get_all_bookings(self) -> list[Booking]:
        """Retrieves all bookings."""
        bookings = self.session.query(Booking).all()
        return bookings

    def get_booking_by_id(self, booking_id: str) -> Booking:
        """Retrieves a booking by its ID."""
        booking = self.session.query(Booking).filter_by(booking_id=booking_id).first()
        return booking

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancels a booking by its ID."""
        booking = self.session.query(Booking).filter_by(booking_id=booking_id).first()
        if booking: # If you find a booking placed with that id.
            booking.cancel() # cancel it
            self.session.commit()
            return True
        return False

    def place_booking(self, booking_id: str, timeout_minutes: int = 30) -> bool:
        """Checks timeout for pending bookings."""
        booking = self.session.query(Booking).filter_by(booking_id=booking_id).first() # get booking.
        if booking:
            if booking.payment_status == PaymentStatus.PENDING: # Check if payment has yet to be made.
                if (datetime.now() - booking.booking_time) < timedelta(minutes=timeout_minutes): # Calculate how much its been since booking was made, if its less than 30 minutes then place booking.
                    # Payment status will be set by Stripe
                    return True # The payment is still pending, but within the time limit.
                else: # Booking created is too old.
                    print(f"Booking {booking_id} timed out and was cancelled.")
                    booking.cancel()
                    self.session.commit()
                    return False
            elif booking.payment_status == PaymentStatus.PAID: # If paid
                print(f"Booking {booking_id} is already paid.")
                return True
            else:
                print(f"Booking {booking_id} is refunded or in an invalid state.")
                return False
        return False
