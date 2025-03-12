import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, City, Cinema
from services.city_service import CityService

# Setup a test database
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
def city_service(session):
    return CityService(session)

@pytest.fixture
def create_test_data(session):
    # Create test City
    city = City(name="Test City", country="Test Country")
    session.add(city)
    session.commit()

    # create a second city.
    city2 = City(name = "second city", country = "second country")
    session.add(city2)
    session.commit()

    # Create test Cinema
    cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
    session.add(cinema)
    session.commit()

    return city, cinema, city2

# Test Cases:

def test_create_city(session, city_service):
    city = city_service.create_city(name="New City", country="New Country")
    assert city is not None
    assert city.name == "New City"
    assert city.country == "New Country"

def test_get_city_by_id(session, city_service, create_test_data):
    city = create_test_data[0]
    retrieved_city = city_service.get_city_by_id(city.city_id)
    assert retrieved_city is not None
    assert retrieved_city.city_id == city.city_id

def test_get_city_by_name(session, city_service, create_test_data):
    city = create_test_data[0]
    retrieved_city = city_service.get_city_by_name(city.name)
    assert retrieved_city is not None
    assert retrieved_city.name == city.name

def test_get_all_cities(session, city_service, create_test_data):
    cities = city_service.get_all_cities()
    assert len(cities) >= 2

def test_update_city(session, city_service, create_test_data):
    city = create_test_data[0]
    updated_city = city_service.update_city(city.city_id, name="Updated City")
    assert updated_city is not None
    assert updated_city.name == "Updated City"

def test_delete_city(session, city_service, create_test_data):
    city = create_test_data[0]
    result = city_service.delete_city(city.city_id)
    assert result is True
    assert city_service.get_city_by_id(city.city_id) is None
    

def test_get_cinemas_in_city(session, city_service, create_test_data):
    city = create_test_data[0]
    cinemas = city_service.get_cinemas_in_city(city.city_id)
    assert len(cinemas) == 1
    assert cinemas[0].city_id == city.city_id