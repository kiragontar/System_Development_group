# Pricing Service Documentation

## Overview

The Pricing Service manages pricing information for cinema tickets based on city, seat class, and time of day. It provides methods to retrieve, add, update, and delete pricing data.

## Class: `PricingService`

The `PricingService` class provides the following methods:

### `get_price(city, seat_class, time_of_day)`

Retrieves the price based on city, seat class, and time of day.

**Parameters:**

- `city` (str): The name of the city.
- `seat_class` (str): The class of the seat (e.g., "Lower Class", "Upper Class", and "VIP").
- `time_of_day` (str): The time of day (e.g., "Morning", "Afternoon", "Evening").

**Returns:**

- `float`: The price of the ticket.

**Raises:**

- `ValueError`: If the price is not found for the given city, seat class, and time of day.

**Example:**
```python
from services.pricing_service import PricingService
from models import CityPricing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

pricing_service = PricingService(session)

try:
    price = pricing_service.get_price("London", "VIP", "Evening")
    print(f"Price: {price}")
except ValueError as e:
    print(e)
```

### `add_price(city, seat_class, time_of_day, price)`

Adds a new price entry.

**Parameters:**
- `city` (str): The name of the city.
- `seat_class` (str): The class of the seat.
- `time_of_day` (str): The time of day.
- `price` (float): The price of the ticket.

**Returns:**
- `CityPricing`: The newly created `CityPricing` object

**Example:**
```python
pricing_service = PricingService(session) # Assuming you have a database engine and session
# Assuming also that u have imported the modules neccessary above.

new_price = pricing_service.add_price("New York", "Lower", "Morning", 12.50)
print(f"New price added: {new_price.id}")
```

### `update_price(id, price)`
Updates the price for a given ID.

**Parameters:**
- `id` (int): The ID of the price entry to update.
- `price` (float): The new price.

**Return:**
- `CityPricing`: The updated `CityPricing` object, or `None` if the ID is not found.

**Example:**
```python
pricing_service = PricingService(session) # Assuming you have a database engine and session
# Assuming also that u have imported the modules neccessary above.

updated_price = pricing_service.update_price(1, 15.00)  # Assuming ID 1 exists
if updated_price:
    print(f"Price updated: {updated_price.id}")
else:
    print("Price ID not found.")
```

### `delete_price(id)`
Deletes a price entry by ID.

**Parameters:**
- `id` (int): The ID of the price entry to delete.

**Returns:**
- `bool`: `True` if the price entry was deleted, `False` if the ID was not found.

**Example:**
```python
pricing_service = PricingService(session) # Assuming you have a database engine and session
# Assuming also that u have imported the modules neccessary above.

deleted = pricing_service.delete_price(1)  # Assuming ID 1 exists
if deleted:
    print("Price deleted.")
else:
    print("Price ID not found.")
```

### `get_by_id(id)`
Retrieves a price entry by its ID.

**Parameters:**
- `id` (int): The ID of the price entry.

**Returns:**
- `CityPricing`: The `CityPricing` object if found, or `None` if not found.

**Example:**
```python
pricing_service = PricingService(session) # Assuming you have a database engine and session
# Assuming also that u have imported the modules neccessary above.

price_entry = pricing_service.get_by_id(1)  # Assuming ID 1 exists
if price_entry:
    print(f"Price entry found: {price_entry.id}, Price: {price_entry.price}")
else:
    print("Price entry not found.")
```

### `get_all()`
Retrieves all price entries.

**Returns:**
- `list[CityPricing]`: A list of all `CityPricing` objects.

**Example:**
```python
pricing_service = PricingService(session) # Assuming you have a database engine and session
# Assuming also that u have imported the modules neccessary above.

all_prices = pricing_service.get_all()
for price_entry in all_prices:
    print(f"Price entry: {price_entry.id}, City: {price_entry.city}, Price: {price_entry.price}")
```

## Relationships:
- **CityPricing**: The `PricingService` interacts with the `CityPricing` model to manage pricing data.
