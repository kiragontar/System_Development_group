# City Service Documentation

## Overview

The City Service handles operations related to city entities, including creating, retrieving, updating, and deleting cities, as well as retrieving cinemas within a city.

## Class: `CityService`

The `CityService` class provides the following methods:

### `create_city(name, country)`
Creates a new city.

**Parameters:**
- `name` (str): The name of the city.
- `country` (str): The country where the city is located.

**Returns:**
- `City`: The newly created `City` object.

**Example:**
```python
from services.city_service import CityService
from models import City, Cinema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

city_service = CityService(session)

city = city_service.create_city(name="London", country="UK")
print(f"City created: {city.city_id}")
```

### `get_city_by_id(city_id)`
Retrieves a city by its ID.

**Parameters:**
- `city_id` (int): The ID of the city to retrieve.

**Returns:**
`Optional[City]`: The `City` object if found, or `None` if not found.

**Example:**
```python
found_city = city_service.get_city_by_id(city.city_id)
if found_city:
    print(f"City found: {found_city.city_id}")
else:
    print("City not found.")
```

### `get_city_by_name(name)`
Retrieves a city by its name.

**Parameters:**
- `name` (str): The name of the city to retrieve.

**Returns:**
`Optional[City]`: The `City` object if found, or `None` if not found.

**Example:**
```python
found_city = city_service.get_city_by_name(name="London")
if found_city:
    print(f"City found by name: {found_city.city_id}")
else:
    print("City not found by name.")
```

### `get_all_cities()`
Retrieves all cities.

**Returns:**
- `List[City]`: A list of all `City` objects.

**Example:**
```python
cities = city_service.get_all_cities()
for city in cities:
    print(f"City: {city.city_id}, Name: {city.name}, Country: {city.country}")
```

### `update_city(city_id, name=None, country=None)`
Updates a city's name and/or country.

**Parameters:**
- `city_id` (int): The ID of the city to update.
- `name` (str, optional): The new name of the city.
- `country` (str, optional): The new country of the city.

**Returns:**
- `Optional[City]`: The updated `City` object if found, or `None` if not found.

**Example:**
```python
updated_city = city_service.update_city(city_id=city.city_id, name="Greater London")
if updated_city:
    print(f"City updated: {updated_city.city_id}, Name: {updated_city.name}")
else:
    print("City not found.")
```

### `delete_city(city_id)`
Deletes a city.

**Parameters:**

- `city_id` (int): The ID of the city to delete.

**Returns:**
- `bool`: `True` if the city was deleted, `False` if not found.

**Example:**
```python
deleted = city_service.delete_city(city.city_id)
if deleted:
    print("City deleted.")
else:
    print("City not found.")
```

### `get_cinemas_in_city(city_id)`
Retrieves all cinemas in a city.

**Parameters:**
- `city_id` (int): The ID of the city.

**Returns:**
- `List[Cinema]`: A list of `Cinema` objects in the city.

**Example:**
```python
cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
session.add(cinema)
session.commit()

cinemas = city_service.get_cinemas_in_city(city.city_id)
for cinema in cinemas:
    print(f"Cinema: {cinema.cinema_id}, Name: {cinema.name}")
```

## Relationships
- **Cinema**: A city can have multiple cinemas associated with it.

