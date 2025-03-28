from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from . import Base
from .screening import Screening
from .booking import Booking
from .seat import Seat
from datetime import datetime


class Ticket(Base):
    """Represents a ticket for a screening."""
    __tablename__ = 'tickets'

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(String(255), ForeignKey('bookings.booking_id'), nullable=False)
    seat_id = Column(Integer, ForeignKey('seats.seat_id'), nullable=False)
    screening_id = Column(Integer, ForeignKey('screenings.screening_id'), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    qr_code = Column(String(255), nullable=True)
    original_ticket_price = Column(Float, nullable=False)

    booking = relationship('Booking', back_populates='tickets')
    seat = relationship('Seat', back_populates='tickets')
    screening = relationship('Screening', back_populates='tickets')

    def __init__(self, booking_id: str, seat_id: int, screening_id: int, original_ticket_price: float, qr_code: str = None):
        self.booking_id = booking_id
        self.seat_id = seat_id
        self.screening_id = screening_id
        self.issue_date = datetime.now()
        self.qr_code = qr_code
        self.original_ticket_price = original_ticket_price

    def get_ticket_id(self) -> int:
        return self.ticket_id

    def get_booking(self) -> 'Booking':
        return self.booking

    def get_seat(self) -> 'Seat':
        return self.seat

    def get_screening(self) -> 'Screening':
        return self.screening

    def get_issue_date(self) -> datetime:
        return self.issue_date
    
    def get_original_ticket_price(self) -> float:
        """Gets the original ticket price."""
        return self.original_ticket_price

    def get_qr_code(self) -> str:
        return self.qr_code

    def set_issue_date(self, issue_date: datetime) -> None:
        if not isinstance(issue_date, datetime):
            raise ValueError("issue_date must be a datetime object.")
        self.issue_date = issue_date

    def set_qr_code(self, qr_code: str) -> None:
        self.qr_code = qr_code
    
    def set_original_ticket_price(self, price: float) -> None:
        """Sets the original ticket price."""
        if price < 0:
            raise ValueError("Ticket price cannot be negative.")
        self.original_ticket_price = price

    def __repr__(self) -> str:
        return f"<Ticket(ticket_id={self.ticket_id}, booking_id='{self.booking_id}', seat_id={self.seat_id}, screening_id='{self.screening_id}')>"
