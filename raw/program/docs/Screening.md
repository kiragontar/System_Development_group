# Screening Service Documentation

## Overview

The Screening Service handles operations related to cinema screenings, including creating, retrieving, updating, and deleting screenings.

## Class: `ScreeningService`

The `ScreeningService` class provides the following methods:

### `create_screening(screen_id, film_id, date, start_time, end_time, lower_hall_sold=0, upper_hall_sold=0, vip_sold=0)`

Creates a new screening.

**Parameters:**
- `screen_id` (str): The ID of the screen.
- `film_id` (str): The ID of the film.
- `date` (datetime): The date of the screening.
- `start_time` (datetime): The start time of the screening.
- `end_time` (datetime): The end time of the screening.
- `lower_hall_sold` (int, optional): The number of lower hall seats sold. Defaults to 0.
- `upper_hall_sold` (int, optional): The number of upper hall seats sold. Defaults to 0.
- `vip_sold` (int, optional): The number of VIP seats sold. Defaults to 0.


**Returns:**

-   `Screening`: The newly created `Screening` object.

**Example:**

```python
from services.screening_service import ScreeningService
from models import Screening, Screen, Film, City, Cinema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

screening_service = ScreeningService(session)

# Create test data
city = City(name="London", country="UK")
session.add(city)
session.commit()

cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
session.add(cinema)
session.commit()

screen = Screen(screen_id="S1", cinema_id=cinema.cinema_id, capacity_upper=80, capacity_lower=30, capacity_vip=10)
session.add(screen)
session.commit()

film = Film(name="Test Film", genre="Action", cast="Actor 1, Actor 2", description="Test Description", age_rating="12", critic_rating=7.5, runtime=120, release_date=datetime(2024, 1, 1))
session.add(film)
session.commit()

start_time = datetime.now().time()
end_time = (datetime.now() + timedelta(hours=2)).time()

screening = screening_service.create_screening(
    screen_id=screen.screen_id, # Using screen ID
    film_id=film.film_id, # Using film ID
    date=datetime.now().date(),
    start_time=start_time,
    end_time=end_time,
    lower_hall_sold=10,
    upper_hall_sold=20,
    vip_sold=5
)
print(f"Screening created: {screening.screening_id}")
```

### `get_screening_by_id(screening_id)`
Retrieves a screening by ID.

**Parameters:**
- `screening_id` (str): The ID of the screening.

**Returns:**
- `Optional[Screening]`: The `Screening` object if found, or `None` if not found.

**Example:**
```python
screening_service = ScreeningService(session)

screening = screening_service.get_screening_by_id(1) # Assuming you have a database engine and session
# And assuming you have imported all neccessary modules above.
if screening:
    print(f"Screening found: {screening.screening_id}")
else:
    print("Screening not found.")
```

### `get_all_screenings()`
Retrieves all screenings.

**Returns:**
- `List[Screening]`: A list of all `Screening` objects.

**Example:**
```python
screening_service = ScreeningService(session) # Assuming you have a database engine and session
# And assuming you have imported all neccessary modules above.

screenings = screening_service.get_all_screenings()
for screening in screenings:
    print(f"Screening: {screening.screening_id}")
```

### `update_screening(screening_id, screen_id=None, film_id=None, date=None, start_time=None, end_time=None, lower_hall_sold=None, upper_hall_sold=None, vip_sold=None)`

**Parameters:**
- `screening_id` (str): The ID of the screening to update.
- `screen_id` (str, optional): The ID of the new screen.
- `film_id` (str, optional): The ID of the new film.
- `date` (datetime, optional): The new date.
- `start_time` (datetime, optional): The new start time.
- `end_time` (datetime, optional): The new end time.
- `lower_hall_sold` (int, optional): The newer number of lower hall seats sold.
- `upper_hall_sold` (int, optional): The newer number of upper hall seats sold.
- `vip_sold` (int, optional): The newer number of VIP seats sold. 

**Returns:**
- `Optional[Screening]`: The updated `Screening` object if found, or `None` if not found.

**Example:**
```python
screening_service = ScreeningService(session) # Assuming you have a database engine and session
# And assuming you have imported all neccessary modules above.

updated_screening = screening_service.update_screening(
    screening_id=2,
    lower_hall_sold=15
)
if updated_screening:
    print(f"Screening updated: {updated_screening.screening_id}")
else:
    print("Screening not found.")
```

### `delete_screening(screening_id)`
Deletes a screening.

**Parameters:**
- `screening_id` (str): The ID of the screening to delete.

**Returns:**
- `bool`: `True` if the screening was deleted, `False` if not found.

**Example:**
```python
screening_service = ScreeningService(session) # Assuming you have a database engine and session
# And assuming you have imported all neccessary modules above.

deleted = screening_service.delete_screening(2)
if deleted:
    print("Screening deleted.")
else:
    print("Screening not found.")
```

### `get_screenings_for_screen(screen_id)`
Retrieves all screenings for a given screen.

**Parameters:**
- `screen_id` (str): The ID of the screen.

**Returns:**
- `List[Screening]`: A list of `Screening` objects.

**Example:**
```python
screening_service = ScreeningService(session) # Assuming you have a database engine and session
# And assuming you have imported all neccessary modules above.

screens = screening_service.get_screenings_for_screen(screen=screen.screen_id)

for screen in screens:
    print(f"Screen: {screen.screen_id}")
```

### `get_screen_for_screening(screening_id)`
Retrieves the screen for a given screening.

**Parameters:**
- `screening_id` (str): The ID of the screening.

**Returns:**
- `Optional[Screen]`: The `Screen` object if found, or `None` if not found.

**Example:**
```python
screening_service = ScreeningService(session) # Assuming you have a database engine and session
# And assuming you have imported all neccessary modules above.

found_screen = screening_service.get_screen_for_screening(screening.screening_id)

if found_screen:
    print(f"Screen found: {found_screen.screen_id}")
else:
    print("Screen not found.")
```

## Relationships
- **Screen:** A screening is associated with a specific screen.
- **Film:** A screening is associated with a specific film.
- **Booking:** A screening can have multiple bookings.
- **Ticket:** A screening can have multiple tickets.