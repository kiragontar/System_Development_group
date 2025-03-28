import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models.ticket import Ticket
from models.booking import Booking 
from models.seat import Seat
from models.city import City
from models.screening import Screening
from models.cinema import Cinema
from models.screen import Screen
from models.film import Film
from models.city_pricing import CityPricing
from services.ticket_service import TicketService
import datetime

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
def ticket_service(session):
    return TicketService(session)

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
    screen = Screen(screen_id="S1",cinema_id=cinema.cinema_id, capacity_upper=100, capacity_lower=50, capacity_vip=20)
    session.add(screen)
    session.commit()
    return screen

@pytest.fixture
def film(session):
    release_date = datetime.date(2023, 1, 1) #example date
    film = Film(
        name="Test Film",
        genre=["Action", "Adventure"],
        cast=["Actor 1", "Actress 2"],
        description="A test film description.",
        age_rating="PG-13",
        critic_rating=7.5,
        runtime=120,
        release_date=release_date,
        movie_poster="test_poster.jpg"
    )
    session.add(film)
    session.commit()
    return film

@pytest.fixture
def screening(session, screen, film):
    start_time = datetime.datetime(2024, 1, 1, 10, 0, 0)
    end_time = datetime.datetime(2024, 1, 1, 12, 0, 0)

    screening = Screening(
        screen_id=screen.screen_id,
        film_id=film.film_id,
        date=datetime.date(2024, 1, 1),
        start_time=start_time,
        end_time=end_time,
        lower_hall_sold=12,
        upper_hall_sold=20,
        vip_sold=3
    )
    session.add(screening)
    session.commit()
    return screening

@pytest.fixture
def booking(session, screening):
    booking = Booking(screening_id=screening.screening_id, price=20.0, seats=[], customer_name="Test Customer")
    session.add(booking)
    session.commit()
    return booking

@pytest.fixture
def seat(session, screen): # screen is now a dependency.
    seat = Seat(screen_id=screen.screen_id, row_number=1, seat_number=1, seat_class="Lower Class")
    session.add(seat)
    session.commit()
    return seat


def test_create_ticket(ticket_service, session, booking, seat, screening):
    # Make sure to set up the pricing service data to have the correct price.
    ticket = ticket_service.create_ticket(booking.booking_id, seat.seat_id, screening.screening_id, 10.0)
    assert ticket.booking_id == booking.booking_id
    assert ticket.seat_id == seat.seat_id
    assert ticket.screening_id == screening.screening_id
    assert ticket.original_ticket_price == 10.0
    retrieved_ticket = session.query(Ticket).filter_by(ticket_id=ticket.ticket_id).first()
    assert retrieved_ticket == ticket

def test_get_ticket_by_id(ticket_service, session, booking, seat, screening):
    ticket = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, original_ticket_price= 10.0)
    session.add(ticket)
    session.commit()
    retrieved_ticket = ticket_service.get_ticket_by_id(ticket.ticket_id)
    assert retrieved_ticket == ticket

def test_get_tickets_by_booking(ticket_service, session, booking, seat, screening):
    ticket1 = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, original_ticket_price= 10.0)
    ticket2 = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, original_ticket_price= 10.0)
    session.add_all([ticket1, ticket2])
    session.commit()
    tickets = ticket_service.get_tickets_by_booking(booking.booking_id)
    assert len(tickets) == 2

def test_get_tickets_by_screening(ticket_service, session, booking, seat, screening):
    ticket1 = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, original_ticket_price= 10.0)
    ticket2 = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, original_ticket_price= 10.0)
    session.add_all([ticket1, ticket2])
    session.commit()
    tickets = ticket_service.get_tickets_by_screening(screening.screening_id)
    assert len(tickets) == 2