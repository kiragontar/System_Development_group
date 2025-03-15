# Cinema Service Documentation

## Overview

The Cinema Service handles operations related to cinema entities, including creating, retrieving, updating, and deleting cinemas, as well as managing cinema-related data like managers, admins, staff, screens, screenings, and films.

## Class: `CinemaService`

The `CinemaService` class provides the following methods:

### `create_cinema(name, address, city_id)`

Creates a new cinema.

**Parameters:**

- `name` (str): The name of the cinema.
- `address` (str): The address of the cinema.
- `city_id` (int): The ID of the city where the cinema is located.

**Returns:**

- `Cinema`: The newly created `Cinema` object.

**Example:**

```python
from services.cinema_service import CinemaService
from models import Cinema, City, Film, CinemaFilm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

cinema_service = CinemaService(session)

# Create test data
city = City(name="London", country="UK")
session.add(city)
session.commit()

cinema = cinema_service.create_cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
print(f"Cinema created: {cinema.cinema_id}")
```

### `get_cinema_by_id(cinema_id)`

Retrieves a cinema by its ID.

**Parameters:**

- `cinema_id` (int): The ID of the cinema to retrieve.

**Returns:**

- `Cinema`: The `Cinema` object if found, or `None` if not found.

**Example:**

```python
# ... (imports and setup as in create_cinema example) ...
found_cinema = cinema_service.get_cinema_by_id(cinema.cinema_id)
if found_cinema:
    print(f"Cinema found: {found_cinema.cinema_id}")
else:
    print("Cinema not found.")
```

### `get_all_cinemas()`

Retrieves all cinemas.

**Returns:**

- `List[Cinema]`: A list of all `Cinema` objects.

**Example:**

```python
# ... (imports and setup as in create_cinema example) ...
cinemas = cinema_service.get_all_cinemas()
for cinema in cinemas:
    print(f"Cinema: {cinema.cinema_id}, Name: {cinema.name}")
```

### `update_cinema(cinema_id, name=None, address=None, city_id=None)`

Updates a cinema's details.

**Parameters:**

- `cinema_id` (int): The ID of the cinema to update.
- `name` (str, optional): The new name of the cinema.
- `address` (str, optional): The new address of the cinema.
- `city_id` (int, optional): The new city ID.

**Returns:**

- `Cinema`: The updated `Cinema` object if found, or `None` if not found.

**Example:**

```python
# ... (imports and setup as in create_cinema example) ...
updated_cinema = cinema_service.update_cinema(cinema_id=cinema.cinema_id, name="Updated Cinema Name")
if updated_cinema:
    print(f"Cinema updated: {updated_cinema.cinema_id}, Name: {updated_cinema.name}")
else:
    print("Cinema not found.")
```

### `delete_cinema(cinema_id)`

Deletes a cinema.

**Parameters:**

- `cinema_id` (int): The ID of the cinema to delete.

**Returns:**

- `bool`: `True` if the cinema was deleted, `False` if not found.

**Example:**

```python
# ... (imports and setup as in create_cinema example) ...
deleted = cinema_service.delete_cinema(cinema.cinema_id)
if deleted:
    print("Cinema deleted.")
else:
    print("Cinema not found.")
```

### `get_managers(cinema_id)`

Retrieves managers for a cinema.

**Parameters:**

- `cinema_id` (int): The ID of the cinema.

**Returns:**

- `List[User]`: A list of `User` objects with the 'Manager' role.

**Example:**

```python
role = Role(name="Manager")
session.add(role)
session.commit()

user = User(username = "manager1", password_hash = "hashed_password", salt="random_salt", firstname="John", lastname="Doe", role_id = role.role_id, cinema_id = cinema.cinema_id)
session.add(user)
session.commit()

managers = cinema_service.get_managers(cinema.cinema_id)
for manager in managers:
    print(f"Manager: {manager.user_id}, Name: {manager.username}")
```

### `get_admins(cinema_id)`

Retrieves admins for a cinema.

**Parameters:**

- `cinema_id` (int): The ID of the cinema.

**Returns:**

- `List[User]`: A list of `User` objects with the 'Admin' role.

**Example:**

```python
role = Role(name="Admin")
session.add(role)
session.commit()

user = User(username = "admin1", password_hash = "hashed_password", salt="random_salt", firstname="Jane", lastname="Smith", role_id = role.role_id, cinema_id = cinema.cinema_id)
session.add(user)
session.commit()

admins = cinema_service.get_admins(cinema.cinema_id)
for admin in admins:
    print(f"Admin: {admin.user_id}, Name: {admin.username}")
```

### `get_staff(cinema_id)`

Retrieves staff for a cinema.

**Parameters:**

- `cinema_id` (int): The ID of the cinema.

**Returns:**

- `List[User]`: A list of `User` objects with the 'Staff' role.

**Example:**

