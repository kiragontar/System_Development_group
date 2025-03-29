from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import Base

class SeatAvailability(Base):
    """
    Represents the availability of a seat in a screening.
    """
    __tablename__ = 'seat_availability'
    
    screening_id = Column(Integer, ForeignKey('screenings.screening_id'), primary_key=True)
    seat_id = Column(String(255), ForeignKey('seats.seat_id'), primary_key=True)
    booking_id = Column(String(255), ForeignKey('bookings.booking_id'), nullable=True)
    seat_availability = Column(Integer, nullable=False)

    # Relationships
    screening = relationship('Screening', back_populates='seat_availability')
    seat = relationship('Seat', back_populates='seat_availability')
    booking = relationship('Booking', back_populates='seat_availability')

    def __init__ (self, screening_id: int, seat_id: str, booking_id: str, seat_availability: int = 1):
        """
        Initializes a new SeatAvailability object with the provided attributes.
        """
        self.screening_id = screening_id
        self.seat_id = seat_id
        self.booking_id = booking_id
        self.seat_availability = seat_availability

    def get_screening_id(self) -> int:
        return self.screening_id
    def get_seat_id(self) -> str:
        return self.seat_id
    def get_booking_id(self) -> str:
        return self.booking_id
    def get_seat_availability(self) -> int:
        return self.seat_availability
    def set_screening_id(self, screening_id: int) -> None:
        if screening_id > 0:
            self.screening_id = screening_id
        else:
            raise ValueError("Screening ID must be a positive integer.")
    def set_seat_id(self, seat_id: str) -> None:
        if seat_id:
            self.seat_id = seat_id
        else:
            raise ValueError("Seat ID cannot be empty.")
    def set_booking_id(self, booking_id: str) -> None:
        if booking_id:
            self.booking_id = booking_id
        else:
            raise ValueError("Booking ID cannot be empty.")
    def set_seat_availability(self, seat_availability: int) -> None:
        if seat_availability:
            self.seat_availability = seat_availability
        else:
            raise ValueError("Seat availability cannot be empty.")
    
    def __repr__(self) -> str:
        return f"<SeatAvailability(screening_id={self.screening_id}, seat_id={self.seat_id}, booking_id={self.booking_id}, seat_availability={self.seat_availability})>"