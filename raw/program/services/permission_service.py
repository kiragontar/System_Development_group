from sqlalchemy.orm import Session
from models import Permission
from typing import List, Optional


class PermissionService:
    """
    Handles operations related to permissions.
    """

    def __init__(self, session: Session):
        """Initializes the PermissionService with a session."""
        self.session = session

    def create_permission(self, name: str) -> Permission:
        """Creates a new permission."""
        permission = Permission(name=name)
        self.session.add(permission)
        self.session.commit()
        return permission

    def get_permission_by_id(self, permission_id: int) -> Optional[Permission]:
        """Retrieves a permission by ID."""
        return self.session.query(Permission).filter_by(permission_id=permission_id).first()

    def get_permission_by_name(self, name: str) -> Optional[Permission]:
        """Retrieves a permission by name."""
        return self.session.query(Permission).filter_by(name=name).first()

    def get_all_permissions(self) -> List[Permission]:
        """Retrieves all permissions."""
        return self.session.query(Permission).all()

    def update_permission(self, permission_id: int, name: str) -> Optional[Permission]:
        """Updates a permission's name."""
        permission = self.get_permission_by_id(permission_id)
        if permission:
            permission.name = name
            self.session.commit()
            return permission
        return None

    def delete_permission(self, permission_id: int) -> bool:
        """Deletes a permission."""
        permission = self.get_permission_by_id(permission_id)
        if permission:
            self.session.delete(permission)
            self.session.commit()
            return True
        return False
