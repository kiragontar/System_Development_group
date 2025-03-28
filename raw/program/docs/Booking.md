# Booking Service Documentation

## Overview

The Booking Service manages all booking-related operations within the Cinema Booking System Backend. It allows for the creation, retrieval, modification, cancellation, and placement of bookings, including seat selection, customer information, and payment status management. The price of the booking is calculated based on the selected seats and the city pricing.

## Class: `BookingService`

The `BookingService` class provides the following methods:

### `create_booking(screening_id, price, seats, customer_name, customer_email=None, customer_phone=None)`


Creates a new booking, calculating the total price based on the selected seats and city pricing.

**Parameters:**

-   `screening_id` (int): The ID of the screening for which the booking is made.
-   `price` (float): The total price of the booking.
-   `seats` (list): A list of `Seat` objects representing the selected seats.
-   `customer_name` (str): The name of the customer.
-   `customer_email` (str, optional): The email address of the customer.
-   `customer_phone` (str, optional): The phone number of the customer.

**Returns:**

-   `Booking`: The newly created `Booking` object.

**Raises:**

-   `InvalidScreeningError`: If the provided `screening_id` does not exist.
-   `NoSeatsSelectedError`: If the `seats` list is empty.

**Example (with price calculation using PricingService):**

```python
from services.booking_service import BookingService, InvalidScreeningError, NoSeatsSelectedError, BookingNotFoundError, BookingTimeoutError
from services.pricing_service import PricingService
from models.seat import Seat
from models.screening import Screening
from models.cinema import Cinema
from models.city import City
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo = True) 
SessionLocal = sessionmaker(bind=engine) 


# Assuming you have a Screening object and its related Cinema and City objects
screening = session.query(Screening).first()
cinema = session.query(Cinema).filter(Cinema.cinema_id == screening.cinema_id).first()
city = session.query(City).filter(City.city_id == cinema.city_id).first()

booking_service = BookingService(session)
pricing_service = PricingService(session)

seats = [Seat(screen_id="S1", row_number=1, seat_number=1, seat_class="upper"),
         Seat(screen_id="S1", row_number=1, seat_number=2, seat_class="upper")]

# Calculate price using PricingService
total_price = 0.0
for seat in seats:
    try:
        price = pricing_service.get_price(city.name, seat.seat_class, "Afternoon") # "Morning", "Afternoon", "Night"
        total_price += price
    except ValueError as e:
        print(f"Error calculating price: {e}")
        # Handle the error appropriately (e.g., skip the seat, raise an exception)

try:
    booking = booking_service.create_booking(
        screening_id=screening.screening_id,
        price=total_price,
        seats=seats,
        customer_name="John Doe",
        customer_email="john.doe@example.com",
        customer_phone="123-456-7890"
    )
    print(f"Booking created: {booking.booking_id}")
except InvalidScreeningError:
    print("Error: Invalid screening ID.")
except NoSeatsSelectedError:
    print("Error: No seats selected.")
```

### `get_all_booking()`
Retrieves all bookings.

**Returns:**
- `list[Booking]`: A list of all `Booking` objects.

**Example:**
```python
booking_service = BookingService(session) # Create booking service object, assuming u have a database engine and session. 
# And that u imported all that was above.

bookings = booking_service.get_all_bookings() # Retrieves all into a list
for booking in bookings: # Prints each booking from the list.
    print(booking.booking_id)
``` 

### `get_booking_by_id(booking_id)`
Retrieves a booking by its ID.

**Parameters:**
- `booking_id` (str): The ID of the booking to retrieve.

**Returns:**
- `Booking`: The `Booking` object if found.

**Raises:**
- `BookingNotFoundError`: If the booking with the provided `booking_id` does not exist.

**Example:**
```python
booking_service = BookingService(session) # Create booking service object, assuming u have a database engine and session. 
# And that u imported all that was above.

try:
    booking = booking_service.get_booking_by_id("some-booking-id")
    print(f"Booking found: {booking.booking_id}")
except BookingNotFoundError as e:
    print(e)
```

### `cancel_booking(booking_id)`
Cancels a booking by its ID.

**Parameters:**
- `booking_id` (str): The ID of the booking to cancel.

**Raises:**
- `BookingNotFoundError`: If the booking with the provided `booking_id` does not exist.

**Example:**
```python
booking_service = BookingService(session) # Create booking service object, assuming u have a database engine and session. 
# And that u imported all that was above.

try:
    booking_service.cancel_booking("some-booking-id")
    print("Booking cancelled.")
except BookingNotFoundError as e:
    print(e)
```

### `place_booking(booking_id, timeout_minutes=30)`
Checks timeout for pending bookings and handles FAILED status.

**Parameters:**
- `booking_id` (str): The ID of the booking to place.
- `timeout_minutes` (int, optional): The timeout in minutes for pending bookings. Defaults to 30.

**Return:**
- `bool`: `True` if the booking is within timeout or already paid, `False` if the booking has failed.

**Raises:**
- `BookingNotFoundError`: If the booking with the provided `booking_id` does not exist.
- `BookingTimeoutError`: If the booking has timed out.

**Example:**
```python
booking_service = BookingService(session) # Create booking service object, assuming u have a database engine and session. 
# And that u imported all that was above.

try:
    booking_service.place_booking("some-booking-id")
    print("Booking placed.")
except BookingNotFoundError as e:
    print(e)
except BookingTimeoutError as e:
    print(e)
```

## Relationships
- **Screening:** A booking is directly associated with a specific screening through the `screening_id` foreign key.
- **Seat:** A booking is directly associated with one or more seats through the `booking_seat_association` secondary table.
- **Payment:** A booking is directly associated with one or more payments through the `payments` relationship.
- **Ticket:** A booking is directly associated with one or more tickets through the `tickets` relationship.