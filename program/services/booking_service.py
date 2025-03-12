from sqlalchemy.orm import Session
from models import Booking, Screening
from enums import PaymentStatus
import uuid
from datetime import datetime, timedelta
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
    def __init__(self, session: Session):
        self.session = session

    def create_booking(self, screening_id: int, price: float, seats: list, customer_name:str, customer_email:str = None, customer_phone:str = None) -> Booking:
        """Creates a new booking."""
        screening = self.session.query(Screening).filter_by(screening_id=screening_id).first()
        if not screening:
            raise InvalidScreeningError("Screening not found")
        if not seats:
            raise NoSeatsSelectedError("No seats selected")

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
        if not booking:
            raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")
        return booking

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancels a booking by its ID."""
        booking = self.session.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")
        booking.cancel()
        self.session.commit()
        logging.info(f"Booking {booking_id} cancelled.")
        
    def place_booking(self, booking_id: str, timeout_minutes: int = 30) -> bool:
        """Checks timeout for pending bookings and handles FAILED status."""
        booking = self.session.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")

        if booking.payment_status == PaymentStatus.PENDING:
            if (datetime.now() - booking.booking_time) < timedelta(minutes=timeout_minutes):
                logging.info(f"Booking {booking_id} within timeout, pending.")
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
