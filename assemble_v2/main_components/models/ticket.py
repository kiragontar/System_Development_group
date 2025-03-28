from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from . import Base
from .screening import Screening
from .booking import Booking
from .seat import Seat
from main_components.enums import PaymentStatus
from datetime import datetime

class Ticket(Base):
    """Represents a ticket for a screening."""
    __tablename__ = 'tickets'

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(String(255), ForeignKey('bookings.booking_id'), nullable=False)
    seat_id = Column(String(255), ForeignKey('seats.seat_id'), nullable=False)
    ticket_price = Column(Float, nullable=False)
    qr_code = Column(String(255), nullable=True)
    issue_date = Column(DateTime, nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    

    booking = relationship('Booking', back_populates='tickets')
    seat = relationship('Seat', back_populates='tickets')


    def __init__(self, booking_id: str, seat_id: str, ticket_price : float, qr_code: str = None,  payment_status: PaymentStatus = PaymentStatus.PENDING):
        self.booking_id = booking_id
        self.seat_id = seat_id
        self.ticket_price = ticket_price
        self.qr_code = qr_code
        self.issue_date = datetime.now()
        self.payment_status = payment_status

    def get_ticket_id(self) -> int:
        return self.ticket_id

    def get_booking_id(self) -> str:
        return self.booking_id

    def get_seat_id(self) -> str:
        return self.seat_id

    def get_ticket_price(self) -> float:
        return self.ticket_price

    def get_qr_code(self) -> str:
        return self.qr_code

    def get_issue_date(self) -> datetime:
        return self.issue_date
    
    def get_payment_status(self) -> PaymentStatus:
        return self.payment_status
    
    def set_ticket_id(self, ticket_id: int) -> None:
        if ticket_id > 0:
            self.ticket_id = ticket_id
        else:
            raise ValueError("Ticket ID must be a positive integer.")
    
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
    def set_ticket_price(self, ticket_price: float) -> None:
        if ticket_price < 0:
            raise ValueError("Ticket price cannot be negative.")
    
    def set_qr_code(self, qr_code: str) -> None:
        self.qr_code = qr_code

    def set_issue_date(self, issue_date: datetime) -> None:
        if not isinstance(issue_date, datetime):
            raise ValueError("issue_date must be a datetime object.")
        self.issue_date = issue_date

    def set_payment_status(self, payment_status: PaymentStatus) -> None:
        if not isinstance(payment_status, PaymentStatus):
          raise ValueError("payment_status must be a PaymentStatus enum object.")
        self.payment_status = payment_status



    def __repr__(self) -> str:
        return f"<Ticket(ticket_id={self.ticket_id}, booking_id='{self.booking_id}', seat_id={self.seat_id}, ticket_price={self.ticket_price}, qr_code='{self.qr_code}', issue_date={self.issue_date}, payment_status={self.payment_status})>"
