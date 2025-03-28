# Screen Service Documentation

## Overview

The Screen Service handles operations related to cinema screens, including creating, retrieving, updating, and deleting screens, as well as checking screen availability.

## Class: `ScreenService`

The `ScreenService` class provides the following methods:

### `create_screen(screen_id, cinema_id, capacity_upper=0, capacity_lower=0, capacity_vip=0)`

Creates a new screen.

**Parameters:**

-   `screen_id` (str): The unique identifier for the screen.
-   `cinema_id` (int): The ID of the cinema to which the screen belongs.
-   `capacity_upper` (int, optional): The upper section seating capacity. Defaults to 0.
-   `capacity_lower` (int, optional): The lower section seating capacity. Defaults to 0.
-   `capacity_vip` (int, optional): The VIP seating capacity. Defaults to 0.

**Returns:**

-   `Screen`: The newly created `Screen` object.

**Example:**

```python
from services.screen_service import ScreenService
from models import Screen, Cinema, City
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

screen_service = ScreenService(session, screening_service=None) # screening_service is needed but not used for create_screen

# Create test data
city = City(name="London", country="UK")
session.add(city)
session.commit()

cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
session.add(cinema)
session.commit()

screen = screen_service.create_screen(screen_id="S1", cinema_id=cinema.cinema_id, capacity_upper=80, capacity_lower=30, capacity_vip=10)
print(f"Screen created: {screen.screen_id}")
```

### `get_screen_by_id(screen_id)`
Retrieves a screen by its ID.

**Parameters:**
- `screen_id` (str): The ID of the screen to retrieve.

**Returns:**
- `Optional[Screen]`: The `Screen` object if found, or `None` if not found.

**Example:**
```python
# ... (imports and setup as in create_screen example) ...

found_screen = screen_service.get_screen_by_id(screen_id="S1")
if found_screen:
    print(f"Screen found: {found_screen.screen_id}")
else:
    print("Screen not found.")
```

### `get_all_screens()`
Retrieves all screens.

**Returns:**
- `List[Screen]`: A list of all `Screen` objects.

**Example:**
```python
# ... (imports and setup as in create_screen example) ...

screens = screen_service.get_all_screens()
for screen in screens:
    print(f"Screen: {screen.screen_id}")
```

### `update_screen_capacities(screen_id, capacity_upper=None, capacity_lower=None, capacity_vip=None)`
Updates the seating capacities of a screen.

**Parameters:**
- `screen_id` (str): The ID of the screen to update.
- `capacity_upper` (int, optional): The new upper section seating capacity.
- `capacity_lower` (int, optional): The new lower section seating capacity.
- `capacity_vip` (int, optional): The new VIP seating capacity.

**Returns:**
- `Optional[Screen]`: The updated `Screen` object if found, or `None` if not found.

**Example:**
```python
# ... (imports and setup as in create_screen example) ...

updated_screen = screen_service.update_screen_capacities(screen_id="S1", capacity_upper=90)
if updated_screen:
    print(f"Screen capacities updated: {updated_screen.screen_id}, Upper: {updated_screen.capacity_upper}")
else:
    print("Screen not found.")
```

### `delete_screen(screen_id)`
Deletes a screen.

**Parameters:**
- `screen_id` (str): The ID of the screen to delete.
Returns:
- `bool`: `True` if the screen was deleted, `False` if not found.

**Example:**
```python
# ... (imports and setup as in create_screen example) ...

deleted = screen_service.delete_screen(screen_id="S1")
if deleted:
    print("Screen deleted.")
else:
    print("Screen not found.")
```

### `check_screen_in_use(screen_id, start_time, end_time)`
Checks if a screen is in use during a given time range.

**Parameters:**
- `screen_id` (str): The ID of the screen to check.
- `start_time` (datetime): The start time of the range.
- `end_time` (datetime): The end time of the range.

**Returns:**
- `bool`: `True` if the screen is in use, `False` otherwise.

**Example:**
```python
# ... (imports and setup as in create_screen example) ...
from datetime import datetime, timedelta

screening_service = ScreeningService(session) # create screening_service.

screen_service_with_screening = ScreenService(session, screening_service)

start_time = datetime.now()
end_time = start_time + timedelta(hours=2)

in_use = screen_service_with_screening.check_screen_in_use(screen_id="S1", start_time=start_time, end_time=end_time)
if in_use:
    print("Screen is in use.")
else:
    print("Screen is not in use.")
```

## Relationships
- **Cinema**: A screen belongs to a specific cinema.
- **Screening**: A screen can have multiple screenings.
- **Seat**: A screen can have multiple seats.