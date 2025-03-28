import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import CityPricing


class PricingService:
    def __init__(self, session: Session):
        self.session = session

    def get_price(self, city: str, seat_class: str, time_of_day: str) -> float:
        """Retrieves the price based on city, seat class, and time of day."""
        if seat_class == "Lower Class":
            pricing = self.session.query(CityPricing).filter_by(
                city=city, seat_class="Lower Class", time_of_day=time_of_day
            ).first()
            if pricing:
                return pricing.price
            else:
                raise ValueError(
                    f"Price not found for city: {city}, seat class: {seat_class}, time: {time_of_day}"
                )
        elif seat_class == "Upper Class":
            lower_class_price = self.get_price(city, "Lower Class", time_of_day)
            return lower_class_price * 1.2

        elif seat_class == "VIP":
            upper_class_price = self.get_price(city, "Lower Class", time_of_day)
            return upper_class_price * 1.2
        
        else:
            raise ValueError(f"Invalid seat type: {seat_class}")

    def add_price(self, city: str, seat_class: str, time_of_day: str, price: float) -> CityPricing:
        new_price = CityPricing(city=city, seat_class=seat_class, time_of_day=time_of_day, price=price)
        self.session.add(new_price)
        self.session.commit()
        return new_price

    def update_price(self, id:int, price:float) -> CityPricing:
        price_object = self.session.query(CityPricing).filter(CityPricing.id == id).first()
        if price_object:
            price_object.price = price
            self.session.commit()
            return price_object
        return None

    def delete_price(self, id: int) -> bool:
        price_object = self.session.query(CityPricing).filter(CityPricing.id == id).first()
        if price_object:
            self.session.delete(price_object)
            self.session.commit()
            return True
        return False
    
    def get_by_id(self, id: int) -> CityPricing:
        """Retrieves a price entry by its ID."""
        return self.session.query(CityPricing).filter(CityPricing.id == id).first()
    
    def get_all(self) -> list[CityPricing]:
        """Retrieves all price entries."""
        return self.session.query(CityPricing).all()