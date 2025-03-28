from sqlalchemy.orm import Session
from backend.models import User
import bcrypt
import re

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username, password, firstname, lastname, role_id, cinema_id=None):
        # Check if username already exists
        if self.get_by_username(username):
            return None, "username_exists"

        # Validate password requirements
        password_errors = self.validate_password_requirements(password)
        if password_errors:
            return None, password_errors

        # Hash the password using bcrypt
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(
            username=username,
            password=hashed_pw.decode('utf-8'),
            firstname=firstname,
            lastname=lastname,
            role_id=role_id,
            cinema_id=cinema_id
        )
        try:
            self.session.add(new_user)
            self.session.commit()
            return new_user, None
        except Exception as e:
            print("\n--- DATABASE ERROR ---\n", str(e))
            self.session.rollback()
            return None, "database_error"

    def login(self, username, password):
        # Authenticate the user by username and password
        user = self.get_by_username(username)
        if not user:
            return None, "User not found"
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return None, "Incorrect password"
        return user, None

    def get_by_username(self, username):
        # Retrieve a user by username
        return self.session.query(User).filter(User.username == username).first()

    def get_by_user_id(self, user_id):
        # Retrieve a user by user ID
        return self.session.get(User, user_id)

    def get_all(self):
        # Retrieve all users
        return self.session.query(User).all()

    def get_all_at_cinema(self, cinema_id):
        # Retrieve all users associated with a specific cinema
        return self.session.query(User).filter(User.cinema_id == cinema_id).all()

    def delete_user(self, user_id):
        # Delete a user by user ID
        user = self.get_by_user_id(user_id)
        if not user:
            return False
        try:
            self.session.delete(user)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            self.session.rollback()
            return False

    def update_user(self, user_id, username=None, firstname=None, lastname=None, role_id=None, cinema_id=None):
        # Update user details
        user = self.get_by_user_id(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if firstname:
            user.firstname = firstname
        if lastname:
            user.lastname = lastname
        if role_id:
            user.role_id = role_id
        # Note: Use "is not None" so that cinema_id can be set to None
        if cinema_id is not None:
            user.cinema_id = cinema_id
        try:
            self.session.commit()
            return user
        except Exception as e:
            print(f"Error updating user: {e}")
            self.session.rollback()
            return None

    def validate_password_requirements(self, password):
        # Validate password security rules
        errors = []
        if len(password) < 8:
            errors.append("• At least 8 characters")
        if not re.search(r'[A-Z]', password):
            errors.append("• 1 uppercase letter (A-Z)")
        if not re.search(r'\d', password):
            errors.append("• 1 number (0-9)")
        if not re.search(r'[!@#$%^&*]', password):
            errors.append("• 1 special character (!@#$%^&*)")
        return errors if errors else None
