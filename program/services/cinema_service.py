from sqlalchemy.orm import Session
from models import Cinema, User, Role, Screen, Screening, CinemaFilm



class CinemaService:
    def __init__(self, session: Session):
        self.session = session

    def create_cinema(self, name: str, address: str, city_id: int) -> Cinema:
        cinema = Cinema(name=name, address=address, city_id=city_id)
        self.session.add(cinema)
        self.session.commit()
        return cinema

    def get_cinema_by_id(self, cinema_id: int) -> Cinema:
        return self.session.query(Cinema).filter_by(cinema_id=cinema_id).first()

    def get_all_cinemas(self) -> list[Cinema]:
        return self.session.query(Cinema).all()

    def update_cinema(self, cinema_id: int, name: str = None, address: str = None, city_id: int = None) -> Cinema:
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            if name:
                cinema.name = name
            if address:
                cinema.address = address
            if city_id:
                cinema.city_id = city_id
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

    def get_films(self, cinema_id: int) -> list['CinemaFilm']:
        cinema = self.get_cinema_by_id(cinema_id)
        if cinema:
            return cinema.get_films()
        return []
    
    def get_cinemas_by_city(self, city_id: int) -> list[Cinema]:
        """Retrieves cinemas by city."""
        return self.session.query(Cinema).filter_by(city_id=city_id).all()

    def get_cinemas_by_film(self, film_id: int) -> list[Cinema]:
        """Retrieves cinemas showing a specific film."""
        return self.session.query(Cinema).join(CinemaFilm).filter(CinemaFilm.film_id == film_id).all()
