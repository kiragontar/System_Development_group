from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from .import Base, booking_seat_association
from .screening import Screening
from .seat import Seat
from main_components.enums import PaymentStatus
from typing import List
from datetime import datetime
from sqlalchemy.types import Enum
import uuid

class Booking(Base):
    """Represents a ticket booking for a specific screening."""

    __tablename__ = 'bookings'

    booking_id = Column(String(225), unique=True, primary_key=True)
    screening_id = Column(Integer, ForeignKey('screenings.screening_id'), nullable=False)
    booking_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=True, unique=True)
    customer_phone = Column(String(255), nullable=True, unique=True)

    # Relationship to Screening
    screening = relationship('Screening', back_populates='bookings')
    seats = relationship('Seat', secondary=booking_seat_association, back_populates='bookings') 
    payments = relationship('Payment', back_populates='booking')
    tickets = relationship('Ticket', back_populates='booking')

    def __init__(self, screening_id: int, price: float, seats: list, customer_name:str, customer_email:str = None, customer_phone:str = None):
        self.booking_id = str(uuid.uuid4()) # Generate UUID here
        self.screening_id = screening_id
        self.booking_time = datetime.now()
        self.price = price
        self.payment_status = PaymentStatus.PENDING
        self.seats = seats
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone

    def get_booking_id(self) -> str:
        return self.booking_id

    def get_screening(self) -> 'Screening':
        return self.screening

    def get_booking_time(self) -> datetime:
        return self.booking_time

    def get_price(self) -> float:
        return self.price

    def get_payment_status(self) -> PaymentStatus:
        return self.payment_status

    def get_customer_name(self) -> str:
        return self.customer_name

    def get_customer_email(self) -> str:
        return self.customer_email

    def get_customer_phone(self) -> str:
        return self.customer_phone

    def get_seats(self) -> List['Seat']:
        return self.seats

    def set_screening(self, screening: 'Screening') -> None:
        if screening:
            self.screening = screening
        else:
            raise ValueError("Screening cannot be None")

    def set_booking_time(self, booking_time : datetime) -> None:
        if not isinstance(booking_time, datetime):
            raise ValueError("booking_time must be a datetime object.")
        self.booking_time = booking_time

    def set_price(self, price: float) -> None:
        if price >= 0:
            self.price = price
        else:
            raise ValueError("Price cannot be negative")

    def set_payment_status(self, payment_status: PaymentStatus) -> None:
        self.payment_status = payment_status

    def set_customer_name(self, customer_name: str) -> None:
        if customer_name:
            self.customer_name = customer_name
        else:
            raise ValueError("Customer name cannot be empty")

    def set_customer_email(self, customer_email: str) -> None:
        self.customer_email = customer_email

    def set_customer_phone(self, customer_phone: str) -> None:
        self.customer_phone = customer_phone

    def set_seats(self, seats: List['Seat']) -> None:
        if seats:
            self.seats = seats
        else:
            raise ValueError("Seats cannot be empty")

    