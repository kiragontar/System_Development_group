# User Service Documentation

## Overview

The User Service manages user-related operations, including authentication, user creation, retrieval, and deletion. It also handles password validation and role management.

## Class: `UserService`

The `UserService` class provides the following methods:

### `login(username, password)`

Authenticates a user based on their username and password.

**Parameters:**

- `username` (str): The username of the user.
- `password` (str): The password of the user.

**Returns:**

- `bool`: `True` if the user exists and the password matches, otherwise `False`.

**Example:**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role, Cinema, City
from services.user_service import UserService
from services.role_service import RoleService
from services.cinema_service import CinemaService
from datetime import datetime

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Create test data
city = City(name="Test City", country="Test Country")
session.add(city)
session.commit()

cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
session.add(cinema)
session.commit()

role = Role(name="Admin")
session.add(role)
session.commit()

role_service = RoleService(session)
cinema_service = CinemaService(session)

user_service = UserService(session, role_service, cinema_service)

# Assuming you have a user with username 'testuser' and password 'password123'
is_logged_in = user_service.login("testuser", "password123")
print(f"Login successful: {is_logged_in}")
```

### `create_user(username, password, firstname, lastname, role_id, cinema_id=None)`

Creates a new user, assigns them a role, and optionally associates them with a cinema.

**Parameters:**

- `username` (str): The username of the new user.
- `password` (str): The password of the new user.
- `firstname` (str): The first name of the new user.
- `lastname` (str): The last name of the new user.
- `role_id` (int): The ID of the role to assign to the user.
- `cinema_id` (int, optional): The ID of the cinema to associate the user with.

**Returns:**

- `User`: The newly created `User` object.

**Example:**

```python
new_user = user_service.create_user(
    username="newuser",
    password="SecurePassword1!",
    firstname="New",
    lastname="User",
    role_id=role.role_id,
    cinema_id=cinema.cinema_id
)
print(f"New user created: {new_user.username}")
```

### `get_by_user_id(user_id)`

Retrieves a user by their user ID.

**Parameters:**

- `user_id` (int): The ID of the user to retrieve.

**Returns:**

- `Optional[User]`: The `User` object if found, or `None` if not found.

**Example:**

```python
user = user_service.get_by_user_id(new_user.user_id)
if user:
    print(f"User found: {user.username}")
else:
    print("User not found.")
```

### `get_by_username(username)`

Retrieves a user by their username.

**Parameters:**

- `username` (str): The username of the user to retrieve.

**Returns:**

- `Optional[User]`: The `User` object if found, or `None` if not found.

**Example:**

```python
user = user_service.get_by_username("newuser")
if user:
    print(f"User found: {user.username}")
else:
    print("User not found.")
```

### `get_all()`

Retrieves all users.

**Returns:**

- `List[User]`: A list of all `User` objects.

**Example:**

```python
users = user_service.get_all()
for user in users:
    print(f"User: {user.username}")
```

### `get_all_at_cinema(cinema_id)`

Retrieves all users associated with a specific cinema.

**Parameters:**

- `cinema_id` (int): The ID of the cinema.

**Returns:**

- `List[User]`: A list of `User` objects associated with the cinema.

**Example:**

```python
users = user_service.get_all_at_cinema(cinema.cinema_id)
for user in users:
    print(f"User at cinema: {user.username}")
```

### `delete_user(user_id)`

Deletes a user by their user ID.

**Parameters:**

- `user_id` (int): The ID of the user to delete.

**Returns:**

- `bool`: `True` if the user was deleted, `False` otherwise.

**Example:**

```python
is_deleted = user_service.delete_user(new_user.user_id)
print(f"User deleted: {is_deleted}")
```

### `validate_password_requirements(password)`

Validates that the password meets required security standards.

**Parameters:**

- `password` (str): The password string to be validated.

**Returns:**

- `bool`: `True` if the password meets the requirements, otherwise `False`.

**Example:**

```python
user_input_password = "UserEnteredPassword123!"
is_valid = user_service.validate_password_requirements(user_input_password)
print(f"Password valid: {is_valid}")
```

### `update_user(user_id, username=None, firstname=None, lastname=None, role_id=None, cinema_id=None)`

Updates a user's details.

**Parameters:**

- `user_id` (int): The ID of the user to update.
- `username` (str, optional): The new username.
- `firstname` (str, optional): The new first name.
- `lastname`(str, optional): The new last name.
- `role_id` (int, optional): The new role ID.
- `cinema_id` (int, optional): The new cinema ID.

**Returns:**

- `Optional[User]`: The updated `User` object, or `None` if the user is not found.

**Example:**

```python
# Assuming you have an existing user 'user'
updated_user = user_service.update_user(
    user_id=user.user_id,
    username="updateduser",
    firstname="Updated",
    lastname="User",
    role_id=new_role.role_id,
    cinema_id=new_cinema.cinema_id
)
if updated_user:
    print(f"User updated: {updated_user.username}")
else:
    print("User not found.")
```

## Relationships

- `Role`: Each user is associated with a role
- `Cinema`: A user can be associated with a cinema
