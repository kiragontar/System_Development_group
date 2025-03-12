import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Film, Cinema, CinemaFilm
from services.film_service import CinemaFilmService
from datetime import datetime

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def cinema(session):
    cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=1)
    session.add(cinema)
    session.commit()
    return cinema

@pytest.fixture
def cinema_film_service(session, cinema):
    return CinemaFilmService(cinema, session)

@pytest.fixture
def film(session):
    film = Film(name="Test Film", genre=["Action"], cast=["Actor 1"], description="Test Description", age_rating="PG-13", critic_rating=7.5, runtime=120, release_date=datetime(2023, 1, 1), movie_poster="poster.jpg")
    session.add(film)
    session.commit()
    return film

def test_add_film_to_cinema(session, cinema_film_service, film):
    cinema_film_service.add_film_to_cinema(film)
    assert film in cinema_film_service.get_all_films()

def test_remove_film_from_cinema(session, cinema_film_service, film):
    cinema_film_service.add_film_to_cinema(film)
    cinema_film_service.remove_film_from_cinema(film.film_id)
    assert film not in cinema_film_service.get_all_films()

def test_get_all_films_by_genre(session, cinema_film_service, film):
    cinema_film_service.add_film_to_cinema(film)
    films = cinema_film_service.get_all_films_by_genre("Action")
    assert film in films

def test_get_all_films_by_id(session, cinema_film_service, film):
    cinema_film_service.add_film_to_cinema(film)
    retrieved_film = cinema_film_service.get_all_films_by_id(film.film_id)
    assert retrieved_film == film