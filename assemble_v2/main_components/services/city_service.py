import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import City, Cinema
from typing import List, Optional


class CityService:
    """
    Handles operations related to cities.
    """

    def __init__(self, session: Session):
        """Initializes the CityService with a session."""
        self.session = session

    def create_city(self, name: str, country: str, price_morning : int, price_afternoon : int, price_evening : int) -> City:
        """Creates a new city."""
        existing_city = self.session.query(City).filter_by(
            name=name,
            country=country
        ).first()

        if existing_city:
            raise ValueError(f"City with name '{name}' and country '{country}' already exists.")
        city = City(name=name, country=country, price_morning = price_morning, price_afternoon = price_afternoon, price_evening = price_evening)
        self.session.add(city)
        self.session.commit()
        return city

    def get_city_by_id(self, city_id: int) -> Optional[City]:
        """Retrieves a city by ID."""
        return self.session.query(City).filter_by(city_id=city_id).first()

    def get_city_by_name(self, name: str) -> Optional[City]:
        """Retrieves a city by name."""
        return self.session.query(City).filter_by(name=name).first()

    def get_all_cities(self) -> List[City]:
        """Retrieves all cities."""
        return self.session.query(City).all()

    def update_city(self, city_id: int, name: str = None, country: str = None, price_morning : str = None, price_afternoon : str = None, price_evening : str = None) -> Optional[City]:
        """Updates a city's name and/or country."""
        city = self.get_city_by_id(city_id)
        if city:
            if name:
                city.name = name
            if country:
                city.country = country
            if price_morning:
                city.price_morning = price_morning
            if price_afternoon:
                city.price_afternoon = price_afternoon
            if price_evening:
                city.price_evening = price_evening

            # Duplicate check
            existing_city = self.session.query(City).filter_by(
                name=name,
                country=country
            ).filter(City.city_id != city_id).first() #exclude the current city

            if existing_city:
                raise ValueError(f"City with name '{city.name}' and country '{city.country}' already exists.")
            
            self.session.commit()
            return city
        return None

    def delete_city(self, city_id: int) -> bool:
        """Deletes a city."""
        city = self.get_city_by_id(city_id)
        if city:
            # Delete associated cinemas first
            cinemas = self.session.query(Cinema).filter_by(city_id=city_id).all()
            for cinema in cinemas:
                self.session.delete(cinema)

            self.session.delete(city)
            self.session.commit()
            return True
        return False

    def get_cinemas_in_city(self, city_id: int) -> List[Cinema]:
        """Retrieves all cinemas in a city."""
        city = self.get_city_by_id(city_id)
        if city:
            return city.cinemas
        return []
