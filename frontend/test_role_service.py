from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Role, Permission
from backend.role_service import RoleService
from backend.permission_service import PermissionService

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize services
role_service = RoleService(session)
permission_service = PermissionService(session)

def test_role_crud():
    # Clean existing data
    session.query(Role).delete()
    
    # Test Create
    admin_role = role_service.create_role("Admin")
    assert admin_role is not None, "Role creation failed"
    print(f"Role created: {admin_role.name}")

    # Test Update
    updated_role = role_service.update_role(admin_role.role_id, "Super Admin")
    assert updated_role.name == "Super Admin", "Role update failed"
    print(f"Role updated: {updated_role.name}")

    # Test Delete
    delete_result = role_service.delete_role(admin_role.role_id)
    assert delete_result is True, "Role deletion failed"
    print(f"Role deleted: {delete_result}")

def test_permission_management():
    # Clean existing data
    session.query(Role).delete()
    session.query(Permission).delete()
    
    # Create test data
    editor_role = role_service.create_role("Editor")
    assert editor_role is not None, "Editor role creation failed"
    
    edit_perm = permission_service.create_permission("edit_content")
    assert edit_perm is not None, "Permission creation failed"

    # Test Add Permission
    add_result = role_service.add_permission_to_role(editor_role.role_id, edit_perm.permission_id)
    assert add_result is True, "Permission add failed"
    print(f"Permission added: {add_result}")

    # Test Check Permission
    has_perm = role_service.check_role_has_permission(editor_role.role_id, edit_perm.permission_id)
    assert has_perm is True, "Permission check failed"
    print(f"Permission check: {has_perm}")

    # Test Remove Permission
    remove_result = role_service.remove_permission_from_role(editor_role.role_id, edit_perm.permission_id)
    assert remove_result is True, "Permission remove failed"
    print(f"Permission removed: {remove_result}")

if __name__ == "__main__":
    # Initialize database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    try:
        test_role_crud()
        test_permission_management()
    except Exception as e:
        print(f"\n--- TEST FAILED ---\n{str(e)}")
    finally:
        session.close()