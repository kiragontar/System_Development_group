import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Role, Permission
from services.role_service import RoleService

# Setup a test database
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def role_service(session):
    return RoleService(session)

def test_create_role(role_service, session):
    role = role_service.create_role("Admin")
    assert role.name == "Admin"
    assert role.role_id is not None
    retrieved_role = session.query(Role).filter_by(role_id=role.role_id).first()
    assert retrieved_role == role

def test_get_role_by_id(role_service, session):
    role = Role(name="Staff")
    session.add(role)
    session.commit()
    retrieved_role = role_service.get_role_by_id(role.role_id)
    assert retrieved_role == role

def test_get_role_by_name(role_service, session):
    role = Role(name="Manager")
    session.add(role)
    session.commit()
    retrieved_role = role_service.get_role_by_name(role.name)
    assert retrieved_role == role

def test_get_all_roles(role_service, session):
    role1 = Role(name="User")
    role2 = Role(name="Guest")
    session.add_all([role1, role2])
    session.commit()
    roles = role_service.get_all_roles()
    assert len(roles) == 2

def test_update_role(role_service, session):
    role = Role(name="OldName")
    session.add(role)
    session.commit()
    updated_role = role_service.update_role(role.role_id, "NewName")
    assert updated_role.name == "NewName"
    retrieved_role = session.query(Role).filter_by(role_id=role.role_id).first()
    assert retrieved_role.name == "NewName"

def test_delete_role(role_service, session):
    role = Role(name="ToDelete")
    session.add(role)
    session.commit()
    result = role_service.delete_role(role.role_id)
    assert result is True
    deleted_role = session.query(Role).filter_by(role_id=role.role_id).first()
    assert deleted_role is None

def test_add_permission_to_role(role_service, session):
    role = Role(name="Admin")
    permission = Permission(name="read")
    session.add_all([role, permission])
    session.commit()
    result = role_service.add_permission_to_role(role.role_id, permission.permission_id)
    assert result is True
    assert permission in role_service.get_permissions_for_role(role.role_id)

def test_remove_permission_from_role(role_service, session):
    role = Role(name="Editor")
    permission = Permission(name="write")
    session.add_all([role, permission])
    session.commit()
    role_service.add_permission_to_role(role.role_id, permission.permission_id)
    result = role_service.remove_permission_from_role(role.role_id, permission.permission_id)
    assert result is True
    assert permission not in role_service.get_permissions_for_role(role.role_id)

def test_get_permissions_for_role(role_service, session):
    role = Role(name="Viewer")
    permission1 = Permission(name="view1")
    permission2 = Permission(name="view2")
    session.add_all([role, permission1, permission2])
    session.commit()
    role_service.add_permission_to_role(role.role_id, permission1.permission_id)
    role_service.add_permission_to_role(role.role_id, permission2.permission_id)
    permissions = role_service.get_permissions_for_role(role.role_id)
    assert len(permissions) == 2

def test_check_role_has_permission(role_service, session):
    role = Role(name="Checker")
    permission = Permission(name="check")
    session.add_all([role, permission])
    session.commit()
    role_service.add_permission_to_role(role.role_id, permission.permission_id)
    assert role_service.check_role_has_permission(role.role_id, permission.permission_id) is True
    assert role_service.check_role_has_permission(role.role_id, 9999) is False