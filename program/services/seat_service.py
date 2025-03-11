from sqlalchemy.orm import Session
from models import Seat


class SeatService:
    def __init__(self, session: Session):
        self.session = session

    def create_seat(self, screen_id: int, row_number: int, seat_number: int, seat_class: str) -> Seat:
        """Creates a new seat."""
        seat = Seat(screen_id=screen_id, row_number=row_number, seat_number=seat_number, seat_class=seat_class)
        self.session.add(seat)
        self.session.commit()
        return seat

    def delete_seat(self, seat_id: int) -> bool:
        """Deletes a seat by its ID."""
        seat = self.session.query(Seat).filter_by(seat_id=seat_id).first()
        if seat:
            self.session.delete(seat)
            self.session.commit()
            return True
        return False

    def get_seat_by_id(self, seat_id: int) -> Seat:
        """Retrieves a seat by its ID."""
        seat = self.session.query(Seat).filter_by(seat_id=seat_id).first()
        return seat

    def get_all_seats_by_screen(self, screen_id: int) -> list[Seat]:
        """Retrieves all seats for a specific screen."""
        seats = self.session.query(Seat).filter_by(screen_id=screen_id).all()
        return seats
    
    def update_seat(self, seat_id: int, screen_id: int = None, row_number: int = None, seat_number: int = None, seat_class: str = None) -> Seat:
        """Updates a seat by its ID."""
        seat = self.session.query(Seat).filter_by(seat_id=seat_id).first()
        if seat:
            if screen_id is not None:
                seat.screen_id = screen_id
            if row_number is not None:
                seat.row_number = row_number
            if seat_number is not None:
                seat.seat_number = seat_number
            if seat_class is not None:
                seat.seat_class = seat_class
            self.session.commit()
            return seat
        return None
    
    def update_seat_availability(self, seat_id: int, is_available: bool) -> Seat:
        """Updates a seat's availability."""
        seat = self.session.query(Seat).filter_by(seat_id=seat_id).first()
        if seat:
            seat.is_available = is_available
            self.session.commit()
            return seat
        return None
