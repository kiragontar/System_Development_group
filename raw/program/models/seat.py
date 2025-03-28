from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from . import Base, booking_seat_association



class Seat(Base):
    """Represents a seat in a screen."""
    __tablename__ = 'seats'

    seat_id = Column(Integer, primary_key=True, autoincrement=True)
    screen_id = Column(String(255), ForeignKey('screens.screen_id'), nullable=False)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'), nullable=False)
    row_number = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    seat_class = Column(String(255), nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)

    screen = relationship('Screen', back_populates='seats')
    bookings = relationship('Booking', secondary=booking_seat_association, back_populates='seats')
    tickets = relationship('Ticket', back_populates='seat')
    cinema = relationship('Cinema', back_populates='seats')

    def __init__(self, screen_id: int, cinema_id: int, row_number: int, seat_number: int, seat_class: str):
        self.screen_id = screen_id
        self.cinema_id = cinema_id
        self.row_number = row_number
        self.seat_number = seat_number
        self.seat_class = seat_class
        self.is_available = True

    def get_seat_id(self) -> int:
        return self.seat_id

    def get_screen_id(self) -> int:
        return self.screen_id

    def get_row_number(self) -> int:
        return self.row_number

    def get_seat_number(self) -> int:
        return self.seat_number

    def get_seat_class(self) -> str:
        return self.seat_class
    
    def get_is_available(self) -> bool:
        return self.is_available

    def set_screen_id(self, screen_id: int) -> None:
        if screen_id > 0:
            self.screen_id = screen_id
        else:
            raise ValueError("Screen ID must be a positive integer.")

    def set_row_number(self, row_number: int) -> None:
        if row_number > 0:
            self.row_number = row_number
        else:
            raise ValueError("Row number must be a positive integer.")

    def set_seat_number(self, seat_number: int) -> None:
        if seat_number >= 50 and seat_number <=120:
            self.seat_number = seat_number
        else:
            raise ValueError("Seat number must be 50 or above and 120 or below.")

    def set_seat_class(self, seat_class: str) -> None:
        if seat_class:
            self.seat_class = seat_class
        else:
            raise ValueError("Seat class cannot be empty.")
        
    def set_is_available(self, is_available: bool) -> None:
        self.is_available = is_available

    def __repr__(self) -> str:
        return f"<Seat(seat_id={self.seat_id}, screen_id={self.screen_id}, row={self.row_number}, seat={self.seat_number}, class='{self.seat_class}', available={self.is_available})>"
