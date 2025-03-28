from sqlalchemy.orm import Session
from models import City, Cinema
from typing import List, Optional


class CityService:
    """
    Handles operations related to cities.
    """

    def __init__(self, session: Session):
        """Initializes the CityService with a session."""
        self.session = session

    def create_city(self, name: str, country: str) -> City:
        """Creates a new city."""
        city = City(name=name, country=country)
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

    def update_city(self, city_id: int, name: str = None, country: str = None) -> Optional[City]:
        """Updates a city's name and/or country."""
        city = self.get_city_by_id(city_id)
        if city:
            if name:
                city.name = name
            if country:
                city.country = country
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
