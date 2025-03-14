# Permission Service Documentation

## Overview

The Permission Service manages operations related to permissions, including creating, retrieving, updating, and deleting permissions.

## Class: `PermissionService`

The `PermissionService` class provides the following methods:

### `create_permission(name)`
Creates a new permission.

**Parameters:**
- `name` (str): The name of the new permission.

**Returns:**
- `Permission`: The newly created `Permission` object.

**Example:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Permission
from services.permission_service import PermissionService

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

permission_service = PermissionService(session)

new_permission = permission_service.create_permission(name="view_movies")
print(f"Permission created: {new_permission.name}")
```

### `get_permission_by_id(permission_id)`
Retrieves a permission by ID.

**Parameters:**
- `permission_id` (int): The ID of the permission to retrieve.

**Returns:**
- `Optional[Permission]`: The `Permission` object if found, or `None` if not found.

**Example:**
```python
permission = permission_service.get_permission_by_id(new_permission.permission_id)
if permission:
    print(f"Permission found: {permission.name}")
else:
    print("Permission not found.")
```

### `get_permission_by_name(name)`
Retrieves a permission by name.

**Parameters:**
- `name` (str): The name of the permission to retrieve.

**Returns:**
- `Optional[Permission]`: The `Permission` object if found, or `None` if not found.

**Example:**
```python
permission = permission_service.get_permission_by_name(name="view_movies")
if permission:
    print(f"Permission found: {permission.name}")
else:
    print("Permission not found.")
```

### `get_all_permissions()`
Retrieves all permissions.

**Returns:**
- `List[Permission]`: A list of all `Permission` objects.

**Example:**
```python
permissions = permission_service.get_all_permissions()
for p in permissions:
    print(f"Permission: {p.name}")
```

### `update_permission(permission_id, name)`
Updates a permission's name.

**Parameters:**
- `permission_id` (int): The ID of the permission to update.
- `name` (str): The new name for the permission.

**Returns:**
- `Optional[Permission]`: The updated `Permission` object, or `None` if the permission is not found.

**Example:**
```python
updated_permission = permission_service.update_permission(permission_id=new_permission.permission_id, name="edit_movies")
if updated_permission:
    print(f"Permission updated: {updated_permission.name}")
else:
    print("Permission not found.")
```

### `delete_permission(permission_id)`
Deletes a permission.

**Parameters:**
- `permission_id` (int): The ID of the permission to delete.

**Returns:**
- `bool`: `True` if the permission was deleted, `False` otherwise.

**Example:**
```python
is_deleted = permission_service.delete_permission(permission_id=new_permission.permission_id)
print(f"Permission deleted: {is_deleted}")
```

## Relationships
- **Roles**: A permission can be associated with multiple roles