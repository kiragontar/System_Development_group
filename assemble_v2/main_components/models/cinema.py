from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


# Cinema model (Table):
class Cinema(Base):
    """
    Represents a cinema entity, including its details like name, address, and relationships with films, screens, and screenings.
    """
    __tablename__ = "cinemas" # This matches the table name.

    city_id = Column(Integer, ForeignKey('cities.city_id'), nullable = False) # City ID references the City table.
    cinema_id = Column(Integer, primary_key = True, autoincrement=True) # Makes a column of id, making it a primary key and type integer.
    name = Column(String(255), nullable = False, unique=True) # name shouldnt be nullable, so its mandatory.
    address = Column(String(255), nullable = False)

    city = relationship('City', back_populates='cinemas')  # One cinema belongs to one city
    screens = relationship('Screen', back_populates='cinema')  # Screens in this cinema
    seats = relationship('Seat', back_populates='cinema')
    users = relationship('User', back_populates='cinema')
    screenings = relationship('Screening', back_populates='cinema')

    def __init__(self, city_id: int, name: str, address: str):
        """
        Initialize the Cinema object.
        
        Parameters:
        - name (str): The name of the cinema.
        - address (str): The address of the cinema.
        - city_id (int): The city ID where the cinema is located.
        """
        self.city_id = city_id
        self.name = name
        self.address = address

    
    def get_id(self) -> int:
        """Returns the unique identifier of the cinema."""
        return self.cinema_id

    def get_name(self) -> str:
        """Returns the name of the cinema."""
        return self.name

    def get_address(self) -> str:
        """Returns the address of the cinema."""
        return self.address
    
    def set_name(self, name: str) -> None:
        """Sets the name of the cinema."""
        self.name = name

    def set_address(self, address: str) -> None:
        """Sets the address of the cinema."""
        self.address = address

    def __repr__(self):
        return f"<Cinema(cinema_id={self.cinema_id}, name='{self.name}', address='{self.address}')>"