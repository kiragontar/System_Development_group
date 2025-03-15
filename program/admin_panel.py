import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.user_service import UserService
from services.role_service import RoleService
from services.cinema_service import CinemaService
from models import Base, User, Role, Cinema, City
from services.city_service import CityService

# Assuming you have a database engine and session
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Create test data
# city = City(name="Test City", country="Test Country")
# session.add(city)
# session.commit()
city_service = CityService(session)
city = city_service.create_city(name="London", country="UK")

# cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
# session.add(cinema)
# session.commit()

# role = Role(name="Admin")
# session.add(role)
# session.commit()

role_service = RoleService(session)
cinema_service = CinemaService(session)

user_service = UserService(session, role_service, cinema_service)
user = user_service.create_user()
# city = city_service.create_city(name="London", country="UK")
# print(f"City created: {city.city_id}")

# def on_button_click(screen):
#     if screen == "employee_list":
#         # If Button 3 is clicked, show the Employees screen
#         show_employees_screen()
#     elif screen == "pick_cinema":
#         show_cinema_screen()
#     else:
#         print(f"Button {screen} clicked!")

def show_main_screen():
    """Hide the employees screen and show the main screen."""
    hide_all_screens()  # Hide employees frame
    main_frame.pack(padx=10, pady=10)  # Show main frame again

def show_employees_screen():
    """Hide the main screen and show the employees screen."""
    hide_all_screens() 
    employees_frame.pack(padx=10, pady=10)  # Show employees frame

def show_cinema_screen():
    hide_all_screens()
    cinema_frame.pack(padx=10, pady=10)

def show_cinema_edit_screen(name="", location="", cinema_id=""):
    # Hide other frames
    hide_all_screens()

    # Pre-fill Entry widgets with the given cinema data
    name_entry.delete(0, tk.END)
    name_entry.insert(0, name)

    location_entry.delete(0, tk.END)
    location_entry.insert(0, location)

    id_entry.delete(0, tk.END)
    id_entry.insert(0, cinema_id)

    # Show edit frame
    cinema_edit_frame.pack()

def hide_all_screens():
    main_frame.pack_forget()
    employees_frame.pack_forget()
    cinema_frame.pack_forget()
    cinema_edit_frame.pack_forget()

# Create main application window
root = tk.Tk()
root.title("Switch Screens Example")

# ---------------------------
#  1) MAIN SCREEN (with 5 buttons)
# ---------------------------
main_frame = tk.LabelFrame(root, text="Main Screen")
main_frame.pack(padx=10, pady=10)

# Create 5 buttons in the main screen
button = tk.Button(
    main_frame,
    text="Employee List",
    bg="blue",       # background color
    fg="black",      # text color
    command=show_employees_screen
    )
button.pack(side="left", padx=5, pady=5)

button = tk.Button(
    main_frame,
    text="Pick Cinema",
    bg="blue",       # background color
    fg="black",      # text color
    command=show_cinema_screen
    )
button.pack(side="left", padx=5, pady=5)


# ---------------------------
#  2) EMPLOYEES SCREEN (mock data)
# ---------------------------
employees_frame = tk.Frame(root)

# A label at the top
employees_label = tk.Label(employees_frame, text="Employee List", font=("Arial", 14, "bold"))
employees_label.pack(pady=5)

# Mock data for employees (firstname, lastname, id)
employees = [
    ("John", "Doe", "ID001"),
    ("Jane", "Smith", "ID002"),
    ("Alice", "Johnson", "ID003"),
    ("Bob", "Williams", "ID004")
]

users = user_service.get_all()
print(users)

# Display each employee in a Label
for first_name, last_name, emp_id in employees:
    tk.Label(employees_frame, text=f"{first_name} {last_name} (ID: {emp_id})").pack()

# Add a "Back" button to return to the main screen
back_button = tk.Button(employees_frame, text="Back to Main", command=show_main_screen)
back_button.pack(pady=10)

# ---------------------------
#  3) CINEMA SELECTION SCREEN (mock data)
# ---------------------------
cinema_frame = tk.Frame(root)

# A label at the top
cinema_label = tk.Label(cinema_frame, text="Pick a Cinema", font=("Arial", 14, "bold"))
cinema_label.pack(pady=5)

# Mock data for cinemas
cinemas = [
    ("Cinema 1", "Location A", "CIN001"),
    ("Cinema 2", "Location B", "CIN002"),
    ("Cinema 3", "Location C", "CIN003"),
    ("Cinema 4", "Location D", "CIN004")
]

# Display each cinema in a Label
for name, location, cinema_id in cinemas:
    tk.Label(cinema_frame, text=f"{name} ({location}) - ID: {cinema_id}").pack()

for name, location, cinema_id in cinemas:
    # Create a frame or just a single button for editing
    edit_button = tk.Button(
        cinema_frame,
        text=f"Edit {name}",
        command=lambda n=name, loc=location, c_id=cinema_id: show_cinema_edit_screen(n, loc, c_id)
    )
    edit_button.pack(pady=2)

button = tk.Button(
    cinema_frame,
    text="Create Cinema",
    command=show_cinema_edit_screen
    )
button.pack(side="left", padx=5, pady=5)

# Add a "Back" button to return to the main screen
back_button = tk.Button(cinema_frame, text="Back to Main", command=show_main_screen)
back_button.pack(pady=10)

# ---------------------------
#  4) CINEMA EDIT SCREEN
# ---------------------------
cinema_edit_frame = tk.Frame(root)

# A label at the top
cinema_edit_label = tk.Label(cinema_edit_frame, text="Edit Cinema", font=("Arial", 14, "bold"))
cinema_edit_label.pack(pady=5)

# Labels and Entry widgets for cinema details
name_label = tk.Label(cinema_edit_frame, text="Name:")
name_label.pack()
name_entry = tk.Entry(cinema_edit_frame)
name_entry.pack()

location_label = tk.Label(cinema_edit_frame, text="Location:")
location_label.pack()
location_entry = tk.Entry(cinema_edit_frame)
location_entry.pack()

id_label = tk.Label(cinema_edit_frame, text="Cinema ID:")
id_label.pack()
id_entry = tk.Entry(cinema_edit_frame)
id_entry.pack()

# A simple "Save" button to handle saving the edits
def save_cinema():
    # In a real application, you'd have code here
    # that updates the cinema in your database or data structure.
    updated_name = name_entry.get()
    updated_location = location_entry.get()
    updated_id = id_entry.get()
    # TODO: Save logic or feedback to user
    print(f"Saved: {updated_name}, {updated_location}, {updated_id}")

save_button = tk.Button(cinema_edit_frame, text="Save", command=save_cinema)
save_button.pack(pady=5)

# A "Back" button that returns to the cinema selection screen
back_button = tk.Button(cinema_edit_frame, text="Back to Cinema List", command=show_cinema_screen)
back_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()