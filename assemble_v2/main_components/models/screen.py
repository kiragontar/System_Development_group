from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from sqlalchemy.orm import Session
from datetime import datetime


# Screen model (Table):
class Screen(Base):
    """
    Represents a cinema screen with seating capacities for upper, lower, and VIP sections.
    This class also provides methods to check if the screen is in use at a specific time,
    and to manage its capacities.
    """
    __tablename__ = 'screens'

    screen_id = Column(String(255), primary_key=True)  # Unique identifier for the screen
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'), primary_key=True)  # Foreign key to the cinema
    total_capacity = Column(Integer, nullable=False)  # Total seating capacity (calculated)
    row_number = Column(Integer, nullable=False)  # Number of rows in the screen


    # Relationship to Cinema (one screen belongs to one cinema)
    
    cinema = relationship('Cinema', back_populates='screens')
    screenings = relationship('Screening', back_populates='screen')  # Screenings on this screen

    def __init__(self, screen_id: str, cinema_id: int, total_capacity: int, row_number: int):
        """
        Initializes a new screen with the provided details.
        """
        self.screen_id = screen_id
        self.cinema_id = cinema_id
        self.total_capacity = total_capacity
        self.row_number = row_number

    def get_id(self) -> str:
        """
        Returns the unique identifier of the screen.
        
        Returns:
        - str: The screen's unique identifier, eg. : "S1".
        """
        return self.screen_id

    def get_total_capacity(self) -> int:
        """
        Returns the total seating capacity of the screen.
        """
        return self.total_capacity

    def update_total_capacity(self, total_capacity : int) -> None:
        """
        Updates the total seating capacity of the screen by summing the capacities of all sections
        (upper, lower, and VIP).
        """
        self.total_capacity = total_capacity
    
    def delete(self, session: Session) -> None:
        """
        Deletes the screen from the database using the session passed into the method.

        Parameters:
        - session (Session): The SQLAlchemy session used for querying and committing transactions.
        """
        session.delete(self)
        session.commit()  # Commit the transaction
    
    @classmethod
    def create_screen(cls, screen_id: str, cinema_id: int, total_capacity: int, row_number : int) -> 'Screen':
        """
        Creates a new Screen object and sets its attributes.
        """
        screen = cls(screen_id, cinema_id, total_capacity, row_number)
        return screen
    
    def __repr__(self) -> str:
        return f"<Screen(screen_id='{self.screen_id}', cinema_id='{self.cinema_id}')>"
    