import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Screen, Cinema, City, Film
from services.screen_service import ScreenService
from services.screening_service import ScreeningService
from datetime import datetime, timedelta

# Setup a test database
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
def screening_service(session):
    return ScreeningService(session)

@pytest.fixture
def screen_service(session, screening_service):
    return ScreenService(session, screening_service)

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
def film(session): 
    film = Film(name="Test Film", genre="Test Genre", cast="Test Cast", description="Test Description", age_rating="12", critic_rating=7.5, runtime=120, release_date=datetime(2023, 1, 1))
    session.add(film)
    session.commit()
    return film

def test_create_screen(screen_service, session, cinema):
    screen = screen_service.create_screen("S1", cinema.cinema_id, 50, 30, 10)
    assert screen.screen_id == "S1"
    assert screen.cinema_id == cinema.cinema_id
    assert screen.capacity_upper == 50
    assert screen.capacity_lower == 30
    assert screen.capacity_vip == 10
    retrieved_screen = session.query(Screen).filter_by(screen_id="S1").first()
    assert retrieved_screen == screen

def test_get_screen_by_id(screen_service, session, cinema):
    screen = Screen.create_screen("S2", cinema.cinema_id, 80, 40, 10)
    session.add(screen)
    session.commit()
    retrieved_screen = screen_service.get_screen_by_id("S2")
    assert retrieved_screen == screen

def test_get_all_screens(screen_service, session, cinema):
    screen1 = Screen.create_screen("S3", cinema.cinema_id, 60, 30, 10)
    screen2 = Screen.create_screen("S4", cinema.cinema_id, 70, 20, 10)
    session.add_all([screen1, screen2])
    session.commit()
    screens = screen_service.get_all_screens()
    assert len(screens) == 2

def test_update_screen_capacities(screen_service, session, cinema):
    screen = Screen.create_screen("S5", cinema.cinema_id, 70, 35, 10)
    session.add(screen)
    session.commit()
    updated_screen = screen_service.update_screen_capacities("S5", capacity_upper=80, capacity_vip=20)
    assert updated_screen.capacity_upper == 80
    assert updated_screen.capacity_lower == 35
    assert updated_screen.capacity_vip == 20
    retrieved_screen = session.query(Screen).filter_by(screen_id="S5").first()
    assert retrieved_screen.capacity_upper == 80
    assert retrieved_screen.capacity_vip == 20

def test_delete_screen(screen_service, session, cinema):
    screen = Screen.create_screen("S6", cinema.cinema_id, 90, 45, 25)
    session.add(screen)
    session.commit()
    result = screen_service.delete_screen("S6")
    assert result is True
    deleted_screen = session.query(Screen).filter_by(screen_id="S6").first()
    assert deleted_screen is None

def test_check_screen_in_use(screen_service, session, cinema, screening_service, film):
    screen = Screen.create_screen("S7", cinema.cinema_id, 90, 45, 25)
    session.add(screen)
    session.commit()

    date = datetime(2023, 10, 26).date()  # Extract date
    start_time = datetime(2023, 10, 26, 10, 0, 0)
    end_time = datetime(2023, 10, 26, 12, 0, 0)
    screening_service.create_screening(
        screen.screen_id, film.film_id, date, start_time, end_time, 10, 20, 5
    ) 

    # Check if the screen is in use during the same time
    assert screen_service.check_screen_in_use(screen.screen_id, start_time, end_time) is True

    # Check if the screen is in use during a non-overlapping time
    new_start_time = datetime(2023, 10, 26, 13, 0, 0)
    new_end_time = datetime(2023, 10, 26, 15, 0, 0)
    assert screen_service.check_screen_in_use(screen.screen_id, new_start_time, new_end_time) is False

    # Check if a different screen is in use.
    assert screen_service.check_screen_in_use("S8", start_time, end_time) is False