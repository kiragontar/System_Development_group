# backend/role_service.py
from sqlalchemy.orm import Session
from backend.models import Role, Permission

class RoleService:
    def __init__(self, session: Session):
        self.session = session
        self.initialize_default_roles()
    # NEW METHOD: Create default roles if missing
    def initialize_default_roles(self):
        default_roles = ["Admin", "User", "Manager"]
        for role_name in default_roles:
            role = self.session.query(Role).filter_by(name=role_name).first()
            if not role:
                new_role = Role(name=role_name)
                self.session.add(new_role)
        self.session.commit()

    def create_role(self, name):
        existing_role = self.get_role_by_name(name)
        if existing_role:
            return None
        new_role = Role(name=name)
        self.session.add(new_role)
        self.session.commit()
        return new_role

    def get_role_by_id(self, role_id):
        return self.session.get(Role, role_id)

    def get_role_by_name(self, name):
        return self.session.query(Role).filter(Role.name == name).first()

    def get_all_roles(self):
        return self.session.query(Role).all()

    def update_role(self, role_id, new_name):
        role = self.get_role_by_id(role_id)
        if not role:
            return None
        role.name = new_name
        self.session.commit()
        return role

    def delete_role(self, role_id):
        role = self.get_role_by_id(role_id)
        if not role:
            return False
        if len(role.users) > 0:  # Prevent deletion if users exist
            return False
        try:
            self.session.delete(role)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting role: {e}")
            self.session.rollback()
            return False

    def add_permission_to_role(self, role_id, permission_id):
        role = self.get_role_by_id(role_id)
        perm = self.session.get(Permission, permission_id)
        if role and perm:
            role.permissions.append(perm)
            self.session.commit()
            return True
        return False

    def remove_permission_from_role(self, role_id, permission_id):
        role = self.get_role_by_id(role_id)
        perm = self.session.get(Permission, permission_id)
        if role and perm:
            try:
                role.permissions.remove(perm)
                self.session.commit()
                return True
            except ValueError:
                return False
        return False

    def get_permissions_for_role(self, role_id):
        role = self.get_role_by_id(role_id)
        return role.permissions if role else []

    def check_role_has_permission(self, role_id, permission_id):
        role = self.get_role_by_id(role_id)
        if not role:
            return False
        return any(perm.permission_id == permission_id for perm in role.permissions)