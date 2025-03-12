import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Cinema, City, User, Role
from services.cinema_service import CinemaService
import bcrypt

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
def cinema_service(session):
    return CinemaService(session)

@pytest.fixture
def create_test_data(session):
    # Create test City
    city = City(name="Test City", country="United Kingdom")
    session.add(city)
    session.commit()

    # Create test Cinema
    cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
    session.add(cinema)
    session.commit()

    # Create test Users and Roles for relationship tests.
    admin_role = Role(name="Admin")
    manager_role = Role(name="Manager")
    staff_role = Role(name="Staff")
    session.add_all([admin_role, manager_role, staff_role])
    session.commit()

    # Generate password hash and salt using bcrypt
    password = "testpassword"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    admin_user = User(username="admin", password_hash=hashed_password.decode('utf-8'), salt=salt.decode('utf-8'), firstname="admin", lastname="user", role_id=admin_role.role_id, cinema_id=cinema.cinema_id)
    manager_user = User(username="manager", password_hash=hashed_password.decode('utf-8'), salt=salt.decode('utf-8'), firstname="manager", lastname="user", role_id=manager_role.role_id, cinema_id=cinema.cinema_id)
    staff_user = User(username="staff", password_hash=hashed_password.decode('utf-8'), salt=salt.decode('utf-8'), firstname="staff", lastname="user", role_id=staff_role.role_id, cinema_id=cinema.cinema_id)

    session.add_all([admin_user, manager_user, staff_user])
    session.commit()

    return cinema, city, admin_user, manager_user, staff_user

# Test Cases:

def test_create_cinema(session, cinema_service, create_test_data):
    city = create_test_data[1]
    cinema = cinema_service.create_cinema(name="New Cinema", address="456 New Ave", city_id=city.city_id)
    assert cinema is not None
    assert cinema.name == "New Cinema"
    assert cinema.address == "456 New Ave"
    assert cinema.city_id == city.city_id

def test_get_cinema_by_id(session, cinema_service, create_test_data):
    cinema = create_test_data[0]
    retrieved_cinema = cinema_service.get_cinema_by_id(cinema.cinema_id)
    assert retrieved_cinema is not None
    assert retrieved_cinema.cinema_id == cinema.cinema_id

def test_get_all_cinemas(session, cinema_service, create_test_data):
    cinemas = cinema_service.get_all_cinemas()
    assert len(cinemas) >= 1

def test_update_cinema(session, cinema_service, create_test_data):
    cinema = create_test_data[0]
    updated_cinema = cinema_service.update_cinema(cinema.cinema_id, name="Updated Cinema")
    assert updated_cinema is not None
    assert updated_cinema.name == "Updated Cinema"

def test_delete_cinema(session, cinema_service, create_test_data):
    cinema = create_test_data[0]
    result = cinema_service.delete_cinema(cinema.cinema_id)
    assert result is True
    assert cinema_service.get_cinema_by_id(cinema.cinema_id) is None

def test_get_managers(session, cinema_service, create_test_data):
    cinema, _, _, manager, _ = create_test_data
    managers = cinema_service.get_managers(cinema.cinema_id)
    assert len(managers) == 1
    assert managers[0].user_id == manager.user_id

def test_get_admins(session, cinema_service, create_test_data):
    cinema, _, admin, _, _ = create_test_data
    admins = cinema_service.get_admins(cinema.cinema_id)
    assert len(admins) == 1
    assert admins[0].user_id == admin.user_id

def test_get_staff(session, cinema_service, create_test_data):
    cinema, _, _, _, staff = create_test_data
    staff_members = cinema_service.get_staff(cinema.cinema_id)
    assert len(staff_members) == 1
    assert staff_members[0].user_id == staff.user_id