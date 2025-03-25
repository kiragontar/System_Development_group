from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, City, Cinema, Role
from backend.user_service import UserService

# Use pymysql with cryptography
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(engine)

# Create test data
city = City(name="Test City", country="Test Country")
session.add(city)
session.commit()

cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
session.add(cinema)
session.commit()

role = Role(name="Admin")
session.add(role)
session.commit()

# Test user operations
user_service = UserService(session)

new_user = user_service.create_user(
    username="testuser",
    password="SecurePass123!",
    firstname="Test",
    lastname="User",
    role_id=role.role_id
)

print(f"User created: {new_user is not None}")
print(f"Login test: {user_service.login('testuser', 'SecurePass123!')}")

session.close()