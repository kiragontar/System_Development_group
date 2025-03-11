from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base, role_permission_association


class Permission(Base):
    """Represents a permission."""
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationships
    roles = relationship('Role', secondary=role_permission_association, back_populates='permissions')

    def __init__(self, name: str):
        """Initializes a Permission instance."""
        self.name = name

    def get_id(self) -> int:
        """Retrieves the permission ID."""
        return self.permission_id

    def __repr__(self):
        """Returns a string representation of the Permission instance."""
        return f"<Permission(permission_id={self.permission_id}, name={self.name})>"