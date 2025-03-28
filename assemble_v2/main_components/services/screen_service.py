import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Screen, Screening
from typing import List, Optional
from datetime import datetime


class ScreenService:
    """
    Handles operations related to cinema screens.
    """

    def __init__(self, session: Session): 
        """Initializes the ScreenService with a session."""
        self.session = session


    def create_screen(self, screen_id: str, cinema_id: int, total_capacity : int, row_number : int) -> Screen:
        """Creates a new screen."""
        screen = Screen.create_screen(screen_id, cinema_id, total_capacity, row_number)
        self.session.add(screen)
        self.session.commit()
        return screen

    def get_screen_by_id(self, screen_id: str, cinema_id: int) -> Optional[Screen]:
        """Retrieves a screen by ID."""
        return self.session.query(Screen).filter_by(screen_id=screen_id, cinema_id=cinema_id).first()

    def get_all_screens(self) -> List[Screen]:
        """Retrieves all screens."""
        return self.session.query(Screen).all()
    
    def get_screens(self, cinema_id: int) -> List[Screen]:
        """Retrieves all screens for a given cinema."""
        return self.session.query(Screen).filter_by(cinema_id=cinema_id).all()
    
    def get_screen_for_screening(self, screening_id: str) -> Optional[Screen]:
        """Retrieves the screen for a given screening."""
        screening = self.get_screening_by_id(screening_id)
        if screening:
            return self.session.query(Screen).filter_by(screen_id=screening.screen_id).first()
        return None
    

    def update_screen_capacities(self, screen_id: str, cinema_id : int, total_capacity : int = None, row_number : int = None) -> Optional[Screen]:
        """Updates the seating capacities of a screen."""
        screen = self.session.query(Screen).filter_by(screen_id=screen_id, cinema_id=cinema_id).first()
        if screen:
            if total_capacity is not None:
                screen.total_capacity = total_capacity
            if row_number is not None:
                screen.row_number = row_number
            self.session.commit()
            return screen
        return None

    def delete_screen(self, screen_id: str, cinema_id : int) -> bool:
        """Deletes a screen."""
        screen = self.session.query(Screen).filter_by(screen_id=screen_id, cinema_id=cinema_id).first()
        if screen:
            self.session.delete(screen)
            self.session.commit()
            return True
        return False
