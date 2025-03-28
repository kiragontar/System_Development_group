import tkinter as tk
from frames.main_menu_frame import MainMenuFrame
from frames.employees_frame import EmployeesFrame
from frames.cinema_list_frame import CinemaListFrame
from frames.cinema_edit_frame import CinemaEditFrame
from services.user_service import UserService
from services.role_service import RoleService
from services.cinema_service import CinemaService
from services.city_service import CityService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema Application")
        self.database_url = DATABASE_URL
        self.engine = create_engine(DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.session = self.SessionLocal()

        # Instantiate services
        self.role_service = RoleService(self.session)
        self.cinema_service = CinemaService(self.session)
        self.city_service = CityService(self.session)
        self.user_service = UserService(self.session, self.role_service, self.cinema_service)

        # Create a container for your frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Instantiate frames
        self.main_menu_frame = MainMenuFrame(container, self)
        self.employees_frame = EmployeesFrame(container, self)
        self.cinema_list_frame = CinemaListFrame(container, self)
        self.cinema_edit_frame = CinemaEditFrame(container, self)

        # Store frames in an easy-to-access way
        self.frames = {
            "MainMenu": self.main_menu_frame,
            "Employees": self.employees_frame,
            "Cinemas": self.cinema_list_frame,
            "CinemaEdit": self.cinema_edit_frame
        }

        # Show the main menu first
        self.show_frame("MainMenu")

    def show_frame(self, frame_name, *args):
        """Show the specified frame."""
        # Hide all frames first
        for frame in self.frames.values():
            frame.pack_forget()

        # Get the frame to display
        frame = self.frames[frame_name]

        # If the frame needs to refresh data or accept arguments:
        if frame_name == "Employees":
            frame.refresh_employee_list()
        elif frame_name == "CinemaEdit":
            name, location, cinema_id, city_id = args
            frame.show_cinema_details(name, location, cinema_id, city_id)
        elif frame_name == "Cinemas":
            frame.refresh_cinema_list()

        # Show the selected frame
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
