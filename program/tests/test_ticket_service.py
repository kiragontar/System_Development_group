import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Ticket, Booking, Seat, Screening, CityPricing
from services.ticket_service import TicketService
from services.pricing_service import PricingService
import datetime

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
def pricing_service():
    return PricingService()

@pytest.fixture
def ticket_service(session, pricing_service):
    return TicketService(session, pricing_service)

@pytest.fixture
def booking(session):
    booking = Booking(screening_id=1, price=20.0, seats=[], customer_name="Test Customer")
    session.add(booking)
    session.commit()
    return booking

@pytest.fixture
def seat(session):
    seat = Seat(screen_id="S1", row_number=1, seat_number=1, seat_class="Lower Class")
    session.add(seat)
    session.commit()
    return seat

@pytest.fixture
def screening(session):
    screening = Screening(screen_id="S1", film_id=1, date= datetime.date(2024,1,1), start_time="2024-01-01 10:00:00", end_time="2024-01-01 12:00:00", lower_hall_sold=12, upper_hall_sold= 20, vip_sold= 3 )
    session.add(screening)
    session.commit()
    return screening

@pytest.fixture
def city_pricing(session):
    # Add price data for testing
    pricing = CityPricing(city="Test City", seat_class="Lower Class", time_of_day="Morning", price=10.0)
    session.add(pricing)
    session.commit()
    return pricing


def test_create_ticket(ticket_service, session, booking, seat, screening, city_pricing):
    # Make sure to set up the pricing service data to have the correct price.
    # I will assume the pricing service returns 10.0 for standard seats in the morning in test city.
    ticket = ticket_service.create_ticket(booking.booking_id, seat.seat_id, screening.screening_id, "Test City", "Morning" )
    assert ticket.booking_id == booking.booking_id
    assert ticket.seat_id == seat.seat_id
    assert ticket.screening_id == screening.screening_id
    assert ticket.ticket_price == 10.0
    retrieved_ticket = session.query(Ticket).filter_by(ticket_id=ticket.ticket_id).first()
    assert retrieved_ticket == ticket

def test_get_ticket_by_id(ticket_service, session, booking, seat, screening):
    ticket = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, ticket_price=10.0)
    session.add(ticket)
    session.commit()
    retrieved_ticket = ticket_service.get_ticket_by_id(ticket.ticket_id)
    assert retrieved_ticket == ticket

def test_get_tickets_by_booking(ticket_service, session, booking, seat, screening):
    ticket1 = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, ticket_price=10.0)
    ticket2 = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, ticket_price=10.0)
    session.add_all([ticket1, ticket2])
    session.commit()
    tickets = ticket_service.get_tickets_by_booking(booking.booking_id)
    assert len(tickets) == 2

def test_get_tickets_by_screening(ticket_service, session, booking, seat, screening):
    ticket1 = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, ticket_price=10.0)
    ticket2 = Ticket(booking_id=booking.booking_id, seat_id=seat.seat_id, screening_id=screening.screening_id, ticket_price=10.0)
    session.add_all([ticket1, ticket2])
    session.commit()
    tickets = ticket_service.get_tickets_by_screening(screening.screening_id)
    assert len(tickets) == 2