from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


# Cinema model (Table):
class Cinema(Base):
    """
    Represents a cinema entity, including its details like name, address, and relationships with films, screens, and screenings.

    Attributes:
        cinema_id (int): Unique identifier for the cinema.
        city_id (int): City ID the cinema belongs to.
        name (str): The name of the cinema.
        address (str): The address of the cinema.
        films (CinemaFilms): Films that are available in this cinema.
        screens (Screen): Screens in the cinema.
        screenings (Screening): Screenings held in the cinema.
    """
    __tablename__ = "cinemas" # This matches the table name.

    cinema_id = Column(Integer, primary_key = True) # Makes a column of id, making it a primary key and type integer.
    city_id = Column(Integer, ForeignKey('city.city_id'), nullable = False) # City ID references the City table.
    name = Column(String, nullable = False) # name shouldnt be nullable, so its mandatory.
    address = Column(String, nullable = False)

    city = relationship('City', back_populates='cinemas')  # One cinema belongs to one city
    cinema_films = relationship('CinemaFilm', back_populates='cinema')  # Films related to this cinema
    screens = relationship('Screen', back_populates='cinema')  # Screens in this cinema
    screenings = relationship('Screening', back_populates='cinema')  # Screenings in this cinema
    users = relationship('User', back_populates='cinema')

    def __init__(self, name: str, address: str, city_id: int):
        """
        Initialize the Cinema object.
        
        Parameters:
        - name (str): The name of the cinema.
        - address (str): The address of the cinema.
        - city_id (int): The city ID where the cinema is located.
        """
        self.name = name
        self.address = address
        self.city_id = city_id
    
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

    def get_films(self):
        return [cinema_film.film for cinema_film in self.cinema_films]

    def __repr__(self):
        return f"<Cinema(cinema_id={self.cinema_id}, name='{self.name}', address='{self.address}')>"