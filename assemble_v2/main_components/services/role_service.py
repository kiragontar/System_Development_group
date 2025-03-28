import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from sqlalchemy.orm import Session
from main_components.models import Role, Permission
from typing import List, Optional


class RoleService:
    """
    Handles operations related to user roles and permissions.
    """

    def __init__(self, session: Session):
        """Initializes the RoleService with a session."""
        self.session = session

    def create_role(self, name: str) -> Role:
        """Creates a new role."""
        role = Role(name=name)
        self.session.add(role)
        self.session.commit()
        return role

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """Retrieves a role by ID."""
        return self.session.query(Role).filter_by(role_id=role_id).first()

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Retrieves a role by name."""
        return self.session.query(Role).filter_by(name=name).first()

    def get_all_roles(self) -> List[Role]:
        """Retrieves all roles."""
        return self.session.query(Role).all()

    def update_role(self, role_id: int, name: str = None) -> Optional[Role]:
        """Updates a role's name."""
        role = self.get_role_by_id(role_id)
        if role:
            if name:
                role.name = name
            self.session.commit()
            return role
        return None

    def delete_role(self, role_id: int) -> bool:
        """Deletes a role."""
        role = self.get_role_by_id(role_id)
        if role:
            self.session.delete(role)
            self.session.commit()
            return True
        return False

    def add_permission_to_role(self, role_id: int, permission_id: int) -> bool:
        """Adds a permission to a role."""
        role = self.get_role_by_id(role_id)
        permission = self.session.query(Permission).filter_by(permission_id=permission_id).first()
        if role and permission:
            if permission not in role.permissions:
                role.permissions.append(permission)
                self.session.commit()
                return True
        return False

    def remove_permission_from_role(self, role_id: int, permission_id: int) -> bool:
        """Removes a permission from a role."""
        role = self.get_role_by_id(role_id)
        permission = self.session.query(Permission).filter_by(permission_id=permission_id).first()
        if role and permission:
            if permission in role.permissions:
                role.permissions.remove(permission)
                self.session.commit()
                return True
        return False

    def get_permissions_for_role(self, role_id: int) -> List['Permission']:
        """Retrieves all permissions associated with a role."""
        role = self.get_role_by_id(role_id)
        if role:
            return role.permissions
        return []

    def check_role_has_permission(self, role_id: int, permission_id: int) -> bool:
        """Checks if a role has a specific permission."""
        role = self.get_role_by_id(role_id)
        permission = self.session.query(Permission).filter_by(permission_id=permission_id).first()
        if role and permission:
            return permission in role.permissions
        return False
