# Ticket Service Documentation

## Overview

The Ticket Service manages the creation and retrieval of tickets. It interacts with the `Seat` and `PricingService` to create tickets with accurate pricing.

## Class: `TicketService`

The `TicketService` class provides the following methods:

### `create_ticket(booking_id, seat_id, screening_id, city, time_of_day, qr_code=None)`

Creates a new ticket.

**Parameters:**
-   `booking_id` (str): The ID of the booking associated with the ticket.
-   `seat_id` (int): The ID of the seat associated with the ticket.
-   `screening_id` (str): The ID of the screening associated with the ticket.
-   `city` (str): The city where the screening is taking place.
-   `time_of_day` (str): The time of day of the screening.
-   `qr_code` (str, optional): The QR code associated with the ticket.

**Returns:**

-   `Ticket`: The newly created `Ticket` object.

**Raises:**

-   `ValueError`: If the seat with the given `seat_id` is not found.

**Example:**

```python
from services.ticket_service import TicketService
from services.pricing_service import PricingService
from models import Seat, Ticket, Booking, Screening, City, Cinema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Assuming you have a PricingService instance
pricing_service = PricingService(session)

ticket_service = TicketService(session, pricing_service)

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

screening = Screening(screen_id=screen.screen_id, cinema_id=cinema.cinema_id, film_id = film.film_id, date = datetime.now().date(), start_time = datetime.now().time(), end_time = (datetime.now() + timedelta(hours=2)).time())
session.add(screen)
session.commit()

seat = Seat(screen_id=screen.screen_id, row_number=1, seat_number=1, seat_class="Lower Class")
session.add(seat)
session.commit()

#Create price
city_price = CityPricing(city = city.name, seat_class = seat.seat_class, time_of_day = "Evening", price = 15.0)
session.add(city_price)
session.commit()

# Calculate booking price
booking_price = pricing_service.get_price(city.name, seat.seat_class, "Evening")

booking = Booking(screening_id=screening.screening_id, price=booking_price, seats=[seat], customer_name="Test Customer")
session.add(booking)
session.commit()

try:
    ticket = ticket_service.create_ticket(
        booking_id=booking.booking_id,
        seat_id=seat.seat_id,
        screening_id=screening.screening_id,
        city=city.name,
        time_of_day="Evening",
        qr_code="some-qr-code"
    )
    print(f"Ticket created: {ticket.ticket_id}")
except ValueError as e:
    print(e)
```

### `get_ticket_by_id(ticket_id)`
Retrieves a ticket by its ID.

**Parameters:**
- `ticket_id` (int): The ID of the ticket to retrieve.

**Returns:**
- `Ticket`: The `Ticket` object if found, or `None` if not found.

**Example:**
```python
ticket_service = TicketService(session, pricing_service) # Assuming you have a database engine and session
# Assuming also that you have Imported all neccessary imports above.

ticket = ticket_service.get_ticket_by_id(1)  # Assuming ticket ID 1 exists
if ticket:
    print(f"Ticket found: {ticket.ticket_id}")
else:
    print("Ticket not found.")
```

### `get_tickets_by_booking(booking_id)`
Retrieves all tickets for a specific booking.

**Parameters:**
- `booking_id` (str): The ID of the booking.

**Returns:**
- `list[Ticket]`: A list of `Ticket` objects associated with the booking.

**Example:**
```python
# Assuming you have a PricingService instance
pricing_service = PricingService(session)

ticket_service = TicketService(session, pricing_service) # Assuming you have a database engine and session
# Assuming also that you have Imported all neccessary imports above.

tickets = ticket_service.get_tickets_by_booking(booking.booking_id)
for ticket in tickets:
    print(f"Ticket: {ticket.ticket_id}")
```

### `get_tickets_by_screening(screening_id)`
Retrieves all tickets for a specific screening.

**Parameters:**
- `screening_id` (str): The ID of the screening.

**Returns:**
- `list[Ticket]`: A list of `Ticket` objects associated with the screening.

**Example:**
```python
# Assuming you have a PricingService instance
pricing_service = PricingService(session)

ticket_service = TicketService(session, pricing_service)# Assuming you have a database engine and session
# Assuming also that you have Imported all neccessary imports above.

tickets = ticket_service.get_tickets_by_screening(screening.screening_id)
for ticket in tickets:
    print(f"Ticket: {ticket.ticket_id}")
```

## Relationships
- **Seat**:  A ticket is associated with a specific seat.
- **PricingService**:  The `TicketService` uses the `PricingService` to determine ticket prices.
- **Booking:** A ticket is associated with a specific booking.
- **Screening:** A ticket is associated with a specific screening.