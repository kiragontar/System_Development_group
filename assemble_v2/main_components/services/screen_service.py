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


    def create_screen(self, screen_id: str, cinema_id: int, capacity_upper: int = 0, capacity_lower: int = 0, capacity_vip: int = 0) -> Screen:
        """Creates a new screen."""
        screen = Screen.create_screen(screen_id, cinema_id, capacity_upper, capacity_lower, capacity_vip)
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

    def update_screen_capacities(self, screen_id: str, capacity_upper: int = None, capacity_lower: int = None, capacity_vip: int = None) -> Optional[Screen]:
        """Updates the seating capacities of a screen."""
        screen = self.get_screen_by_id(screen_id)
        if screen:
            if capacity_upper is not None:
                screen.set_capacity_upper(capacity_upper)
            if capacity_lower is not None:
                screen.set_capacity_lower(capacity_lower)
            if capacity_vip is not None:
                screen.set_capacity_vip(capacity_vip)
            self.session.commit()
            return screen
        return None

    def delete_screen(self, screen_id: str) -> bool:
        """Deletes a screen."""
        screen = self.get_screen_by_id(screen_id)
        if screen:
            screen.delete(self.session)
            return True
        return False

    def check_screen_in_use(self, screen_id: str, start_time: datetime, end_time: datetime, screening_service) -> bool: 
        """Checks if a screen is in use during a given time range."""
        screenings = screening_service.get_screenings_for_screen(screen_id)
        for screening in screenings:
            if screening.start_time is not None and screening.end_time is not None and screening.start_time < end_time and screening.end_time > start_time:
                return True
        return False