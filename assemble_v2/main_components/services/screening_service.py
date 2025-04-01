import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Screening,Film
from typing import List, Optional
from datetime import datetime, date

class ScreeningService:
    """
    Handles operations related to cinema screenings.
    """

    def __init__(self, session: Session):
        """Initializes the ScreeningService with a session."""
        self.session = session

    def create_screening(self, film_id : int, screen_id : str, cinema_id : int, date : datetime, start_time : datetime, screening_availability : int) -> Screening:
        """Creates a new screening."""

        # Check for duplicate screenings
        existing_screening = self.session.query(Screening).filter_by(
            screen_id=screen_id,
            cinema_id=cinema_id,
        ).first()

        if existing_screening:
            raise ValueError("A screening with the same screen and cinema already exists.")

        screening = Screening.create_screening(film_id, screen_id, cinema_id, date, start_time, screening_availability)
        self.session.add(screening)
        self.session.commit()
        return screening

    def get_screening_by_id(self, screening_id: int) -> Optional[Screening]:
        """Retrieves a screening by ID."""
        return self.session.query(Screening).filter_by(screening_id=screening_id).first()

    def get_screening_for_screen(self, screen_id: str, cinema_id : int) -> Optional[Screening]:
        """Retrieves a screening by screen ID."""
        return self.session.query(Screening).filter_by(screen_id=screen_id, cinema_id=cinema_id).first()
    
    def get_all_screenings_for_cinema(self, cinema_id : int) -> List[Screening]:
        """Retrieves all screenings for a given cinema."""
        return self.session.query(Screening).filter_by(cinema_id=cinema_id).all()
    
    def get_all_screenings(self) -> List[Screening]:
        """Retrieves all screenings."""
        return self.session.query(Screening).all()
    
    def add_film_to_screening(self, screening_id: int, film_id: int) -> Screening:
        """Adds a film to a screening."""
        try:
            screening = self.session.query(Screening).filter_by(screening_id=screening_id).first()
            if not screening:
                raise ValueError(f"Screening with ID {screening_id} not found.")

            film = self.session.query(Film).filter_by(film_id=film_id).first()
            if not film:
                raise ValueError(f"Film with ID {film_id} not found.")
            
            screening.film_id = film_id # Connect film to screening
            self.session.commit()
            return screening
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Failed to add film {film_id} to screening {screening_id}: {e}")

    def remove_film_from_screening(self, screening_id: int) -> Screening:
        """Removes the film from a screening."""
        try:
            screening = self.session.query(Screening).filter_by(screening_id=screening_id).first()
            if not screening:
                raise ValueError(f"Screening with ID {screening_id} not found.")
            
            screening.film_id = None # Disconnect film from screening
            self.session.commit()
            return screening
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Failed to remove film from screening {screening_id}: {e}")

    def update_screening(self, screening_id: int, film_id: int = None, screen_id: str = None, cinema_id : int = None,  date: datetime = None, start_time: datetime = None, screening_availability : int = None) -> Optional[Screening]:
        """Updates a screening's details."""
        screening = self.get_screening_by_id(screening_id)
        if screening:
            if film_id:
                screening.set_film_id(film_id)
            if screen_id:
                screening.set_screen_id(screen_id)
            if cinema_id:
                screening.cinema_id = cinema_id
            if date:
                screening.set_date(date)
            if start_time:
                screening.set_start_time(start_time)
            if screening_availability:
                screening.set_screening_availability(screening_availability)
            
            # Check for duplicate screenings (excluding the screening being updated)
            existing_screening = self.session.query(Screening).filter(
                Screening.screen_id == (screen_id if screen_id is not None else screening.screen_id),
                Screening.cinema_id == (cinema_id if cinema_id is not None else screening.cinema_id),
                Screening.screening_id != screening_id  # Exclude the current screening
            ).first()

            if existing_screening:
                raise ValueError("A screening with the same screen and cinema already exists.")
            
            self.session.commit()
            return screening
        return None

    def delete_screening(self, screening_id: int) -> bool:
        """Deletes a screening."""
        screening = self.get_screening_by_id(screening_id)
        if screening:
            self.session.delete(screening)
            self.session.commit()
            return True
        return False
    

    def get_screenings_by_cinema_and_date(self, cinema_id: int, date_obj: date) -> List[Screening]:
        """Retrieves all screenings for a given cinema on a specific date."""
        return self.session.query(Screening).filter(
            Screening.cinema_id == cinema_id,
            Screening.date == date_obj
        ).all()
