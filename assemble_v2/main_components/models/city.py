from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base


# City model (Table):
class City(Base):
    """
    Represents a city, including its name, country, and its associated cinemas.
    """
    __tablename__ = 'cities'

    city_id = Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier for the city.
    name = Column(String(255), nullable=False, unique=True)  # The name of the city.
    country = Column(String(255), nullable=False)  # The country where the city is located.
    price_morning = Column(Integer, nullable=False)  
    price_afternoon = Column(Integer, nullable=False) 
    price_evening = Column(Integer, nullable=False)  

    # Relationship to cinemas in the city
    cinemas = relationship('Cinema', back_populates='city')  # List of cinemas in the city.

    def __init__(self, name: str, country: str, price_morning: int, price_afternoon: int, price_evening: int):
        """
        Initialize the City object.

        Parameters:
        - name (str): The name of the city.
        - country (str): The country of the city.
        """
        self.name = name
        self.country = country
        self.price_morning = price_morning
        self.price_afternoon = price_afternoon
        self.price_evening = price_evening

    def get_id(self) -> int:
        """Returns the unique identifier of the city."""
        return self.city_id

    def get_name(self) -> str:
        """Returns the name of the city."""
        return self.name

    def get_country(self) -> str:
        """Returns the country of the city."""
        return self.country
    
    def get_price_morning(self) -> int:
        return self.price_morning
    
    def get_price_afternoon(self) -> int:
        return self.price_afternoon
    
    def get_price_evening(self) -> int:
        return self.price_evening
    
    def set_name(self, name: str) -> None:
        """Sets the name of the city."""
        if name:   
            self.name = name
        else:
            raise ValueError("Name cannot be empty.")
        
        
    def set_country(self, country: str) -> None:
        """Sets the country of the city."""
        if country:
            self.country = country
        else:
            raise ValueError("Country cannot be empty.")
    def set_price_morning(self, price: int) -> None:

        if price:
            self.price_morning = price
        else:
            raise ValueError("Price cannot be empty.")
    def set_price_afternoon(self, price: int) -> None:

        if price:
            self.price_afternoon = price
        else:
            raise ValueError("Price cannot be empty.")
    def set_price_evening(self, price: int) -> None:

        if price:
            self.price_evening = price
        else:
            raise ValueError("Price cannot be empty.")
    def __repr__(self):
      return f"<City(city_id={self.city_id}, name='{self.name}', country='{self.country}')>"
    