from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from . import Base
from .booking import Booking
from enums import PaymentStatus
from datetime import datetime
from sqlalchemy.types import Enum

class Payment(Base):
    """Represents a payment transaction."""
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(String(255), ForeignKey('bookings.booking_id'), nullable=False)
    payment_method = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    transaction_id = Column(String(255), nullable=True)
    payment_status = Column(Enum(PaymentStatus), nullable=False)

    booking = relationship('Booking', back_populates='payments')

    def __init__(self, booking_id: str, payment_method: str, amount: float, transaction_id: str = None):
        self.booking_id = booking_id
        self.payment_method = payment_method
        self.amount = amount
        self.payment_date = datetime.now()
        self.transaction_id = transaction_id
        self.payment_status = PaymentStatus.PENDING # Initialized to pending

    def get_payment_id(self) -> int:
        return self.payment_id

    def get_booking(self) -> 'Booking':
        return self.booking

    def get_payment_method(self) -> str:
        return self.payment_method

    def get_amount(self) -> float:
        return self.amount

    def get_payment_date(self) -> datetime:
        return self.payment_date

    def get_transaction_id(self) -> str:
        return self.transaction_id

    def get_payment_status(self) -> PaymentStatus:
        return self.payment_status

    def set_transaction_id(self, transaction_id: str) -> None:
        self.transaction_id = transaction_id

    def set_payment_status(self, payment_status: PaymentStatus) -> None:
        self.payment_status = payment_status

    def __repr__(self) -> str:
        return f"<Payment(payment_id={self.payment_id}, booking_id='{self.booking_id}', amount={self.amount}, payment_method='{self.payment_method}', payment_status='{self.payment_status}')>"
