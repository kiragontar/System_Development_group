# Seat Service Documentation

## Overview

The Seat Service handles operations related to cinema seats, including creating, retrieving, updating, and deleting seats.

## Class: `SeatService`

The `SeatService` class provides the following methods:

### `create_seat(screen_id, row_number, seat_number, seat_class)`

Creates a new seat.

**Parameters:**

-   `screen_id` (int): The ID of the screen.
-   `row_number` (int): The row number of the seat.
-   `seat_number` (int): The seat number.
-   `seat_class` (str): The class of the seat (e.g., "Lower Class", "Upper Class", "VIP").

**Returns:**

-   `Seat`: The newly created `Seat` object.

**Example:**
```python
from services.seat_service import SeatService
from models import Seat, Screen, City, Cinema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

seat_service = SeatService(session)

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

seat = seat_service.create_seat(screen_id=screen.screen_id, row_number=1, seat_number=1, seat_class="Lower Class")
print(f"Seat created: {seat.seat_id}")
```

### `delete_seat(seat_id)`
Deletes a seat by its ID.

**Parameters:**
- `seat_id` (int): The ID of the seat to delete.

**Returns:**
- `bool`: `True` if the seat was deleted, `False` if not found.

**Example:**
```python
seat_service = SeatService(session) # Assuming you have a database engine and session and that you have imported the modules.

deleted = seat_service.delete_seat(seat.seat_id)
if deleted:
    print("Seat deleted.")
else:
    print("Seat not found.")
```

### `get_seat_by_id(seat_id)`
Retrieves a seat by its ID.

**Parameters:**
- `seat_id` (int): The ID of the seat to retrieve.

**Returns:**
- `Seat`: The `Seat` object if found, or `None` if not found.

**Example:**
```python
# ... (imports and setup as in create_seat example) ...

found_seat = seat_service.get_seat_by_id(seat.seat_id)
if found_seat:
    print(f"Seat found: {found_seat.seat_id}")
else:
    print("Seat not found.")
```

### `get_all_seats_by_screen(screen_id)`
Retrieves all seats for a specific screen.

**Parameters:**
- `screen_id` (int): The ID of the screen.

**Returns:**
- `List[Seat]`: A list of `Seat` objects for the specified screen.

**Example:**
```python
# ... (imports and setup as in create_seat example) ...

seats = seat_service.get_all_seats_by_screen(screen_id=screen.screen_id)
for seat in seats:
    print(f"Seat: {seat.seat_id}, Row: {seat.row_number}, Seat: {seat.seat_number}, Class: {seat.seat_class}")
```

### `update_seat(seat_id, screen_id=None, row_number=None, seat_number=None, seat_class=None)`
Updates a seat by its ID.

**Parameters:**
- `seat_id` (int): The ID of the seat to update.
- `screen_id` (int, optional): The new screen ID.
- `row_number` (int, optional): The new row number.
- `seat_number` (int, optional): The new seat number.
- `seat_class` (str, optional): The new seat class.

**Returns:**
- `Seat`: The updated `Seat` object if found, or `None` if not found.

**Example:**
```python
# ... (imports and setup as in create_seat example) ...

updated_seat = seat_service.update_seat(seat_id=seat.seat_id, seat_class="VIP")
if updated_seat:
    print(f"Seat updated: {updated_seat.seat_id}, Class: {updated_seat.seat_class}")
else:
    print("Seat not found.")
```

### `update_seat_availability(seat_id, is_available)`
Updates a seat's availability.

**Parameters:**
- `seat_id` (int): The ID of the seat to update.
- `is_available` (bool): The new availability status (True or False).

**Returns:**
- `Seat`: The updated `Seat` object if found, or `None` if not found.

**Example:**
```python
# ... (imports and setup as in create_seat example) ...

updated_seat = seat_service.update_seat_availability(seat_id=seat.seat_id, is_available=False)
if updated_seat:
    print(f"Seat availability updated: {updated_seat.seat_id}, Available: {updated_seat.is_available}")
else:
    print("Seat not found.")
```

## Relationships
- **Screen**: A seat is associated with a specific screen.
- **Booking**: A seat can be associated with multiple bookings.
- **Ticket**: A seat is associated with a specific ticket.