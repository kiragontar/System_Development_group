from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from . import Base
from typing import List
from datetime import datetime

class Film(Base):
    """
    Represents a film with attributes such as title, genre, cast, and ratings.
    This class provides methods to access and modify film details.
    """
    __tablename__ = 'films'

    film_id = Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier for the film
    name = Column(String(255), nullable=False)  # Name of the film
    genre = Column(String(255), nullable=False)  # Genres of the film stored as a single string.
    cast = Column(String(255), nullable=False)  # List of cast members stored as a single string
    description = Column(String(255), nullable=False)  # Brief description of the film
    age_rating = Column(String(255), nullable=False)  # Age restriction (e.g., PG-13, R)
    critic_rating = Column(Float, nullable=False)  # Critic rating (e.g., IMDb or Rotten Tomatoes score)
    runtime = Column(Integer, nullable=False)  # Runtime in minutes
    release_date = Column(DateTime, nullable=False)  # Date when the film was released
    movie_poster = Column(String(255), nullable=True)  # file path for the movie poster

    # Relationship with screenings (one film can have multiple screenings)
    screenings = relationship('Screening', back_populates='film')
    cinema_films = relationship('CinemaFilm', back_populates='film')

    def __init__(self, name: str, genre: List[str], cast: List[str], 
                 description: str, age_rating: str, critic_rating: float, 
                 runtime: int, release_date: datetime, movie_poster: str = None):
        """
        Initializes a Film object with provided attributes.
        
        Parameters:
        - film_id (int): Auto incremented so no need to include it
        - name (str): Title of the film.
        - genre (List[str]): List of Genres of the film.
        - cast (List[str]): List of cast members.
        - description (str): Short description of the film.
        - age_rating (str): Age restriction of the film.
        - critic_rating (float): Rating given by critics.
        - runtime (int): Duration of the film in minutes.
        - release_date (datetime): Date when the film was released.
        - movie_poster (str, optional): file path of the movie poster.
        """
        self.name = name
        self.genre = ','.join(genre)
        self.cast = ','.join(cast)  # Convert list to a comma-separated string
        self.description = description
        self.age_rating = age_rating
        self.critic_rating = critic_rating
        self.runtime = runtime
        self.release_date = release_date
        self.movie_poster = movie_poster

    def get_id(self) -> int:
        """Returns the unique film ID."""
        return self.film_id

    def get_name(self) -> str:
        """Returns the film's name."""
        return self.name

    def get_genre(self) -> List[str]:
        """Returns the film's genres as a list of strings"""
        return self.genre.split(',')

    def get_cast(self) -> List[str]:
        """Returns the cast as a list of names."""
        if self.cast:
            return [member.strip() for member in self.cast.split(',')]
        else:
            return []

    def get_description(self) -> str:
        """Returns the film's description."""
        return self.description

    def get_age_rating(self) -> str:
        """Returns the film's age rating."""
        return self.age_rating

    def get_critic_rating(self) -> float:
        """Returns the film's critic rating."""
        return self.critic_rating

    def get_runtime(self) -> int:
        """Returns the film's runtime in minutes."""
        return self.runtime

    def get_release_date(self) -> datetime:
        """Returns the film's release date."""
        return self.release_date

    def get_movie_poster(self) -> str:
        """Returns the file path or URL of the movie poster."""
        return self.movie_poster
    
    def set_name(self, name: str) -> None:
        """Updates the film's name."""
        if name:
            self.name = name
        else:
            raise ValueError("Name cannot be empty.")
        
    def set_genre(self, genre: List[str]) -> None:
        """Updates the film's genre."""
        if genre:
            self.genre = ','.join(genre)
        else:
            raise ValueError("Genre cannot be empty")
    def set_cast(self, new_cast: List[str]) -> None:
        """
        Updates the cast of the film.
        
        Parameters:
        - new_cast (List[str]): List of new cast members.
        """
        if new_cast:
            self.cast = ','.join(new_cast)
        else:
            raise ValueError("Cast cannot be empty.")
        
    def set_description(self, description: str) -> None:
        """Updates the film's description."""
        if description:
            self.description = description
        else:
            raise ValueError("Description cannot be empty.")
        
    def set_age_rating(self, age_rating: str) -> None:
        """Updates the film's age rating."""
        if age_rating:
            self.age_rating = age_rating
        else:
            raise ValueError("Age rating cannot be empty.")

    def set_critic_rating(self, critic_rating: float) -> None:
        """Updates the film's critic rating."""
        if critic_rating >= 0:
            self.critic_rating = critic_rating
        else:
            raise ValueError("Critic Rating cannot be negative.")
        
    def set_runtime(self, runtime: int) -> None:
        """Updates the film's runtime in minutes."""
        if runtime >= 0:
            self.runtime = runtime
        else:
            raise ValueError("Runtime cannot be negative.")
        
    def set_release_date(self, release_date: datetime) -> None:
        """Updates the film's release date."""
        if release_date:
            self.release_date = release_date
        else:
            raise ValueError("Release date cannot be empty.")
        
    def set_movie_poster(self, movie_poster: str) -> None:
        """Updates the film's movie poster file path or URL."""
        if movie_poster:
            self.movie_poster = movie_poster
        else:
            raise ValueError("Movie poster cannot be empty.")
        
    def create_genre(self, new_genre: str) -> None:
        """Adds a new genre to the film."""
        genres = self.get_genre()
        new_genre = new_genre.strip()
        if new_genre not in genres:
            genres.append(new_genre)
            self.set_genre(genres)
    
    def delete_genre(self, genre_to_remove: str) -> None:
        """Removes a specific genre from the film."""
        genres = self.get_genre()
        genre_to_remove = genre_to_remove.strip()
        if genre_to_remove in genres:
            genres.remove(genre_to_remove)
            self.set_genre(genres)
    
    def __repr__(self):
        return f"<Film(film_id='{self.film_id}', name='{self.name}', genre='{self.genre}', cast='{self.cast}')>"