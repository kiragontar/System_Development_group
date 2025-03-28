from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base, role_permission_association


class Permission(Base):
    """Represents a permission."""
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # Relationships
    roles = relationship('Role', secondary=role_permission_association, back_populates='permissions')

    def __init__(self, name: str):
        """Initializes a Permission instance."""
        self.name = name

    def get_id(self) -> int:
        """Retrieves the permission ID."""
        return self.permission_id
    
    def get_name(self) -> str:
        """Retrieves the name of the permission."""
        return self.name
    
    def set_name(self, name: str) -> None:
        """Updates the name of the permission."""
        if name:
            self.name = name
        else:
            raise ValueError("Name cannot be empty.")

    def __repr__(self):
        """Returns a string representation of the Permission instance."""
        return f"<Permission(permission_id={self.permission_id}, name={self.name})>"