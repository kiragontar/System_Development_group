import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role, Cinema, City  # Import necessary models
from services.user_service import UserService
from services.role_service import RoleService
from services.cinema_service import CinemaService
import bcrypt

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
def user_service(session):
    role_service = RoleService(session) 
    cinema_service = CinemaService(session)
    return UserService(session, role_service, cinema_service) 

@pytest.fixture
def role(session):
    role = Role(name="Test Role")
    session.add(role)
    session.commit()
    return role

@pytest.fixture
def city(session):
    city = City(name="Test City", country="Test Country")
    session.add(city)
    session.commit()
    return city

@pytest.fixture
def cinema(session,city):
    cinema = Cinema(name="Test Cinema", address='123 avenue', city_id=city.city_id) 
    session.add(cinema)
    session.commit()
    return cinema

def test_create_user(user_service, session, role, cinema):
    user = user_service.create_user(
        username="testuser",
        password="Password123!",
        firstname="Test",
        lastname="User",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    assert user.username == "testuser"
    assert user.firstname == "Test"
    assert user.lastname == "User"
    assert user.role_id == role.role_id
    assert user.cinema_id == cinema.cinema_id
    retrieved_user = session.query(User).filter_by(user_id=user.user_id).first()
    assert retrieved_user == user

def test_login_success(user_service, role, cinema):
    password = "Password123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User(
        username="testuser",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test",
        lastname="User",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user_service.session.add(user)
    user_service.session.commit()

    assert user_service.login("testuser", password) is True

def test_login_failure(user_service, role, cinema):
    password = "Password123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User(
        username="testuser",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test",
        lastname="User",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user_service.session.add(user)
    user_service.session.commit()

    assert user_service.login("testuser", "wrongpassword") is False
    assert user_service.login("wronguser", password) is False

def test_get_by_username(user_service, role, cinema):
    password = "Password123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User(
        username="testuser",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test",
        lastname="User",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user_service.session.add(user)
    user_service.session.commit()

    retrieved_user = user_service.get_by_username("testuser")
    assert retrieved_user == user

def test_get_by_user_id(user_service, role, cinema):
    password = "Password123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User(
        username="testuser",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test",
        lastname="User",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user_service.session.add(user)
    user_service.session.commit()

    retrieved_user = user_service.get_by_user_id(user.user_id)
    assert retrieved_user == user

def test_get_all(user_service, role, cinema):
    password = "Password123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user1 = User(
        username="testuser1",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test1",
        lastname="User1",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user2 = User(
        username="testuser2",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test2",
        lastname="User2",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user_service.session.add_all([user1, user2])
    user_service.session.commit()

    users = user_service.get_all()
    assert len(users) == 2

def test_get_all_at_cinema(user_service, role, cinema):
    password = "Password123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user1 = User(
        username="testuser1",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test1",
        lastname="User1",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user2 = User(
        username="testuser2",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test2",
        lastname="User2",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user_service.session.add_all([user1, user2])
    user_service.session.commit()

    users = user_service.get_all_at_cinema(cinema.cinema_id)
    assert len(users) == 2

def test_delete_user(user_service, role, cinema):
    password = "Password123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User(
        username="testuser",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test",
        lastname="User",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user_service.session.add(user)
    user_service.session.commit()

    assert user_service.delete_user(user.user_id) is True
    assert user_service.get_by_user_id(user.user_id) is None

def test_update_user(user_service, role, cinema, session):
    password = "Password123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User(
        username="testuser",
        password_hash=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
        firstname="Test",
        lastname="User",
        role_id=role.role_id,
        cinema_id=cinema.cinema_id
    )
    user_service.session.add(user)
    user_service.session.commit()

    new_role = Role(name="New Role")
    session.add(new_role)
    session.commit()

    new_cinema = Cinema(name="New Cinema", address='456 New St', city_id=cinema.city_id)
    session.add(new_cinema)
    session.commit()

    updated_user = user_service.update_user(
        user_id=user.user_id,
        username="updateduser",
        firstname="Updated",
        lastname="User",
        role_id=new_role.role_id,
        cinema_id=new_cinema.cinema_id
    )

    assert updated_user is not None
    assert updated_user.username == "updateduser"
    assert updated_user.firstname == "Updated"
    assert updated_user.role_id == new_role.role_id
    assert updated_user.cinema_id == new_cinema.cinema_id

def test_validate_password_requirements_success(user_service):
    """Test successful password validation."""
    assert user_service.validate_password_requirements("Password123!") is True

def test_validate_password_requirements_failure_short(user_service):
    """Test password too short."""
    assert user_service.validate_password_requirements("Short1!") is False

def test_validate_password_requirements_failure_no_digit(user_service):
    """Test password missing digit."""
    assert user_service.validate_password_requirements("Password!") is False

def test_validate_password_requirements_failure_no_special(user_service):
    """Test password missing special character."""
    assert user_service.validate_password_requirements("Password123") is False