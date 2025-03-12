from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from . import Base  # Import your Base from models/__init__.py. "." indicates a relative import, it tells python to look for "Base" within the package
from datetime import datetime, timedelta, timezone

# User model (Table):
class User(Base):
    """
    Represents a user in the cinema booking system.

    This model stores user information, including personal details, authentication credentials, 
    and role assignments. It also establishes relationships with the Role and Cinema models.

    Attributes:
        user_id (int): Primary key, uniquely identifying each user.
        username (str): Unique username for authentication.
        password (str): Hashed password for secure authentication.
        firstname (str): First name of the user.
        lastname (str): Last name of the user.
        role_id (int): Foreign key linking to the Role table, defining the user's role.
        cinema_id (int, optional): Foreign key linking to the Cinema table, if the user is associated with a specific cinema.
        role (Role): Relationship with the Role model, enabling bidirectional access.
    
    Methods:
        __repr__(): Returns a string representation of the User instance.
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key = True, autoincrement=True) # Unique identifier for the user.
    username = Column(String(255), unique = True, nullable = False) # Username must be unique, and must not be null.
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable = False) # First name of the user.
    lastname = Column(String(255), nullable = False) # Last name of the user.
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable = False) # Foreign key linking to the Role table.
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id')) #link to a cinema, if the user works at one.
    is_password_expired = Column(Boolean, default=False)  # Indicates whether the password has expired.
    expiration_date = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=90))  # When a new row is created, if no value is provided for expiration_date, it will automatically be set to the current UTC time plus 90 days.


    # Relationship to the Role table
    role = relationship('Role', back_populates='users') # ensures that changes to one side of the relationship are automatically reflected on the other. For example, if you add a new User and assign them a Role, the User's role attribute and the Role's users attribute will both be updated automatically, keeping the relationship consistent in both directions.
    cinema = relationship('Cinema', back_populates='users')

    def __init__(self, username: str, password_hash: str, salt: str, firstname: str, lastname: str, role_id: int, cinema_id: int = None):
        """
        Initializes a User instance.

        user_id (int): This will be auto incremented, so no need to include it.
        username (str): Unique username.
        firstname (str): First name of the user.
        lastname (str): Last name of the user.
        role_id (int): Role ID associated with the user.
        cinema_id (int): ID of the cinema the user works at (optional).
        """
        self.username = username
        self.password_hash = password_hash # Store password hash.
        self.salt = salt
        self.firstname = firstname
        self.lastname = lastname
        self.role_id = role_id
        self.cinema_id = cinema_id
        self.is_password_expired = False
        self.expiration_date = datetime.now(timezone.utc) + timedelta(days=90)  # Default expiration is 90 days.

    def get_username(self) -> str:
        """
        Retrieves the username of the user.

        return (str): The username as a string.
        """
        return self.username
    
    def get_firstname(self) -> str:
        """
        Retrieves the first name of the user.

        return (str): The first name as a string.
        """
        return self.firstname

    def get_lastname(self) -> str:
        """
        Retrieves the last name of the user.

        return (str): The last name as a string.
        """
        return self.lastname

    def get_role_id(self) -> int:
        """
        Retrieves the role ID of the user.

        return (int): The role ID as an integer.
        """
        return self.role_id
    
    def check_has_permission(self, permission_id: int) -> bool:
        """
        Checks if the user has a specific permission based on their role.

        permission_id (int): The permission ID to check.
        return (bool): True if the user has the permission, otherwise False.
        """
        return self.role and self.role.check_has_permission(permission_id) # if user dont have role, it will resolve to None. Calls the role class method "check_has_permission"
    
    def get_cinema_id(self) -> int:
        """
        Retrieves the cinema ID where the user works, if applicable.

        return (int): The cinema ID as an integer, or None if not assigned to a cinema.
        """
        return self.cinema_id

    def check_is_password_expired(self) -> bool:
        """
        Checks if the user's password is expired based on the expiration date.

        return (bool): True if the password is expired, otherwise False.
        """
        return datetime.now(timezone.utc) > self.expiration_date
    
    def expire_password(self) -> None:
        """
        Marks the user's password as expired.

        This method should be called when the password reaches the expiration date.
        """
        self.is_password_expired = True
    
    def set_username(self, username: str) -> None:
        """
        Updates the username of the user.

        username (str): The new username to assign.
        """
        if username:
            self.username = username
        else:
            raise ValueError("Username cannot be empty.")


    def set_password(self, password_hash: str, salt: str) -> None:
        """
        Sets the password hash and salt.
        """
        self.password_hash = password_hash
        self.salt = salt
    
    def set_firstname(self, firstname: str) -> None:
        """
        Updates the first name of the user.

        firstname (str): The new first name to assign.
        """
        if firstname:
            self.firstname = firstname
        else:
            raise ValueError("First name cannot be empty.")
    
    def set_lastname(self, lastname: str) -> None:
        """
        Updates the last name of the user.

        lastname (str): The new last name to assign.
        """
        if lastname:
            self.lastname = lastname
        else:
            raise ValueError("Last name cannot be empty.")

    def set_role_id(self, role_id: int) -> None:
        """
        Updates the role ID of the user.

        role_id (int): The new role ID to assign.
        """
        if role_id:
            self.role_id = role_id
        else:
            raise ValueError("Role ID must exist.")

    def set_cinema(self, cinema_id: int) -> None:
        """
        Updates the cinema ID where the user works.

        cinema_id (int): The new cinema ID to assign.
        """
        if cinema_id:
            self.cinema_id = cinema_id
        else:
            raise ValueError("Cinema must exist.")
        
    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', firstname='{self.firstname}', lastname='{self.lastname}')>"
