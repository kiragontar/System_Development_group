import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Payment, Booking, Seat, Screening, Film, Cinema
from services.payment_service import PaymentService
from enums import PaymentStatus
from datetime import datetime
import uuid

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
def payment_service(session):
    return PaymentService(session)

@pytest.fixture
def booking(session):
    cinema = Cinema(name="Test Cinema", address="Test Address", city_id=1)
    session.add(cinema)
    session.commit()

    film = Film(name="Test Film", genre=["Action"], cast=["Actor 1"], description="Test Description", age_rating="PG-13", critic_rating=7.5, runtime=120, release_date=datetime(2023, 1, 1), movie_poster="poster.jpg")
    session.add(film)
    session.commit()

    # Screening ID will be auto-generated
    screening = Screening(screen_id="1",film_id=film.film_id,date=datetime.now().date(),start_time="10:00",end_time="12:00",lower_hall_sold=0, upper_hall_sold=0,vip_sold=0 )
    session.add(screening)
    session.commit()

    seat = Seat(screen_id=1, row_number=1, seat_number=1, seat_class="Upper Class")
    session.add(seat)
    session.commit()

    booking = Booking(screening_id=screening.screening_id, price=10.0, seats=[seat], customer_name="Test Customer", customer_email="test@example.com", customer_phone="1234567890")
    session.add(booking)
    session.commit()

    return booking

def test_create_payment(session, payment_service, booking):
    payment = payment_service.create_payment(booking_id=booking.booking_id, payment_method="Credit Card", amount=10.0, transaction_id="12345")
    assert payment.booking_id == booking.booking_id
    assert payment.payment_method == "Credit Card"
    assert payment.amount == 10.0
    assert payment.transaction_id == "12345"
    assert payment.payment_status == PaymentStatus.PENDING

def test_update_payment_status(session, payment_service, booking):
    payment = payment_service.create_payment(booking_id=booking.booking_id, payment_method="Credit Card", amount=10.0)
    updated_payment = payment_service.update_payment_status(payment.payment_id, PaymentStatus.PAID, "54321")
    assert updated_payment.payment_status == PaymentStatus.PAID
    assert updated_payment.transaction_id == "54321"

def test_get_payment_by_id(session, payment_service, booking):
    payment = payment_service.create_payment(booking_id=booking.booking_id, payment_method="Credit Card", amount=10.0)
    retrieved_payment = payment_service.get_payment_by_id(payment.payment_id)
    assert retrieved_payment == payment

def test_get_payments_by_booking(session, payment_service, booking):
    payment1 = payment_service.create_payment(booking_id=booking.booking_id, payment_method="Credit Card", amount=10.0)
    payment2 = payment_service.create_payment(booking_id=booking.booking_id, payment_method="PayPal", amount=5.0)
    payments = payment_service.get_payments_by_booking(booking.booking_id)
    assert payment1 in payments
    assert payment2 in payments

def test_refund_payment(session, payment_service, booking):
    payment = payment_service.create_payment(booking_id=booking.booking_id, payment_method="Credit Card", amount=10.0)
    result = payment_service.refund_payment(payment.payment_id)
    assert result is True
    refunded_payment = payment_service.get_payment_by_id(payment.payment_id)
    assert refunded_payment.payment_status == PaymentStatus.REFUNDED