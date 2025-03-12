import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, CityPricing
from services.pricing_service import PricingService

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
def pricing_service(session):
    return PricingService(session)

def test_get_price(pricing_service, session):
    pricing = CityPricing(city="London", seat_class="Lower Class", time_of_day="Morning", price=10.0)
    session.add(pricing)
    session.commit()
    price = pricing_service.get_price("London", "Lower Class", "Morning")
    assert price == 10.0

def test_add_price(pricing_service, session):
    new_pricing = pricing_service.add_price("Paris", "Upper Class", "Afternoon", 15.0)
    assert new_pricing.city == "Paris"
    assert new_pricing.price == 15.0
    retrieved_pricing = session.query(CityPricing).filter_by(id=new_pricing.id).first()
    assert retrieved_pricing == new_pricing

def test_update_price(pricing_service, session):
    pricing = CityPricing(city="Tokyo", seat_class="VIP", time_of_day="Night", price=20.0)
    session.add(pricing)
    session.commit()
    updated_pricing = pricing_service.update_price(pricing.id, 25.0)
    assert updated_pricing.price == 25.0
    retrieved_pricing = session.query(CityPricing).filter_by(id=pricing.id).first()
    assert retrieved_pricing.price == 25.0

def test_delete_price(pricing_service, session):
    pricing = CityPricing(city="Berlin", seat_class="Economy", time_of_day="Morning", price=8.0)
    session.add(pricing)
    session.commit()
    result = pricing_service.delete_price(pricing.id)
    assert result is True
    deleted_pricing = session.query(CityPricing).filter_by(id=pricing.id).first()
    assert deleted_pricing is None