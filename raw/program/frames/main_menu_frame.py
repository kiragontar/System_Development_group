import tkinter as tk
from frames.employees_frame import EmployeesFrame
from frames.cinema_list_frame import CinemaListFrame

class MainMenuFrame(tk.Frame):
    """The main menu screen with navigation buttons."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Main Menu", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        btn_employees = tk.Button(
            self,
            text="Employee List",
            command=lambda: controller.show_frame("Employees")
        )
        btn_employees.pack(padx=5, pady=5)

        btn_cinemas = tk.Button(
            self,
            text="Pick Cinema",
            command=lambda: controller.show_frame("Cinemas")
        )
        btn_cinemas.pack(padx=5, pady=5)

        self.pack(fill="both", expand=True)  # Ensure the frame gets packed into the container



