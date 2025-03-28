# Role Service Documentation

## Overview

The Role Service manages operations related to user roles and permissions, including creating, retrieving, updating, and deleting roles, as well as adding and removing permissions from roles.

## Class: `RoleService`

The `RoleService` class provides the following methods:

### `create_role(name)`
Creates a new role.

**Parameters:**
- `name` (str): The name of the new role.

**Returns:**
- `Role`: The newly created `Role` object.

**Example:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Role, Permission
from services.role_service import RoleService
from services.permission_service import PermissionService 

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

role_service = RoleService(session)
permission_service = PermissionService(session) 

new_role = role_service.create_role(name="Admin")
print(f"Role created: {new_role.name}")
```

### `get_role_by_id(role_id)`
Retrieves a role by ID.

**Parameters:**
- `role_id` (int): The ID of the role to retrieve.

**Returns:**
- `Optional[Role]`: The `Role` object if found, or `None` if not found.

**Example:**
```python
role = role_service.get_role_by_id(new_role.role_id)
if role:
    print(f"Role found: {role.name}")
else:
    print("Role not found.")
```

### `get_role_by_name(name)`
Retrieves a role by name.

**Parameters:**
- `name` (str): The name of the role to retrieve.

**Returns:**
- `Optional[Role]`: The `Role` object if found, or `None` if not found.

**Example:**
```python
role = role_service.get_role_by_name(name="Admin")
if role:
    print(f"Role found: {role.name}")
else:
    print("Role not found.")
```

### `get_all_roles()`
Retrieves all roles.

**Returns:**
- `List[Role]`: A list of all `Role` objects.

**Example:**
```python
roles = role_service.get_all_roles()
for r in roles:
    print(f"Role: {r.name}")
```

### `update_role(role_id, name=None)`
Updates a role's name.

**Parameters:**
- `role_id` (int): The ID of the role to update.
- `name` (str, optional): The new name for the role.

**Returns:**
- `Optional[Role]`: The updated `Role` object, or `None` if the role is not found.

**Example:**
```python
updated_role = role_service.update_role(role_id=new_role.role_id, name="Super Admin")
if updated_role:
    print(f"Role updated: {updated_role.name}")
else:
    print("Role not found.")
```

### `delete_role(role_id)`
Deletes a role.

**Parameters:**
- `role_id` (int): The ID of the role to delete.

**Returns:**
- `bool`: `True` if the role was deleted, `False` otherwise.

**Example:**
```python
is_deleted = role_service.delete_role(role_id=new_role.role_id)
print(f"Role deleted: {is_deleted}")
```

### `add_permission_to_role(role_id, permission_id)`
Adds a permission to a role.

**Parameters:**
- `role_id` (int): The ID of the role.
- `permission_id` (int): The ID of the permission to add.

**Returns:**
- `bool`: `True` if the permission was added, `False` otherwise.

**Example:**
```python
new_permission = permission_service.create_permission(name="edit_users")
added = role_service.add_permission_to_role(role_id=new_role.role_id, permission_id=new_permission.permission_id)
print(f"Permission added: {added}")
```

### `remove_permission_from_role(role_id, permission_id)`
Removes a permission from a role.

**Parameters:**
- `role_id` (int): The ID of the role.
- `permission_id` (int): The ID of the permission to remove.

**Returns:**
- `bool`: `True` if the permission was removed, `False` otherwise.

**Example:**
```python
removed = role_service.remove_permission_from_role(role_id=new_role.role_id, permission_id=new_permission.permission_id)
print(f"Permission removed: {removed}")
```

### `get_permissions_for_role(role_id)`
Retrieves all permissions associated with a role.

**Parameters:**
- `role_id` (int): The ID of the role.

**Returns:**
- `List['Permission']`: A list of `Permission` objects associated with the role.

**Example:**
```python
permissions = role_service.get_permissions_for_role(role_id=new_role.role_id)
for p in permissions:
    print(f"Permission: {p.name}")
```

### `check_role_has_permission(role_id, permission_id)`
Checks if a role has a specific permission.

**Parameters:**
- `role_id` (int): The ID of the role.
- `permission_id` (int): The ID of the permission.

**Returns:**
- `bool`: `True` if the role has the permission, `False` otherwise.

**Example:**
```python
has_permission = role_service.check_role_has_permission(role_id=new_role.role_id, permission_id=new_permission.permission_id)
print(f"Role has permission: {has_permission}")
```

## Relationships
- **Users**: A role can be assigned to multiple users 
- **Permissions**: A role can be associated with multiple permissions