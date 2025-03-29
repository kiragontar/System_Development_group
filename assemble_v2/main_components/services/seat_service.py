import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Seat, SeatAvailability


class SeatService:
    def __init__(self, session: Session):
        self.session = session

    def create_seat(self, screen_id: str, cinema_id: int, seat_type : str) -> Seat:
        """Creates a new seat."""
        seat = Seat(screen_id=screen_id, cinema_id=cinema_id, seat_type=seat_type)
        self.session.add(seat)
        self.session.commit()
        return seat

    def delete_seat(self, seat_id: int, cinema_id : int) -> bool:
        """Deletes a seat by its ID."""
        seat = self.session.query(Seat).filter_by(seat_id=seat_id, cinema_id=cinema_id).first()
        if seat:
            self.session.delete(seat)
            self.session.commit()
            return True
        return False

    def get_seat_by_id(self, seat_id: str) -> Seat:
        """Retrieves a seat by its ID."""
        seat = self.session.query(Seat).filter_by(seat_id=seat_id).first()
        return seat

    def get_all_seats_by_screen(self, screen_id: str, cinema_id : int) -> list[Seat]:
        """Retrieves all seats for a specific screen."""
        seats = self.session.query(Seat).filter_by(screen_id=screen_id, cinema_id=cinema_id).all()
        return seats
    
    def update_seat(self, seat_id: str, screen_id: str = None, cinema_id: int = None, seat_type: str = None) -> Seat:
        """Updates a seat by its ID."""
        seat = self.session.query(Seat).filter_by(seat_id=seat_id).first()
        if seat:
            if screen_id is not None:
                seat.screen_id = screen_id
            if cinema_id is not None:
                seat.cinema_id = cinema_id
            if seat_type is not None:
                seat.seat_type = seat_type
            self.session.commit()
            return seat
        return None
    
    def check_seat_availability(self, screening_id : int, seat_id: str) -> bool:
        """Checks if a seat is available."""
        availability = self.session.query(SeatAvailability).filter_by(
            screening_id=screening_id,
            seat_id=seat_id,
            seat_availability=1
        ).first()

        return availability is not None
    
    def update_seat_availability(self, screening_id : int,  seat_id: str, seat_availability: int) -> SeatAvailability:
        """Updates a seat's availability."""
        availability = self.session.query(SeatAvailability).filter_by(
            screening_id=screening_id,
            seat_id=seat_id,
        ).first()
        if availability:
            availability.seat_availability = seat_availability
            self.session.commit()
            return availability
        return None
