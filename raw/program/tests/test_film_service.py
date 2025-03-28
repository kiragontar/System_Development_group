import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Film, Cinema, CinemaFilm, City
from services.film_service import CinemaFilmService
from datetime import datetime

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost/testdb"
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
def city(session): 
    city = City(name="Test City", country="Test Country")
    session.add(city)
    session.commit()
    return city

@pytest.fixture
def cinema(session, city):
    cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
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

def test_update_film(session, cinema_film_service, film):
    cinema_film_service.add_film_to_cinema(film)
    updated_film = cinema_film_service.update_film(
        film_id=film.film_id,
        name="Updated Test Film",
        genre=["Sci-Fi"],
        cast=["Actor 2"],
        description="Updated Description",
        age_rating="R",
        critic_rating=8.0,
        runtime=130,
        release_date=datetime(2023, 2, 1),
        movie_poster="updated_poster.jpg"
    )
    assert updated_film is not None
    assert updated_film.name == "Updated Test Film"
    assert updated_film.get_genre() == ["Sci-Fi"]
    assert updated_film.get_cast() == ["Actor 2"]
    assert updated_film.description == "Updated Description"
    assert updated_film.age_rating == "R"
    assert updated_film.critic_rating == 8.0
    assert updated_film.runtime == 130
    assert updated_film.release_date == datetime(2023, 2, 1)
    assert updated_film.movie_poster == "updated_poster.jpg"