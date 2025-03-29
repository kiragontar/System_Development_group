from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Date
from sqlalchemy.orm import relationship
from . import Base
from .screen import Screen
from .film import Film
from datetime import datetime


class Screening(Base):
    """
    Represents a cinema screening for a specific film in a screen at a given date and time.
    """
    __tablename__ = 'screenings'

    screening_id = Column(Integer, primary_key=True, autoincrement=True)
    film_id = Column(Integer, ForeignKey('films.film_id'))
    screen_id = Column(String(255), ForeignKey('screens.screen_id'))
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'))
    date = Column(Date)
    start_time = Column(DateTime)
    screening_availability = Column(Integer, nullable=False)

    # Relationships
    cinema = relationship('Cinema', back_populates='screenings')
    screen = relationship('Screen', back_populates='screenings')
    film = relationship('Film', back_populates='screenings')
    seat_availability = relationship('SeatAvailability', back_populates='screening')

    def __init__(self, film_id: str, screen_id: str, cinema_id: int, date: datetime, start_time: datetime, screening_availability: int = 1):
        """
        Initializes a new Screening object with the provided attributes.
        """
        self.film_id = film_id
        self.screen_id = screen_id
        self.cinema_id = cinema_id
        self.date = date
        self.start_time = start_time
        self.screening_availability = screening_availability
        
        

    @classmethod
    def create_screening(cls, film_id: str, screen_id: str, cinema_id: int, date: datetime, start_time: datetime, screening_availability: int = 1) -> 'Screening':
        """
        Creates a new Screening object and sets its attributes.
        
        Parameters:
        - film_id (str): The ID of the film to be screened
        - screen_id (str): The ID of the screen/hall where the film will be shown
        - cinema_id (int): The ID of the cinema
        - date (datetime): The date of the screening
        - start_time (datetime): The start time of the screening
        - screening_availability (int): Availability status, default is 1 (available)
        
        Returns:
        - Screening: A new Screening object
        """
        screening = cls(
            film_id=film_id,
            screen_id=screen_id,
            cinema_id=cinema_id,
            date=date,
            start_time=start_time,
            screening_availability=screening_availability
        )
        return screening

    def get_screening_id(self) -> int:
        """
        Retrieves the unique identifier of the screening.

        Returns:
            str: The screening ID.
        """
        return self.screening_id

    def get_film_id(self) -> 'Film':
        """
        Retrieves the associated film.

        Returns:
        - Film: The associated Film object.
        """
        return self.film

    def get_screen_id(self) -> 'Screen':
        """
        Retrieves the associated screen.

        Returns:
        - Screen: The associated Screen object.
        """
        return self.screen
    
    
    def get_date(self) -> datetime:
        """
        Retrieves the screening date.

        Returns:
        - datetime: The date of the screening.
        """
        return self.date
    
    def get_start_time(self) -> datetime:
        """
        Retrieves the screening start time.

        Returns:
        - datetime: The start time of the screening.
        """
        return self.start_time
    
    def geet_screening_availability(self) -> int:
        """
        Retrieves the screening availability status.
        
        Returns:
        - int: The availability status of the screening.
        """
        return self.screening_availability
    
    def set_film_id(self, film_id: 'Film') -> None:
        """
        Sets the film ID for the screening.

        Parameters:
        - film_id (Film): The associated film.
        """
        self.film_id = film_id.film_id

    def set_screen_id(self, screen_id: 'Screen') -> None:
        """
        Sets the screen ID for the screening.

        Parameters:
        - screen_id (Screen): The associated screen.
        """
        self.screen_id = screen_id.screen_id
    
    def set_date(self, date: datetime) -> None:
        """
        Sets the date of the screening.

        Parameters:
        - date (datetime): The date of the screening.
        """
        self.date = date
    
    def set_start_time(self, start_time: datetime) -> None:
        """
        Sets the start time of the screening.

        Parameters:
        - start_time (datetime): The start time of the screening.
        """
        self.start_time = start_time

    def set_screening_availability(self, screening_availability: int) -> None:
        """
        Sets the availability status of the screening.

        Parameters:
        - screening_availability (int): The availability status of the screening.
        """
        self.screening_availability = screening_availability