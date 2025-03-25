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
    screen_id = Column(String(255), ForeignKey('screens.screen_id'))
    film_id = Column(Integer, ForeignKey('films.film_id'))
    date = Column(Date) # Change back to DateTime for no testing.
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    lower_hall_sold = Column(Integer)
    upper_hall_sold = Column(Integer)
    vip_sold = Column(Integer)

    # Relationships
    screen = relationship('Screen', back_populates='screenings')
    film = relationship('Film', back_populates='screenings')
    bookings = relationship('Booking', back_populates='screening')
    tickets = relationship('Ticket', back_populates='screening')

    def __init__(self, screen_id: str, film_id: str, date: datetime, start_time: datetime, end_time: datetime, lower_hall_sold: int, upper_hall_sold: int, vip_sold: int):
        """
        Initializes a new Screening object with the provided attributes.
        """
        self.screen_id = screen_id
        self.film_id = film_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.lower_hall_sold = lower_hall_sold
        self.upper_hall_sold = upper_hall_sold
        self.vip_sold = vip_sold

    @classmethod
    def create_screening(cls, screen_id: str, film_id: int, date: datetime, start_time: datetime, end_time: datetime, lower_hall_sold: int = 0, upper_hall_sold: int = 0, vip_sold: int = 0) -> 'Screening':
        """
        Creates a new Screening object and sets its attributes.
        """
        screening = cls(
            screen_id=screen_id,
            film_id=film_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            lower_hall_sold=lower_hall_sold,
            upper_hall_sold=upper_hall_sold,
            vip_sold=vip_sold,
        )
        return screening

    def get_screening_id(self) -> int:
        """
        Retrieves the unique identifier of the screening.

        Returns:
            str: The screening ID.
        """
        return self.screening_id

    def get_screen_id(self) -> 'Screen':
        """
        Retrieves the associated screen.

        Returns:
        - Screen: The associated Screen object.
        """
        return self.screen
    
    def get_film_id(self) -> 'Film':
        """
        Retrieves the associated film.

        Returns:
        - Film: The associated Film object.
        """
        return self.film
    
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
    
    def get_end_time(self) -> datetime:
        """
        Retrieves the screening end time.

        Returns:
        - datetime: The end time of the screening.
        """
        return self.end_time
    
    def get_lower_hall_sold(self) -> int:
        """
        Retrieves the number of lower hall tickets sold.

        Returns:
        - int: The number of lower hall tickets sold.
        """
        return self.lower_hall_sold

    def get_upper_hall_sold(self) -> int:
        """
        Retrieves the number of upper hall tickets sold.

        Returns:
        - int: The number of upper hall tickets sold.
        """
        return self.upper_hall_sold

    def get_vip_sold(self) -> int:
        """
        Retrieves the number of VIP tickets sold.

        Returns:
        - int: The number of VIP tickets sold.
        """
        return self.vip_sold
    
    def set_screen_id(self, screen_id: 'Screen') -> None:
        """
        Sets the screen ID for the screening.

        Parameters:
        - screen_id (Screen): The associated screen.
        """
        self.screen_id = screen_id.screen_id
    
    def set_film_id(self, film_id: 'Film') -> None:
        """
        Sets the film ID for the screening.

        Parameters:
        - film_id (Film): The associated film.
        """
        self.film_id = film_id.film_id
    
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

    def set_end_time(self, end_time: datetime) -> None:
        """
        Sets the end time of the screening.

        Parameters:
        - end_time (datetime): The end time of the screening.
        """
        self.end_time = end_time

    def set_lower_hall_sold(self, lower_hall_sold: int) -> None:
        """
        Sets the number of lower hall tickets sold.

        Parameters:
        - lower_hall_sold (int): The number of lower hall tickets sold.
        """
        self.lower_hall_sold = lower_hall_sold

    def set_upper_hall_sold(self, upper_hall_sold: int) -> None:
        """
        Sets the number of upper hall tickets sold.

        Parameters:
        - upper_hall_sold (int): The number of upper hall tickets sold.
        """
        self.upper_hall_sold = upper_hall_sold

    def set_vip_sold(self, vip_sold: int) -> None:
        """
        Sets the number of VIP tickets sold.

        Parameters:
        - vip_sold (int): The number of VIP tickets sold.
        """
        self.vip_sold = vip_sold