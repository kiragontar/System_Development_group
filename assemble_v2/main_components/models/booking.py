from sqlalchemy import Column, String, ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from .import Base


class Booking(Base):
    """Represents a ticket booking for a specific screening."""

    __tablename__ = 'bookings'

    booking_id = Column(String(225), nullable=False)
    seat_id = Column(String(255), ForeignKey('seats.seat_id', ondelete='CASCADE'), nullable=False)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=True)
    customer_phone = Column(String(255), nullable=True)

    # Relationship to Screening
    seat = relationship('Seat', back_populates='bookings')
    seat_availability = relationship('SeatAvailability', back_populates='booking')
    tickets = relationship('Ticket', back_populates='booking', cascade="all, delete-orphan")

    __table_args__ = (
        PrimaryKeyConstraint('booking_id', 'seat_id'), #Composite primary key.
    )

    def __init__(self, booking_id: str, seat_id : str, customer_name:str, customer_email:str = None, customer_phone:str = None):
        self.booking_id = booking_id
        self.seat_id = seat_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone

    def get_booking_id(self) -> str:
        return self.booking_id
    
    def get_seat_id(self) -> str:
        return self.seat_id
    
    def get_customer_name(self) -> str:
        return self.customer_name

    def get_customer_email(self) -> str:
        return self.customer_email

    def get_customer_phone(self) -> str:
        return self.customer_phone

    def set_booking_id(self, booking_id: str) -> None:
        if booking_id:
            self.booking_id = booking_id
        else:
            raise ValueError("Booking ID cannot be empty.")
    def set_seat_id(self, seat_id: str) -> None:
        if seat_id:
            self.seat_id = seat_id
        else:
            raise ValueError("Seat ID cannot be empty.")
    def set_customer_name(self, customer_name: str) -> None:
        if customer_name:
            self.customer_name = customer_name
        else:
            raise ValueError("Customer name cannot be empty")

    def set_customer_email(self, customer_email: str) -> None:
        self.customer_email = customer_email

    def set_customer_phone(self, customer_phone: str) -> None:
        self.customer_phone = customer_phone

   