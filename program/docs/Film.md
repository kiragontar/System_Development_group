# Film Service Documentation

## Overview

The Film Service handles operations related to film entities, including retrieving films, adding or removing films from a cinema, and filtering films by genre or ID.

## Class: `CinemaFilmService`

The `CinemaFilmService` class provides the following methods:

### `get_all_films()`
Retrieves all films showing at the cinema.

**Returns:**
- `List[Film]`: A list of `Film` objects.

**Example:**
```python
from services.film_service import CinemaFilmService
from models import Film, Cinema, CinemaFilm, City
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Create test data
city = City(name="London", country="UK")
session.add(city)
session.commit()

cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
session.add(cinema)
session.commit()

film1 = Film(name="Film 1", genre=["Action", "Sci-Fi"], cast=["Actor 1", "Actor 2"],
description="Description 1", age_rating="PG-13", critic_rating=7.5,
runtime=120, release_date=datetime(2024, 1, 1), movie_poster="poster1.jpg")

film2 = Film(name="Film 2", genre=["Comedy"], cast=["Actor 3", "Actor 4"],
description="Description 2", age_rating="PG", critic_rating=8.0,
runtime=105, release_date=datetime(2024, 2, 15), movie_poster="poster2.jpg")

session.add_all([film1, film2])
session.commit()

cinema_film1 = CinemaFilm(cinema_id=cinema.cinema_id, film_id=film1.film_id)

cinema_film2 = CinemaFilm(cinema_id=cinema.cinema_id, 
film_id=film2.film_id)

session.add_all([cinema_film1, cinema_film2])
session.commit()

cinema_film_service = CinemaFilmService(cinema, session)

films = cinema_film_service.get_all_films()
for film in films:
    print(f"Film: {film.film_id}, Name: {film.name}")
```

### `get_all_films_by_genre(genre)`
Retrieves all films of a specific genre showing at the cinema.

**Parameters:**
- `genre` (str): The genre to filter by.

**Returns:**
- `List[Film]`: A list of `Film` objects matching the genre.

**Example:**
```python
found_film = cinema_film_service.get_all_films_by_id(film1.film_id)
if found_film:
    print(f"Film found: {found_film.film_id}, Name: {found_film.name}")
else:
    print("Film not found.")
```

### `add_film_to_cinema(film)`
Adds a film to the cinema.

**Parameters:**
- `film (Film)`: The Film object to add.

**Example:**
```python
film3 = Film(name="Film 3", genre=["Drama"], cast=["Actor 5"], description="Description 3", age_rating="R", critic_rating=8.5, runtime=130, release_date=datetime(2024, 3, 1), movie_poster="poster3.jpg")

session.add(film3)
session.commit()

cinema_film_service.add_film_to_cinema(film3)
print(f"Film '{film3.name}' added to cinema.")
```

### `remove_film_from_cinema(film_id)`
Removes a film from the cinema.

**Parameters:**

`film_id (int)`: The ID of the film to remove.

**Example:**
```python
cinema_film_service.remove_film_from_cinema(film2.film_id)
print(f"Film '{film2.name}' removed from cinema.")
```

### `update_film(film_id, name=None, genre=None, cast=None, description=None, age_rating=None, critic_rating=None, runtime=None, release_date=None, movie_poster=None)`
Updates a film's details.

**Parameters:**
- `film_id` (int): The ID of the film to update.
- `name` (str, optional): The new name of the film.
- `genre` (List[str], optional): The new genre of the film.
- `cast` (List[str], optional): The new cast of the film.
- `description` (str, optional): The new description of the film.
- `age_rating` (str, optional): The new age rating of the film.
- `critic_rating` (float, optional): The new critic rating of the film.
- `runtime` (int, optional): The new runtime of the film.
- `release_date` (datetime, optional): The new release date of the film.
- `movie_poster` (str, optional): The new movie poster file path or URL.

**Returns:**
- `Optional[Film]`: The updated `Film` object if found, or None if not found.

**Example:**
```python
updated_film = cinema_film_service.update_film(
    film_id=film1.film_id,
    name="Updated Film 1",
    genre=["Thriller"],
    cast=["Actor 6"],
    description="Updated Description 1",
    age_rating="R",
    critic_rating=8.5,
    runtime=135,
    release_date=datetime(2024, 4, 1),
    movie_poster="updated_poster1.jpg"
)
if updated_film:
    print(f"Film '{updated_film.name}' updated.")
else:
    print("Film not found.")
```

## Relationship
- **Screening**: A film can have multiple screenings
- **CinemaFilm**: A film can be associated with multiple cinemas