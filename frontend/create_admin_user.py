# create_admin_user.py
import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base
from backend.user_service import UserService
from backend.role_service import RoleService

DATABASE_URL = "mysql+pymysql://shrimp:shrimp@127.0.0.1:3306/cinema"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# Fetch Admin role dynamically
role_service = RoleService(session)
admin_role = role_service.get_role_by_name("Admin")

if not admin_role:
    print("Error: 'Admin' role not found. Run init_admin.py first!")
    exit()

user_service = UserService(session)
admin_user, error = user_service.create_user(
    username="admin",
    password="AdminPassword123!",
    firstname="Admin",
    lastname="User",
    role_id=admin_role.role_id
)

if admin_user:
    print(f"Admin user '{admin_user.username}' created!")
else:
    print(f"Error: {error}")