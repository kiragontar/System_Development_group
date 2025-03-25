import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys
import os
program_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if program_path not in sys.path:
    sys.path.insert(0, program_path)  # Insert at the beginning
services_path = os.path.join(program_path, "services")
if services_path not in sys.path:
    sys.path.insert(0, services_path)
print(sys.path)
from models import Base
from models.booking import Booking
from models.screen import Screen
from models.film import Film
from models.seat import Seat
from models.screening import Screening
from models.city import City
from models.cinema import Cinema
from models.city_pricing import CityPricing
from enums import PaymentStatus 
from services.booking_service import BookingService, InvalidScreeningError, NoSeatsSelectedError, BookingNotFoundError # Import custom exceptions
from services.seat_service import SeatService
from services.ticket_service import TicketService
from services.pricing_service import PricingService 

import uuid

# Setup a test database
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost/testdb"  
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
def pricing_service(session):
    return PricingService(session) #Create instance of PricingService.

@pytest.fixture
def ticket_service(session):
    return TicketService(session)

@pytest.fixture
def seat_service(session):
    return SeatService(session)

@pytest.fixture
def booking_service(session, seat_service, pricing_service, ticket_service): # Creates an instance of the BookingService.
    return BookingService(session, seat_service, ticket_service, pricing_service) # Passes in the session to the service. Makes service available to test functions.


@pytest.fixture
def create_test_data(session, cinema):
    # Create test Screen
    screen = Screen(screen_id="S1", cinema_id=cinema.cinema_id, capacity_upper=80, capacity_lower=30, capacity_vip=10)
    session.add(screen)
    session.commit()

    # Create test film
    film = Film(name="Test Film", genre="Action", cast="Actor 1, Actor 2", description="Test Description", age_rating="12", critic_rating=7.5, runtime=120, release_date=datetime(2024, 1, 1))
    session.add(film)
    session.commit()

    # Create the CityPricing entries
    city_pricing_upper = CityPricing(
        city="Test City",
        seat_class="Upper",
        time_of_day="Afternoon",
        price=25.0
    )
    city_pricing_lower = CityPricing(
        city="Test City",
        seat_class="Lower",
        time_of_day="Afternoon",
        price=20.0
    )
    city_pricing_vip = CityPricing(
        city="Test City",
        seat_class="VIP",
        time_of_day="Afternoon",
        price=30.0
    )
    session.add_all([city_pricing_upper, city_pricing_lower, city_pricing_vip])
    session.commit()

    # Create test screening
    now = datetime.now()
    start_time = now
    end_time = now + timedelta(hours=2)

    screening = Screening(
        screen_id="S1",
        film_id=film.film_id,
        date=now.date(),
        start_time=start_time,
        end_time=end_time,
        lower_hall_sold=0,
        upper_hall_sold=0,
        vip_sold=0
    )
    session.add(screening)
    session.commit()

    #Create test seats
    seats = [
        Seat(screen_id='S1', row_number=1, seat_number=1, seat_class='Lower'),
        Seat(screen_id='S1', row_number=2, seat_number=2, seat_class='Upper'),
        Seat(screen_id='S1', row_number=3, seat_number=1, seat_class='Upper'),
        Seat(screen_id='S1', row_number=4, seat_number=2, seat_class='Lower'),
    ]
    for seat in seats:
        session.add(seat)
        session.commit()
        session.refresh(seat) # Force refresh

    return screening, seats

def test_create_booking_success(session, booking_service, create_test_data):  # Pytest automatically discovers and runs this test function. the arguments are fixtures that pytest injects into the function.
    screening, seats = create_test_data # Retreives the screening created and the two seats.
    # Calculate the expected price based on the provided seats and pricing service

    # Retrieve CityPricing records from the database
    city_pricing_upper = session.query(CityPricing).filter_by(seat_class='Upper').first()
    city_pricing_lower = session.query(CityPricing).filter_by(seat_class='Lower').first()
    city_pricing_vip = session.query(CityPricing).filter_by(seat_class="VIP").first()

    expected_price = 0.0
    for seat in seats:
        if seat.seat_class == 'Lower':
            expected_price += city_pricing_lower.price # From the city pricing fixture
        elif seat.seat_class == 'Upper':
            expected_price += city_pricing_upper.price # From the city pricing fixture
        elif seat.seat_class == "VIP":
            expected_price += city_pricing_vip.price

    customer_name = "John Doe"
    customer_email = "john.doe@example.com"
    customer_phone = "123-456-7890"

    booking = booking_service.create_booking(screening.screening_id, expected_price, seats, customer_name, customer_email, customer_phone)
    print(f"Test: Calculated booking price: {booking.price}, Expected: {expected_price}")
    assert booking is not None
    assert booking.screening_id == screening.screening_id
    assert booking.price == expected_price # Use calculated expected price
    assert booking.customer_name == customer_name
    assert booking.customer_email == customer_email
    assert booking.customer_phone == customer_phone
    assert len(booking.seats) == 4
    assert booking.payment_status == PaymentStatus.PENDING

    retrieved_booking = session.query(Booking).filter_by(booking_id=booking.booking_id).first()
    assert retrieved_booking is not None
    assert retrieved_booking.booking_id == booking.booking_id

