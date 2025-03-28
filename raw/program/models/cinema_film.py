from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


class CinemaFilm(Base):
    """Represents the association between a cinema and a film."""
    __tablename__ = 'cinema_film'

    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'), primary_key=True)
    film_id = Column(Integer, ForeignKey('films.film_id'), primary_key=True)

    cinema = relationship('Cinema', back_populates='cinema_films')
    film = relationship('Film', back_populates='cinema_films')

    def __init__(self, cinema_id: int, film_id: str):
        self.cinema_id = cinema_id
        self.film_id = film_id

    def __repr__(self):
        return f"<CinemaFilm(cinema_id={self.cinema_id}, film_id='{self.film_id}')>"