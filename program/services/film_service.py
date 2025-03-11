from sqlalchemy.orm import Session
from models import Cinema, Film, CinemaFilm
from typing import List, Optional


class CinemaFilmService:
    """Manages film-related operations for a specific cinema."""

    def __init__(self, cinema: Cinema, session: Session):
        """Initializes the CinemaFilmService for a specific cinema."""
        self.cinema = cinema
        self.session = session

    def get_all_films(self) -> List[Film]:
        """Retrieves all films showing at the cinema."""
        return self.cinema.get_films()

    def get_all_films_by_genre(self, genre: str) -> List[Film]:
        """Retrieves all films of a specific genre showing at the cinema."""
        return [film for film in self.cinema.get_films() if genre in film.get_genre()]
    
    def get_all_films_by_id(self, film_id: str) -> Optional[Film]:
        """Retrieves a film by ID if it's showing at the cinema."""
        for film in self.cinema.get_films():
            if film.film_id == film_id:
                return film
        return None
    
    def add_film_to_cinema(self, film: Film) -> None:
        """Adds a film to the cinema."""
        cinema_film = CinemaFilm(cinema_id=self.cinema.cinema_id, film_id=film.film_id)
        self.session.add(cinema_film)
        self.session.commit()
    
    def remove_film_from_cinema(self, film_id: str) -> None:
        """Removes a film from the cinema."""
        cinema_film = self.session.query(CinemaFilm).filter_by(cinema_id=self.cinema.cinema_id, film_id=film_id).first()
        if cinema_film:
            self.session.delete(cinema_film)
            self.session.commit()