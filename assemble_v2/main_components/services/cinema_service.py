import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Cinema, User, Role, Screen, Screening, Film


class CinemaService:
    def __init__(self, session: Session):
        self.session = session

    def create_cinema(self, city_id: int, name: str, address: str) -> Cinema:
        cinema = Cinema(city_id=city_id, name=name, address=address)
        self.session.add(cinema)
        self.session.commit()
        return cinema

    def get_cinema_by_id(self, cinema_id: int) -> Cinema:
        return self.session.query(Cinema).filter_by(cinema_id=cinema_id).first()

    def get_cinema_by_name(self, cinema_name: str) -> Cinema:
        return self.session.query(Cinema).filter_by(name=cinema_name).first()

    def get_all_cinemas(self) -> list[Cinema]:
        return self.session.query(Cinema).all()

    def update_cinema(self, cinema_id: int, city_id: int = None, name: str = None, address: str = None) -> Cinema:
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            if city_id:
                cinema.city_id = city_id
            if name:
                cinema.name = name
            if address:
                cinema.address = address
            self.session.commit()
            return cinema
        return None

    def delete_cinema(self, cinema_id: int) -> bool:
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            self.session.delete(cinema)
            self.session.commit()
            return True
        return False

    def get_managers(self, cinema_id: int) -> list[User]:
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            return self.session.query(User).join(Role).filter(User.cinema_id == cinema_id, Role.name == 'Manager').all()
        return []

    def get_admins(self, cinema_id: int) -> list[User]:
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            return self.session.query(User).join(Role).filter(User.cinema_id == cinema_id, Role.name == 'Admin').all()
        return []

    def get_staff(self, cinema_id: int) -> list[User]:
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            return self.session.query(User).join(Role).filter(User.cinema_id == cinema_id, Role.name == 'Staff').all()
        return []

    def get_screens(self, cinema_id: int) -> list['Screen']:
        return self.session.query(Screen).filter_by(cinema_id=cinema_id).all()

    def get_screenings(self, cinema_id: int) -> list['Screening']:
        return self.session.query(Screening).filter_by(cinema_id=cinema_id).all()

    def get_films(self, cinema_id: int) -> list['Film']:
        films = self.session.query(Film).join(Screening).filter(Screening.cinema_id == cinema_id).distinct().all() # Get distinct films
        return films

    def get_cinemas_by_city(self, city_id: int) -> list[Cinema]:
        """Retrieves cinemas by city."""
        return self.session.query(Cinema).filter_by(city_id=city_id).all()

    def get_cinemas_by_film(self, film_id: int) -> list[Cinema]:
        """Retrieves cinemas showing a specific film."""
        cinemas = self.session.query(Cinema).join(Screening).filter(Screening.film_id == film_id).distinct().all()
        return cinemas