def test_create_booking_invalid_screening(session, booking_service, create_test_data):
    _, seats = create_test_data
    invalid_screening_id = 999999
    price = 20.0
    customer_name = "John Doe"

    with pytest.raises(InvalidScreeningError): #Catch any exception that may be thrown.
        booking_service.create_booking(invalid_screening_id, price, seats, customer_name)

def test_create_booking_no_seats(session, booking_service, create_test_data):
    screening, _ = create_test_data
    price = 20.0
    customer_name = "John Doe"

    with pytest.raises(NoSeatsSelectedError):
        booking_service.create_booking(screening.screening_id, price, [], customer_name)

def test_get_all_bookings(session, booking_service, create_test_data):
    screening, seats = create_test_data
    booking1 = booking_service.create_booking(screening.screening_id, 20.0, seats, "John Doe")
    booking2 = booking_service.create_booking(screening.screening_id, 25.0, seats, "Jane Doe")

    all_bookings = booking_service.get_all_bookings()

    assert len(all_bookings) == 2
    assert booking1 in all_bookings
    assert booking2 in all_bookings

def test_get_booking_by_id(session, booking_service, create_test_data):
    screening, seats = create_test_data
    booking = booking_service.create_booking(screening.screening_id, 20.0, seats, "John Doe")

    retrieved_booking = booking_service.get_booking_by_id(booking.booking_id)

    assert retrieved_booking == booking

def test_cancel_booking(session, booking_service, create_test_data, seat_service):
    screening, seats = create_test_data
    booking = booking_service.create_booking(screening.screening_id, 20.0, seats, "John Doe")
    booking_id = booking.booking_id
    booking_service.cancel_booking(booking_id)

    canceled_booking = session.query(Booking).filter_by(booking_id=booking_id).first()
    assert canceled_booking.payment_status == PaymentStatus.Failed

    updated_seat1 = seat_service.get_seat_by_id(seats[0].seat_id)
    updated_seat2 = seat_service.get_seat_by_id(seats[1].seat_id)
    assert updated_seat1.is_available is True
    assert updated_seat2.is_available is True

    updated_screening = session.query(Screening).filter_by(screening_id=screening.screening_id).first()
    assert updated_screening.lower_hall_sold == 0
    assert updated_screening.upper_hall_sold == 0

def test_cancel_paid_booking(session, booking_service, create_test_data, seat_service):
    screening, seats = create_test_data
    booking = booking_service.create_booking(screening.screening_id, 20.0, seats, "John Doe")
    booking_id = booking.booking_id

    # Simulate a paid booking
    booking.payment_status = PaymentStatus.PENDING
    session.add(booking)
    session.commit()

    # Place the booking to increment the sold counts
    booking_service.place_booking(booking_id)
    updated_screening_after_place = session.query(Screening).filter_by(screening_id=screening.screening_id).first()

    # Call cancel_booking only once.
    booking_service.cancel_booking(booking_id)

    canceled_booking = session.query(Booking).filter_by(booking_id=booking.booking_id).first()
    assert canceled_booking.payment_status == PaymentStatus.REFUNDED

    updated_seat1 = seat_service.get_seat_by_id(seats[0].seat_id)
    updated_seat2 = seat_service.get_seat_by_id(seats[1].seat_id)
    assert updated_seat1.is_available is True
    assert updated_seat2.is_available is True

    updated_screening = session.query(Screening).filter_by(screening_id=screening.screening_id).first()
    assert updated_screening.lower_hall_sold == 0
    assert updated_screening.upper_hall_sold == 0

def test_cancel_booking_not_found(session, booking_service, create_test_data):
    with pytest.raises(BookingNotFoundError):
        booking_service.cancel_booking("nonexistent_booking_id")

def test_place_booking(session, booking_service, create_test_data, seat_service):
    screening, seats = create_test_data
    booking = booking_service.create_booking(screening.screening_id, 20.0, seats, "John Doe")
    booking_id = booking.booking_id

    assert booking_service.place_booking(booking_id) is True
    updated_seat1 = seat_service.get_seat_by_id(seats[0].seat_id)
    updated_seat2 = seat_service.get_seat_by_id(seats[1].seat_id)
    assert updated_seat1.is_available is False
    assert updated_seat2.is_available is False
    updated_screening = session.query(Screening).filter_by(screening_id=screening.screening_id).first()
    assert updated_screening.upper_hall_sold == 2

def test_place_booking_not_found(session, booking_service, create_test_data):
    with pytest.raises(BookingNotFoundError):
        booking_service.place_booking("nonexistent_booking_id")