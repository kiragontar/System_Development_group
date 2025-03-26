from sqlalchemy.orm import Session
from backend.models import Permission

class PermissionService:
    def __init__(self, session: Session):
        self.session = session
        self.model = Permission

    def create_permission(self, name):
        # Create a new permission if it doesn't already exist
        if self.get_permission_by_name(name):
            return None
        new_perm = Permission(name=name)
        self.session.add(new_perm)
        self.session.commit()
        return new_perm

    def get_permission_by_name(self, name):
        # Retrieve a permission by name
        return self.session.query(Permission).filter(Permission.name == name).first()

    def get_permission_by_id(self, permission_id):
        # Retrieve a permission by its ID
        return self.session.get(Permission, permission_id)

    def get_all_permissions(self):
        # Retrieve all permissions
        return self.session.query(Permission).all()

    def update_permission(self, permission_id, name):
        # Update the name of a permission
        perm = self.get_permission_by_id(permission_id)
        if not perm:
            return None
        perm.name = name
        try:
            self.session.commit()
            return perm
        except Exception as e:
            print(f"Error updating permission: {e}")
            self.session.rollback()
            return None

    def delete_permission(self, permission_id):
        # Delete a permission by ID
        perm = self.get_permission_by_id(permission_id)
        if not perm:
            return False
        try:
            # Remove the permission from all roles first
            for role in perm.roles:
                role.permissions.remove(perm)
            self.session.delete(perm)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting permission: {e}")
            self.session.rollback()
            return False
