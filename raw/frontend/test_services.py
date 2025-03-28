# test_services.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User, Role, Permission  # Adjust the import path as necessary
from backend.user_service import UserService
from backend.role_service import RoleService
from backend.permission_service import PermissionService


DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Initialize services
user_service = UserService(session)
role_service = RoleService(session)
permission_service = PermissionService(session)

print("=== Testing Role Service ===")
# 1. Create a new role
role = role_service.create_role("Admin")
if role:
    print(f"Role created: {role.name}")
else:
    print("Role already exists.")

# 2. Retrieve role by ID and name
retrieved_role = role_service.get_role_by_id(role.role_id)
print(f"Retrieved role by ID: {retrieved_role.name}")

retrieved_role_by_name = role_service.get_role_by_name("Admin")
print(f"Retrieved role by name: {retrieved_role_by_name.name}")

# 3. Update role name
updated_role = role_service.update_role(role.role_id, "SuperAdmin")
if updated_role:
    print(f"Role updated: {updated_role.name}")
else:
    print("Role update failed.")

# 4. Test permission management for role
permission = permission_service.create_permission("edit_users")
if permission:
    print(f"Permission created: {permission.name}")
else:
    print("Permission already exists.")

# Add permission to role
if role_service.add_permission_to_role(role.role_id, permission.permission_id):
    print("Permission added to role.")
else:
    print("Failed to add permission to role.")

# Check role has permission
has_perm = role_service.check_role_has_permission(role.role_id, permission.permission_id)
print(f"Role has 'edit_users' permission: {has_perm}")

# Remove permission from role
if role_service.remove_permission_from_role(role.role_id, permission.permission_id):
    print("Permission removed from role.")
else:
    print("Failed to remove permission from role.")

# 5. Delete role (only works if no users are assigned)
if role_service.delete_role(role.role_id):
    print("Role deleted successfully.")
else:
    print("Role deletion failed (maybe role is assigned to a user).")

print("\n=== Testing Permission Service ===")
# Test get_permission_by_id, get_all_permissions, update_permission
perm = permission_service.create_permission("view_movies")
if perm:
    print(f"Permission created: {perm.name}")

retrieved_perm = permission_service.get_permission_by_id(perm.permission_id)
if retrieved_perm:
    print(f"Retrieved permission by ID: {retrieved_perm.name}")

all_perms = permission_service.get_all_permissions()
print("All permissions:")
for p in all_perms:
    print(f"- {p.name}")

updated_perm = permission_service.update_permission(perm.permission_id, "view_all_movies")
if updated_perm:
    print(f"Permission updated: {updated_perm.name}")
else:
    print("Permission update failed.")

if permission_service.delete_permission(perm.permission_id):
    print("Permission deleted successfully.")
else:
    print("Permission deletion failed.")

print("\n=== Testing User Service ===")
# Create a role first (if not already created)
role = role_service.create_role("User")
if not role:
    role = role_service.get_role_by_name("User")

# 1. Create a new user
new_user, error = user_service.create_user(
    username="testuser",
    password="SecurePass1!",
    firstname="Test",
    lastname="User",
    role_id=role.role_id
)
if new_user:
    print(f"User created: {new_user.username}")
else:
    print(f"User creation failed: {error}")

# 2. Test login
login_success = user_service.login("testuser", "SecurePass1!")
print(f"Login success: {login_success}")

# 3. Retrieve by user ID and username
user_by_id = user_service.get_by_user_id(new_user.user_id)
print(f"User retrieved by ID: {user_by_id.username}")

user_by_username = user_service.get_by_username("testuser")
print(f"User retrieved by username: {user_by_username.username}")

# 4. Get all users
all_users = user_service.get_all()
print("All users:")
for user in all_users:
    print(f"- {user.username}")

# 5. Update user details
updated_user = user_service.update_user(new_user.user_id, firstname="Updated", lastname="Tester")
if updated_user:
    print(f"User updated: {updated_user.firstname} {updated_user.lastname}")
else:
    print("User update failed.")

# 6. Delete the user
if user_service.delete_user(new_user.user_id):
    print("User deleted successfully.")
else:
    print("User deletion failed.")

# 7. (Optional) If you have a cinema_id field in your model, you can test get_all_at_cinema(cinema_id)
# For example, if new_user.cinema_id is set:
if new_user.cinema_id:
    users_at_cinema = user_service.get_all_at_cinema(new_user.cinema_id)
    print("Users at cinema:")
    for u in users_at_cinema:
        print(f"- {u.username}")

print("\n=== All tests completed. ===")
