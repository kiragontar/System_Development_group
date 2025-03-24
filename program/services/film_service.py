from sqlalchemy.orm import Session
from models import Cinema, Film, CinemaFilm
from typing import List, Optional
from datetime import datetime

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
    # Add method to create film.
    def create_film(self, name: str, genre: List[str], cast: List[str], 
                 description: str, age_rating: str, critic_rating: float, 
                 runtime: int, release_date: datetime, movie_poster: str = None) -> Film:
        """Creates a new film"""
        try:
            new_film = Film(
                name=name,
                genre=genre,
                cast=','.join(cast),
                description=description,
                age_rating=age_rating,
                critic_rating=critic_rating,
                runtime=runtime,
                release_date=release_date,
                movie_poster=movie_poster
            )
            self.session.add(new_film)
            self.session.commit()
            return new_film
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Failed to create film: {e}")

    def delete_film(self, film_id: int) -> None:
        """Deletes a film."""
        try:
            film = self.session.query(Film).filter(Film.film_id == film_id).first()
            if film:
                self.session.delete(film)
                self.session.commit()
            else:
                raise ValueError(f"Film with ID {film_id} not found.")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Failed to delete film: {e}")


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

    def update_film(self, film_id: int, name: str = None, genre: List[str] = None, cast: List[str] = None,
                    description: str = None, age_rating: str = None, critic_rating: float = None,
                    runtime: int = None, release_date: datetime = None, movie_poster: str = None) -> Optional[Film]:
        """Updates a film's details."""
        film = self.get_all_films_by_id(film_id)
        if film:
            if name:
                film.name = name
            if genre:
                film.genre = ','.join(genre)
            if cast:
                film.cast = ','.join(cast)
            if description:
                film.description = description
            if age_rating:
                film.age_rating = age_rating
            if critic_rating:
                film.critic_rating = critic_rating
            if runtime:
                film.runtime = runtime
            if release_date:
                film.release_date = release_date
            if movie_poster:
                film.movie_poster = movie_poster
            self.session.commit()
            return film
        return None
