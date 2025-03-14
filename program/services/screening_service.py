from sqlalchemy.orm import Session
from models import Screening, Screen
from typing import List, Optional
from datetime import datetime

class ScreeningService:
    """
    Handles operations related to cinema screenings.
    """

    def __init__(self, session: Session):
        """Initializes the ScreeningService with a session."""
        self.session = session

    def create_screening(self, screen_id: str, film_id: str, date: datetime, start_time: datetime, end_time: datetime, lower_hall_sold: int = 0, upper_hall_sold: int = 0, vip_sold: int = 0) -> Screening:
        """Creates a new screening."""
        screening = Screening.create_screening(screen_id, film_id, date, start_time, end_time, lower_hall_sold, upper_hall_sold, vip_sold)
        self.session.add(screening)
        self.session.commit()
        return screening

    def get_screening_by_id(self, screening_id: int) -> Optional[Screening]:
        """Retrieves a screening by ID."""
        return self.session.query(Screening).filter_by(screening_id=screening_id).first()

    def get_all_screenings(self) -> List[Screening]:
        """Retrieves all screenings."""
        return self.session.query(Screening).all()

    def update_screening(self, screening_id: str, screen_id: str = None, film_id: str = None, date: datetime = None, start_time: datetime = None, end_time: datetime = None, lower_hall_sold: int = None, upper_hall_sold: int = None, vip_sold: int = None) -> Optional[Screening]:
        """Updates a screening's details."""
        screening = self.get_screening_by_id(screening_id)
        if screening:
            if screen_id:
                screening.set_screen_id(screen_id)
            if film_id:
                screening.set_film_id(film_id)
            if date:
                screening.set_date(date)
            if start_time:
                screening.set_start_time(start_time)
            if end_time:
                screening.set_end_time(end_time)
            if lower_hall_sold is not None:
                screening.set_lower_hall_sold(lower_hall_sold)
            if upper_hall_sold is not None:
                screening.set_upper_hall_sold(upper_hall_sold)
            if vip_sold is not None:
                screening.set_vip_sold(vip_sold)
            self.session.commit()
            return screening
        return None

    def delete_screening(self, screening_id: str) -> bool:
        """Deletes a screening."""
        screening = self.get_screening_by_id(screening_id)
        if screening:
            self.session.delete(screening)
            self.session.commit()
            return True
        return False
    
    def get_screenings_for_screen(self, screen_id: str) -> List[Screening]:
        """Retrieves all screenings for a given screen."""
        return self.session.query(Screening).filter_by(screen_id=screen_id).all()

    def get_screen_for_screening(self, screening_id: str) -> Optional[Screen]:
        """Retrieves the screen for a given screening."""
        screening = self.get_screening_by_id(screening_id)
        if screening:
            return self.session.query(Screen).filter_by(screen_id=screening.screen_id).first()
        return None