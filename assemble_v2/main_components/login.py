import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_components.services.user_service import UserService  # Import UserService
from main_components.services.role_service import RoleService  # Import RoleService
from main_components.services.cinema_service import CinemaService # Import CinemaService
from main_components.services.city_service import CityService
from models import User  # Import User model

# Database setup
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Create RoleService and CinemaService instances
role_service = RoleService(session)
cinema_service = CinemaService(session)
city_service = CityService(session)

# Create UserService instance
user_service = UserService(session, role_service, cinema_service)

def create_test_city():
    try:
        existing_city = city_service.get_city_by_name("Test City")
        if not existing_city:
            test_city = city_service.create_city(
                name="Test City",
                country="Test Country"
            )
            messagebox.showinfo("City Creation", "Test city created successfully.")
            return test_city.city_id
        else:
            return existing_city.city_id
    except Exception as e:
        messagebox.showerror("City Creation", f"Failed to create test city: {e}")
        return None

def create_test_cinema():
    city_id = create_test_city()
    try:
        existing_cinema = cinema_service.get_cinema_by_name("Test Cinema")
        if not existing_cinema:
            test_cinema = cinema_service.create_cinema(
                name="Test Cinema",
                address="123 Test St",
                city_id= city_id
            )
            messagebox.showinfo("Cinema Creation", "Test cinema created successfully.")
            return test_cinema.cinema_id
        else:
            return existing_cinema.cinema_id
    except Exception as e:
        messagebox.showerror("Cinema Creation", f"Failed to create test cinema: {e}")
        return None
    
# Create a role (if it doesn't exist)
def create_test_role():
    try:
        # Check if the role already exists
        existing_role = role_service.get_role_by_name("Test Role")
        if not existing_role:
            test_role = role_service.create_role(name="Test Role")
            messagebox.showinfo("Role Creation", "Test role created successfully.")
            return test_role.role_id
        else:
            return existing_role.role_id
    except Exception as e:
        messagebox.showerror("Role Creation", f"Failed to create test role: {e}")
        return None
# Add a test user
def create_test_user():
    cinema_id = create_test_cinema()
    role_id = create_test_role()
    try:
        # Assuming you have a role ID for a standard user (e.g., role_id=1)
        test_user = user_service.create_user(
            username="testuser",
            password="testpassword1$",
            firstname="test",
            lastname="testlast",
            role_id=role_id,  # Replace with a valid role ID from your database
            cinema_id=cinema_id # Replace with a valid cinema ID
        )
        messagebox.showinfo("User Creation", "Test user created successfully.")
    except Exception as e:
        messagebox.showerror("User Creation", f"Failed to create test user: {e}")


# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
   # Use UserService's login method
    user = user_service.login(username, password)

    if user:
        messagebox.showinfo("Login", "Login Successful")
        # Add code to navigate to the next screen or perform actions after login
    else:
        messagebox.showerror("Login", "Invalid Credentials")

# Function to handle signup (not implemented)
def signup():
    messagebox.showinfo("Sign Up", "Sign Up functionality is not implemented yet")

# Function to clear placeholder text when user focuses on the field
def clear_placeholder(event):
    if event.widget.get() == event.widget.placeholder:
        event.widget.delete(0, tk.END)
        event.widget.configure(fg="white")

# Function to add placeholder text if the field is empty
def add_placeholder(event):
    if not event.widget.get():
        event.widget.insert(0, event.widget.placeholder)
        event.widget.configure(fg="grey")

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("1280x720")
root.configure(bg="#b6b8ba")

# Create a frame to center the content
frame = tk.Frame(root, bg="#b6b8ba")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Add buttons to create the city.
create_city_button = tk.Button(root, text="Create Test City", command=create_test_city)
create_city_button.pack()

# Add buttons to create the cinema.
create_cinema_button = tk.Button(root, text="Create Test Cinema", command=create_test_cinema)
create_cinema_button.pack()

# Add buttons to create the role.
create_role_button = tk.Button(root, text="Create Test Role", command=create_test_role)
create_role_button.pack()
# Add a button to create the test user (for testing purposes)
create_user_button = tk.Button(root, text="Create Test User", command=create_test_user)
create_user_button.pack() # place it somewhere in your window.
# Create username label and entry field
label_username = tk.Label(frame, text="Username", font=("Arial", 14), bg="#b6b8ba")
label_username.grid(row=0, column=0, pady=10, padx=10)
entry_username = tk.Entry(frame, font=("Arial", 14), fg="grey", bg="#7a818c", insertbackground="black", highlightthickness=0)
entry_username.placeholder = "Enter username"
entry_username.insert(0, entry_username.placeholder)
entry_username.bind("<FocusIn>", clear_placeholder)
entry_username.bind("<FocusOut>", add_placeholder)
entry_username.grid(row=0, column=1, pady=10, padx=20)

# Create password label and entry field
label_password = tk.Label(frame, text="Password", font=("Arial", 14), bg="#b6b8ba")
label_password.grid(row=1, column=0, pady=10, padx=10)
entry_password = tk.Entry(frame, font=("Arial", 14), fg="grey", bg="#7a818c", insertbackground="black", highlightthickness=0, show="*")
entry_password.placeholder = "Enter password"
entry_password.insert(0, entry_password.placeholder)
entry_password.bind("<FocusIn>", clear_placeholder)
entry_password.bind("<FocusOut>", add_placeholder)
entry_password.grid(row=1, column=1, pady=10, padx=20)

# Create a frame for buttons and align them to the right
button_frame = tk.Frame(frame, bg="#b6b8ba")
button_frame.grid(row=2, column=1, pady=20, padx=20, sticky="e")

# Create and place the login button
button_login = tk.Button(button_frame, text="Login", command=login, bd=0, font=("Arial", 14), highlightthickness=1)
button_login.pack(side=tk.LEFT, padx=10)

# Create and place the sign up button
button_signup = tk.Button(button_frame, text="Sign Up", command=signup, bd=0, font=("Arial", 14), highlightthickness=1)
button_signup.pack(side=tk.LEFT, padx=10)

# Start the Tkinter event loop
root.mainloop()
