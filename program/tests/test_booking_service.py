import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Add parent directory to sys.path so python can search for services and models package.
from models import Base
from models.booking import Booking
from models.screen import Screen
from models.film import Film
from models.seat import Seat
from models.screening import Screening
from enums import PaymentStatus 
from services.booking_service import BookingService, InvalidScreeningError, NoSeatsSelectedError  # Import custom exceptions
import uuid

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
def booking_service(session): # Creates an instance of the BookingService.
    return BookingService(session) # Passes in the session to the service. Makes service available to test functions.

@pytest.fixture
def create_test_data(session):
    # Create test Screen
    screen = Screen(screen_id="S1", cinema_id=1, capacity_upper=80, capacity_lower=30, capacity_vip=10)
    session.add(screen)
    session.commit()

    # Create test film
    film = Film(name="Test Film", genre="Action", cast="Actor 1, Actor 2", description="Test Description", age_rating="12", critic_rating=7.5, runtime=120, release_date=datetime(2024, 1, 1))
    session.add(film)
    session.commit()

    # Create test screening
    now = datetime.now()
    start_time_str = now.time().strftime("%H:%M:%S")  # Convert to string for SQLite
    end_time_str = (now + timedelta(hours=2)).time().strftime("%H:%M:%S")  # Convert to string

    screening = Screening(
        screen_id="S1",
        film_id=film.film_id,
        date=now.date(),
        start_time=start_time_str,  # Use the string
        end_time=end_time_str,  # Use the string
        lower_hall_sold=0,
        upper_hall_sold=0,
        vip_sold=0
    )
    session.add(screening)
    session.commit()

    #Create test seats
    seat1 = Seat(screen_id="S1", row_number=1, seat_number=50, seat_class="upper")
    seat2 = Seat(screen_id="S1", row_number=1, seat_number=51, seat_class="upper")
    session.add_all([seat1, seat2])
    session.commit()

    return screening, [seat1, seat2]


def test_create_booking_success(session, booking_service, create_test_data):  # Pytest automatically discovers and runs this test function. the arguments are fixtures that pytest injects into the function.
    screening, seats = create_test_data # Retreives the screening created and the two seats.
    price = 20.0 
    customer_name = "John Doe"
    customer_email = "john.doe@example.com"
    customer_phone = "123-456-7890"

    booking = booking_service.create_booking(screening.screening_id, price, seats, customer_name, customer_email, customer_phone)

    assert booking is not None
    assert booking.screening_id == screening.screening_id
    assert booking.price == price
    assert booking.customer_name == customer_name
    assert booking.customer_email == customer_email
    assert booking.customer_phone == customer_phone
    assert len(booking.seats) == 2
    assert booking.payment_status == PaymentStatus.PENDING

    # Verify booking exists in the database
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