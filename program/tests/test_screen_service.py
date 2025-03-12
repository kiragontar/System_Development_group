import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Screen, Cinema
from services.screen_service import ScreenService

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
def screen_service(session):
    return ScreenService(session)

@pytest.fixture
def cinema(session):
    cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=1)
    session.add(cinema)
    session.commit()
    return cinema

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

# the check screen in use function requires a screening service to be made.
# I will not add it in this test.