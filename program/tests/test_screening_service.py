import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Add parent directory to sys.path so python can search for services and models package.

from services.screening_service import ScreeningService
from models.screening import Screening
from models.screen import Screen
from models.film import Film
from datetime import datetime

# Setup a test database
DATABASE_URL = "sqlite:///:memory:"  # Use in-memory SQLite for testing, database exists only in RAM and is destroyed after testing.
engine = create_engine(DATABASE_URL) # Creates interface to database.
SessionLocal = sessionmaker(bind=engine) # Sessions are used to interact with database.

@pytest.fixture # Defines a fixture which is a function that sets up and tears down resources for testing.
def session():
    from models import Base
    Base.metadata.create_all(bind=engine) # Creates all the tables defined in the models in the in-memory database.
    session = SessionLocal() # Creates a new database session 
    yield session # Provides the session to the test function. The yield keyword makes it a generator, so the code after yield is executed after the test finishes.
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine) # Drops all tables cleaning database.

@pytest.fixture
def screening_service(session): # Creates an instance of the ScreeningService.
    return ScreeningService(session) # Passes in the session to the service. Makes service available to test functions.

@pytest.fixture
def create_test_data(session):  #Creates test data for the screen, and film tables.
    screen = Screen.create_screen(screen_id="S1", cinema_id=1, capacity_upper=80, capacity_lower=30, capacity_vip=10)
    film = Film(name="Action Movie", genre="Action", cast = "actor1, actor2", description = "movie description", age_rating = "12", critic_rating = 7.8, runtime = 120, release_date = datetime(2024,1,1))
    session.add_all([screen, film])  # Adds the data to the session, and commits the data.
    session.commit()
    return screen.screen_id, film.film_id # Returns the screen id, and the film id.

def test_create_screening(screening_service, session, create_test_data): # Pytest automatically discovers and runs this test function. screening_service, session and create_test_data are fixtures that pytest injects into the function.
    screen_id, film_id = create_test_data
    start_time = datetime(2024, 1, 1, 10, 0)
    end_time = datetime(2024, 1, 1, 12, 0)
    date = datetime(2024, 1, 1)
    lower_hall_sold_value = 10
    upper_hall_sold_value = 20
    vip_sold_value = 5

    screening = screening_service.create_screening(
        screen_id=screen_id,
        film_id=film_id,
        date=date,
        start_time=start_time,
        end_time=end_time,
        lower_hall_sold=lower_hall_sold_value,
        upper_hall_sold=upper_hall_sold_value,
        vip_sold=vip_sold_value
    )

    assert screening is not None
    assert isinstance(screening.screening_id, int)
    assert screening.screen_id == screen_id
    assert screening.film_id == film_id
    assert screening.date == date.date()
    #Convert the string from the screening object to a datetime object.
    converted_screening_time = datetime.strptime(screening.start_time, "%Y-%m-%d %H:%M:%S")
    assert converted_screening_time == start_time
    # Convert end_time string to datetime object
    converted_end_time = datetime.strptime(screening.end_time, "%Y-%m-%d %H:%M:%S")
    assert converted_end_time == end_time
    assert screening.lower_hall_sold == lower_hall_sold_value
    assert screening.upper_hall_sold == upper_hall_sold_value
    assert screening.vip_sold == vip_sold_value
