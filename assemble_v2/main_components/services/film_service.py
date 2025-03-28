import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Cinema, Film
from typing import List, Optional
from datetime import datetime
import logging 

logging.basicConfig(level=logging.INFO)

class FilmService:
    """Manages film-related operations for a specific cinema."""

    def __init__(self, session: Session):
        self.session = session

    def get_film_by_name(self, film_name: str) -> Film:
        """Retrieves a film by its name."""
        film = self.session.query(Film).filter_by(name=film_name).first()
        if film is None:
            raise ValueError(f"Film with name {film_name} not found.")
        return film

    def get_all_films(self) -> List[Film]:
        try:
            films = self.session.query(Film).all()
            return films
        except Exception as e:
            logging.error(f"Failed to retrieve all films: {e}")
            return []  # Return an empty list on error

    def get_all_films_by_genre(self, genre: str) -> List[Film]:
        """Retrieves all films of a specific genre from the database."""
        try:
            films = self.session.query(Film).filter(Film.genre.like(f"%{genre}%")).all()
            return films
        except Exception as e:
            logging.error(f"Failed to retrieve films of genre {genre}: {e}")
            return []  # Return an empty list on error
    
    def get_film_by_id(self, film_id: str) -> Optional[Film]:
        """Retrieves a film by its ID."""
        try:
            film = self.session.query(Film).filter_by(film_id=film_id).first()
            return film
        except Exception as e:
            logging.error(f"Failed to retrieve film with ID {film_id}: {e}")
            return None  # Return None on error
        
        
    # Add method to create film.
    def create_film(self, name: str, genre: List[str], cast: List[str], 
                 description: str, age_rating: str, critic_rating: float, 
                 runtime: int, release_date: datetime, movie_poster: str = None) -> Film:
        """Creates a new film"""
        try:
            new_film = Film(
                name=name,
                genre=genre,
                cast=cast,
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
        if self.cinema is None:
            raise ValueError("Cinema must be set before adding a film.")
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
