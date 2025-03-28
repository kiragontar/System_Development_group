import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from models import User
from typing import List, Optional
import bcrypt

class UserService:
    """
    Handles operations related to user authentication, creation, and role management.

    This service provides methods for user authentication, retrieval, and role 
    assignment, interacting with the database using an SQLAlchemy session.

    Attributes:
        session (Session): The database session used for executing queries and transactions.

    Methods:
        login(username: str, password: str) -> bool:
            Authenticates a user based on their username and password.
        
        create_user(username: str, password: str, firstname: str, lastname: str, role_id: int, cinema: 'Cinema') -> 'User':
            Creates a new user, assigns them a role, and associates them with a cinema.

        get_by_username(username: str) -> 'User':
            Retrieves a user by their username.

        get_role_by_id(role_id: int) -> 'Role':
            Retrieves a role by its ID.

        delete_user(user_id: str) -> bool:
            Deletes a user from the system by their unique user ID
    """

    def __init__(self, session: Session, role_service, cinema_service): 
        """Initializes the UserService with a session and other services."""
        self.session = session
        self.role_service = role_service
        self.cinema_service = cinema_service 

    def login(self, username: str, password: str) -> bool:
        """
        Authenticates a user based on the username and password.
        
        Parameters:
        - username (str): The username of the user.
        - password (str): The password of the user.
        
        Returns:
        bool: - True if the user exists and the password matches, otherwise False.
        """
        user = self.get_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return True
        return False
    
    
    def create_user(self, username: str, password: str, firstname: str, lastname: str, role_id: int, cinema_id: Optional[int] = None) -> User:
        if not self.validate_password_requirements(password):
            raise ValueError("Password does not meet requirements.")

        role = self.role_service.get_role_by_id(role_id)
        if not role:
            raise ValueError("Role not found.")

        if cinema_id:
            cinema = self.cinema_service.get_cinema_by_id(cinema_id)
            if not cinema:
                raise ValueError("Cinema not found.")

        salt = bcrypt.gensalt() # Salt for against rainbow table hack.
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) # Hash password and add salt.
        user = User(username=username, password_hash=hashed_password.decode('utf-8'), salt=salt.decode('utf-8'), firstname=firstname, lastname=lastname, role_id=role_id, cinema_id=cinema_id)
        self.session.add(user)
        self.session.commit()
        return user

    
    def get_by_user_id(self, user_id: int) -> Optional['User']:
        """Retrieves a user by ID."""
        return self.session.query(User).filter_by(user_id=user_id).first()
    
    def get_by_username(self, username: str) -> Optional['User']:
        """Retrieves a user by username."""
        return self.session.query(User).filter_by(username=username).first()

    def get_all(self) -> List['User']:
        """Retrieves all users."""
        return self.session.query(User).all()

    def get_all_at_cinema(self, cinema_id: int) -> List[User]:
        cinema = self.cinema_service.get_cinema_by_id(cinema_id)
        if not cinema:
            raise ValueError("Cinema not found.")
        return self.session.query(User).filter_by(cinema_id=cinema_id).all()

    def validate_password_requirements(self, password: str) -> bool:
        """
        Validates that the password meets required security standards.
        
        Parameters:
        - password (str): The password string to be validated.
        
        Returns:
        Bool - True if the password meets the requirements, otherwise False.
        """
        # Example: Password must be at least 8 characters long, contain a number, and a special character
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for char in password):
            return False
        return True
    
    def delete_user(self, user_id: int) -> bool:
        """Deletes a user."""
        user = self.get_by_user_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
    
    def update_user(self, user_id: int, username: str = None, firstname: str = None,
                    lastname: str = None, role_id: int = None, cinema_id: int = None) -> Optional[User]:
        """Updates a user's details."""
        user = self.get_by_user_id(user_id)
        if user:
            if username:
                user.username = username
            if firstname:
                user.firstname = firstname
            if lastname:
                user.lastname = lastname
            if role_id:
                role = self.role_service.get_role_by_id(role_id)
                if not role:
                    raise ValueError("Role not found.")
                user.role_id = role_id
            if cinema_id is not None:
                if cinema_id:
                    cinema = self.cinema_service.get_cinema_by_id(cinema_id)
                    if not cinema:
                        raise ValueError("Cinema not found.")
                user.cinema_id = cinema_id
            self.session.commit()
            return user
        return None