from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base, role_permission_association  # Import your Base from models/__init__.py


# Role model (Table):
class Role(Base):
    """
    Represents a user role in the cinema booking system.

    This model defines different user roles and their associated permissions. 
    Each role can be assigned to multiple users, establishing a one-to-many relationship.

    Attributes:
        role_id (int): Primary key, uniquely identifying each role.
        name (str): Unique name of the role (e.g., Admin, Staff).
        users (List[User]): Relationship to the User model, allowing bidirectional access.

    Methods:
        __repr__(): Returns a string representation of the Role instance.
    """
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key = True) # Unique identifier for the role.
    name = Column(String, unique = True, nullable = False) # The name of the role (e.g., Admin, Staff).

    # Relationship to the User table (a role can have many users)
    users = relationship('User', back_populates='role') # Basically creates a users attribute 
    permissions = relationship('Permission', secondary=role_permission_association, back_populates='roles')

    def __init__(self, name: str):
        """Initializes a Role instance."""
        self.name = name

    def get_name(self) -> str:
        """
        Retrieves the name of the role.

        return (str): The name of the role.
        """
        return self.name
    
    def get_id(self) -> int:
        """
        Retrieves the role ID.

        return (int): The role's unique identifier.
        """
        return self.role_id
    
    def set_name(self, name: str) -> None:
        """
        Updates the name of the role.

        name (str): The new name for the role.

        return (None)
        """
        if name:
            self.name = name
        else:
            raise ValueError("Name cannot be empty.")
        
    def __repr__(self):
        """
        Returns a string representation of the Role instance.

        return (str): A string containing role details.
        """
        return f"<Role(role_id={self.role_id}, name={self.name}, permissions={self.permissions})>"