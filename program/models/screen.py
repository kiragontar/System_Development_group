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
    capacity_upper = Column(Integer, nullable=False)  # Upper section seating capacity
    capacity_lower = Column(Integer, nullable=False)  # Lower section seating capacity
    capacity_vip = Column(Integer, nullable=False)  # VIP seating capacity
    total_capacity = Column(Integer, nullable=False)  # Total seating capacity (calculated)

    # Relationship to Cinema (one screen belongs to one cinema)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'))
    cinema = relationship('Cinema', back_populates='screens')
    screenings = relationship('Screening', back_populates='screen')  # Screenings on this screen
    seats = relationship('Seat', back_populates='screen')

    def __init__(self, screen_id: str, cinema_id: int, capacity_upper: int, capacity_lower: int, capacity_vip: int):
        """
        Initializes a new screen with the provided details.
        """
        self.screen_id = screen_id
        self.cinema_id = cinema_id
        self.capacity_upper = capacity_upper
        self.capacity_lower = capacity_lower
        self.capacity_vip = capacity_vip
        self.total_capacity = capacity_upper + capacity_lower + capacity_vip

    def get_id(self) -> str:
        """
        Returns the unique identifier of the screen.
        
        Returns:
        - str: The screen's unique identifier, eg. : "S1".
        """
        return self.screen_id
    
    def get_capacity_upper(self) -> int:
        """
        Returns the number of seats in the upper section of the screen.
        
        Returns:
        - int: The seating capacity of the upper section.
        """
        return self.capacity_upper
    
    def get_capacity_lower(self) -> int:
        """
        Returns the number of seats in the lower section of the screen.
        
        Returns:
        - int: The seating capacity of the lower section.
        """
        return self.capacity_lower

    def get_capacity_vip(self) -> int:
        """
        Returns the number of VIP seats in the screen.
        
        Returns:
        - int: The number of VIP seats in the screen.
        """
        return self.capacity_vip
    
    def get_total_capacity(self) -> int:
        """
        Returns the total seating capacity of the screen.
        """
        return self.total_capacity

    def set_capacity_upper(self, capacity_upper: int) -> None:
        """
        Sets the seating capacity for the upper section of the screen and updates the total capacity.
        
        Args:
        - capacity_upper (int): The number of seats to set in the upper section.
        """
        self.capacity_upper = capacity_upper
        self.update_total_capacity()

    def set_capacity_lower(self, capacity_lower: int) -> None:
        """
        Sets the seating capacity for the lower section of the screen and updates the total capacity.
        
        Args:
        - capacity_lower (int): The number of seats to set in the lower section.
        """
        self.capacity_lower = capacity_lower
        self.update_total_capacity()

    def set_capacity_vip(self, capacity_vip: int) -> None:
        """
        Sets the seating capacity for the VIP section of the screen and updates the total capacity.
        
        Args:
        - capacity_vip (int): The number of seats to set in the VIP section.
        """
        self.capacity_vip = capacity_vip
        self.update_total_capacity()

    def update_total_capacity(self) -> None:
        """
        Updates the total seating capacity of the screen by summing the capacities of all sections
        (upper, lower, and VIP).
        """
        self.total_capacity = self.capacity_upper + self.capacity_lower + self.capacity_vip

    
    def delete(self, session: Session) -> None:
        """
        Deletes the screen from the database using the session passed into the method.

        Parameters:
        - session (Session): The SQLAlchemy session used for querying and committing transactions.
        """
        session.delete(self)
        session.commit()  # Commit the transaction

    
    @classmethod
    def create_screen(cls, screen_id: str, cinema_id: int, capacity_upper: int = 0, capacity_lower: int = 0, capacity_vip: int = 0) -> 'Screen':
        """
        Creates a new Screen object and sets its attributes.
        """
        screen = cls(screen_id, cinema_id, capacity_upper, capacity_lower, capacity_vip)
        return screen
    
    def __repr__(self) -> str:
        return f"<Screen(screen_id='{self.screen_id}', cinema_id='{self.cinema_id}')>"
    