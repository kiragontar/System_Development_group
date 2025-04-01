from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from . import Base



class Seat(Base):
    """Represents a seat in a screen."""
    __tablename__ = 'seats'

    seat_id = Column(String(255), primary_key=True, unique=True)
    screen_id = Column(String(255), ForeignKey('screens.screen_id', ondelete='CASCADE'), nullable=False)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'), nullable=False)
    seat_type = Column(String(255), nullable=False)


    bookings = relationship('Booking', back_populates='seat')
    tickets = relationship('Ticket', back_populates='seat')
    cinema = relationship('Cinema', back_populates='seats')
    seat_availability = relationship('SeatAvailability', back_populates='seat')

    _seat_counters = {}  # Class-level dictionary to store counters

    def __init__(self, screen_id: str, cinema_id: int, seat_type: str):
        self.screen_id = screen_id
        self.cinema_id = cinema_id
        self.seat_type = seat_type

        # Generate the seat_id using the counter
        key = (screen_id, cinema_id)
        if key not in Seat._seat_counters:
            Seat._seat_counters[key] = 1
        else:
            Seat._seat_counters[key] += 1

        self.seat_id = f"{screen_id}_C{cinema_id}_{Seat._seat_counters[key]}"

    def get_seat_id(self) -> str:
        return self.seat_id
    def get_cinema_id(self) -> int:
        return self.cinema_id

    def get_screen_id(self) -> int:
        return self.screen_id

    def get_seat_type(self) -> str:
        return self.seat_type
    
    def set_seat_id(self, seat_id: str) -> None:
        if seat_id:
            self.seat_id = seat_id
        else:
            raise ValueError("Seat ID cannot be empty.")
    
    def set_screen_id(self, screen_id: int) -> None:
        if screen_id > 0:
            self.screen_id = screen_id
        else:
            raise ValueError("Screen ID must be a positive integer.")

    def set_cinema_id(self, cinema_id: int) -> None:
        if cinema_id:
            self.cinema_id = cinema_id
        else:
            raise ValueError("cinema id cannot be empty.")
    def set_seat_type(self, seat_type: str) -> None:
        if seat_type:
            self.seat_type = seat_type
        else:
            raise ValueError("Seat type cannot be empty.")
        
    def __repr__(self) -> str:
        return f"<Seat(seat_id={self.seat_id}, screen_id={self.screen_id}, type='{self.seat_type}')>"
