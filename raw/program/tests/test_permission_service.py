import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Permission
from services.permission_service import PermissionService

# Setup a test database
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost/testdb"
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
def permission_service(session):
    return PermissionService(session)

def test_create_permission(permission_service, session):
    permission = permission_service.create_permission("test_permission")
    assert permission.name == "test_permission"
    assert permission.permission_id is not None
    retrieved_permission = session.query(Permission).filter_by(permission_id=permission.permission_id).first()
    assert retrieved_permission == permission

def test_get_permission_by_id(permission_service, session):
    permission = Permission(name="test_get_by_id")
    session.add(permission)
    session.commit()
    retrieved_permission = permission_service.get_permission_by_id(permission.permission_id)
    assert retrieved_permission == permission

def test_get_permission_by_name(permission_service, session):
    permission = Permission(name="test_get_by_name")
    session.add(permission)
    session.commit()
    retrieved_permission = permission_service.get_permission_by_name(permission.name)
    assert retrieved_permission == permission

def test_get_all_permissions(permission_service, session):
    permission1 = Permission(name="perm1")
    permission2 = Permission(name="perm2")
    session.add_all([permission1, permission2])
    session.commit()
    permissions = permission_service.get_all_permissions()
    assert len(permissions) == 2

def test_update_permission(permission_service, session):
    permission = Permission(name="old_name")
    session.add(permission)
    session.commit()
    updated_permission = permission_service.update_permission(permission.permission_id, "new_name")
    assert updated_permission.name == "new_name"

def test_delete_permission(permission_service, session):
    permission = Permission(name="to_delete")
    session.add(permission)
    session.commit()
    result = permission_service.delete_permission(permission.permission_id)
    assert result is True
    assert permission_service.get_permission_by_id(permission.permission_id) is None