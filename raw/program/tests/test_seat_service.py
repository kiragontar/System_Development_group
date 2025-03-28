import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Seat, Screen, City, Cinema
from services.seat_service import SeatService


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
def seat_service(session):
    return SeatService(session)

@pytest.fixture
def city(session):
    city = City(name="Test City", country="Test Country")
    session.add(city)
    session.commit()
    return city

@pytest.fixture
def cinema(session, city):
    cinema = Cinema(name="Test Cinema", address='123 avenue', city_id=city.city_id)
    session.add(cinema)
    session.commit()
    return cinema

@pytest.fixture
def screen(session, cinema): 
    screen = Screen(screen_id="S1", cinema_id=cinema.cinema_id, capacity_upper=100, capacity_lower=50, capacity_vip=20)
    session.add(screen)
    session.commit()
    return screen


def test_create_seat(seat_service, session, screen):
    seat = seat_service.create_seat(screen.screen_id, 1, 1, "Upper Class")
    assert seat.screen_id == screen.screen_id
    assert seat.row_number == 1
    assert seat.seat_number == 1
    assert seat.seat_class == "Upper Class"
    retrieved_seat = session.query(Seat).filter_by(seat_id=seat.seat_id).first()
    assert retrieved_seat == seat

def test_delete_seat(seat_service, session, screen):
    seat = Seat(screen_id=screen.screen_id, row_number=2, seat_number=2, seat_class="VIP")
    session.add(seat)
    session.commit()
    result = seat_service.delete_seat(seat.seat_id)
    assert result is True
    deleted_seat = session.query(Seat).filter_by(seat_id=seat.seat_id).first()
    assert deleted_seat is None

def test_get_seat_by_id(seat_service, session, screen):
    seat = Seat(screen_id=screen.screen_id, row_number=3, seat_number=3, seat_class="VIP")
    session.add(seat)
    session.commit()
    retrieved_seat = seat_service.get_seat_by_id(seat.seat_id)
    assert retrieved_seat == seat

def test_get_all_seats_by_screen(seat_service, session, screen):
    seat1 = Seat(screen_id=screen.screen_id, row_number=4, seat_number=4, seat_class="Lower Class")
    seat2 = Seat(screen_id=screen.screen_id, row_number=5, seat_number=5, seat_class="VIP")
    session.add_all([seat1, seat2])
    session.commit()
    seats = seat_service.get_all_seats_by_screen(screen.screen_id)
    assert len(seats) == 2

def test_update_seat(seat_service, session, screen):
    seat = Seat(screen_id=screen.screen_id, row_number=6, seat_number=6, seat_class="Standard")
    session.add(seat)
    session.commit()
    updated_seat = seat_service.update_seat(seat.seat_id, row_number=7, seat_class="Premium")
    assert updated_seat.row_number == 7
    assert updated_seat.seat_class == "Premium"
    retrieved_seat = session.query(Seat).filter_by(seat_id=seat.seat_id).first()
    assert retrieved_seat.row_number == 7
    assert retrieved_seat.seat_class == "Premium"

def test_update_seat_availability(seat_service, session, screen):
    seat = Seat(screen_id=screen.screen_id, row_number=8, seat_number=8, seat_class="Standard")
    session.add(seat)
    session.commit()
    updated_seat = seat_service.update_seat_availability(seat.seat_id, False)
    assert updated_seat.is_available is False
    retrieved_seat = session.query(Seat).filter_by(seat_id=seat.seat_id).first()
    assert retrieved_seat.is_available is False