```python
role = Role(name="Staff")
session.add(role)
session.commit()

user = User(username = "staff1", password_hash = "hashed_password", salt="random_salt", firstname="Alice", lastname="Johnson", role_id = role.role_id, cinema_id = cinema.cinema_id)
session.add(user)
session.commit()

staff = cinema_service.get_staff(cinema.cinema_id)
for staff_member in staff:
    print(f"Staff: {staff_member.user_id}, Name: {staff_member.username}")
```

### `get_screens(cinema_id)`

Retrieves screens for a cinema.

**Parameters:**

- `cinema_id` (int): The ID of the cinema.

**Returns:**

- `List[Screen]`: A list of `Screen` objects.

**Example:**

```python
screen = Screen(screen_id="S1", cinema_id=cinema.cinema_id, capacity_upper=80, capacity_lower=30, capacity_vip=10)
session.add(screen)
session.commit()

screens = cinema_service.get_screens(cinema.cinema_id)
for screen in screens:
    print(f"Screen: {screen.screen_id}")
```

### `get_screenings(cinema_id)`

Retrieves screenings for a cinema.

**Parameters:**

- `cinema_id` (int): The ID of the cinema.

**Returns:**

- `List[Screening]`: A list of `Screening` objects.

**Example:**

```python
screen = Screen(screen_id="S1", cinema_id=cinema.cinema_id, capacity_upper=80, capacity_lower=30, capacity_vip=10)
session.add(screen)
session.commit()

film = Film(name="Test Film", genre=["Action", "Sci-Fi"], cast=["Actor 1", "Actor 2"],
description="Test Description", age_rating="PG-13", critic_rating=7.5,
runtime=120, release_date=datetime(2024, 1, 1), movie_poster="poster.jpg")
session.add(film)
session.commit()

screening = Screening(screen_id = screen.screen_id, film_id = film.film_id, date = "2024-12-12", start_time = "10:00", end_time = "12:00")
session.add(screening)
session.commit()

screenings = cinema_service.get_screenings(cinema.cinema_id)
for screening in screenings:
    print(f"Screening: {screening.screening_id}")
```

### `get_films(cinema_id)`

Retrieves films for a cinema.

**Parameters:**

- `cinema_id` (int): The ID of the cinema.

**Returns:**

- `List[Film]`: A list of `Film` objects.

**Example:**

```python
film1 = Film(name="Film 1", genre=["Action", "Sci-Fi"], cast=["Actor 1", "Actor 2"],
description="Description 1", age_rating="PG-13", critic_rating=7.5,
runtime=120, release_date=datetime(2024, 1, 1), movie_poster="poster1.jpg")

film2 = Film(name="Film 2", genre=["Comedy"], cast=["Actor 3", "Actor 4"],
description="Description 2", age_rating="PG", critic_rating=8.0,
runtime=105, release_date=datetime(2024, 2, 15), movie_poster="poster2.jpg")

session.add_all([film1, film2])
session.commit()

cinema_film1 = CinemaFilm(cinema_id=cinema.cinema_id, film_id=film1.film_id)

cinema_film2 = CinemaFilm(cinema_id=cinema.cinema_id, film_id=film2.film_id)

session.add_all([cinema_film1, cinema_film2])
session.commit()

films = cinema_service.get_films(cinema.cinema_id)
for film in films:
    print(f"Film: {film.film_id}, Name: {film.name}")
```

### `get_cinemas_by_city(city_id)`

Retrieves cinemas by city.

**Parameters:**

- `city_id` (int): The ID of the city.

**Returns:**

- `List[Cinema]`: A list of `Cinema` objects.

**Example:**

```python
cinemas_in_city = cinema_service.get_cinemas_by_city(city.city_id)
for cinema_in_city in cinemas_in_city:
    print(f"Cinema: {cinema_in_city.cinema_id}, Name: {cinema_in_city.name}")
```

### `get_cinemas_by_film(film_id)`

Retrieves cinemas showing a specific film.

**Parameters:**

- `film_id` (int): The ID of the film.

**Returns:**

- `List[Cinema]`: A list of `Cinema` objects.

**Example:**

```python
cinema2 = cinema_service.create_cinema(name="Cinema 2", address="Address 2", city_id=city.city_id)

film = Film(name="Film 1", genre=["Action"], cast=["Actor 1"], description="Description 1", age_rating="PG13", critic_rating=8.0, runtime=120, release_date=datetime(2024, 12, 12), movie_poster = "poster.jpg")
session.add(film)
session.commit()

cinema_film1 = CinemaFilm(cinema_id=cinema.cinema_id, film_id=film.film_id)
cinema_film2 = CinemaFilm(cinema_id=cinema2.cinema_id, film_id=film.film_id)
session.add_all([cinema_film1, cinema_film2])
session.commit()

cinemas = cinema_service.get_cinemas_by_film(film.film_id)
for cinema in cinemas:
    print(f"Cinema: {cinema.cinema_id}, Name: {cinema.name}")
```

## Relationships

- **City:** A cinema belongs to a specific city.
- **CinemaFilm:** A cinema can have multiple films associated with it.
- **Screen:** A cinema can have multiple screens.
- **User:** A cinema can have multiple users associated with it (managers, admins, staff).
