from sqlalchemy import Column, Integer, String, Float
from . import Base


class CityPricing(Base):
    __tablename__ = 'city_pricing'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(255), nullable=False)
    seat_class = Column(String(255), nullable=False)
    time_of_day = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, city: str, seat_class: str, time_of_day: str, price: float):
        self.city = city
        self.seat_class = seat_class
        self.time_of_day = time_of_day
        self.price = price

        if price < 0:
            raise ValueError("Price cannot be negative.")