import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.city_service import CityService
from services.cinema_service import CinemaService
from manager_main_screen import ManagerMainScreen

# SQLAlchemy setup
engine = create_engine("mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema")  # Change this to your DB
Session = sessionmaker(bind=engine)
session = Session()

city_service = CityService(session)
cinema_service = CinemaService(session)

COLORS = {
    'background': '#f0f0f0',
    'button': '#2c3e50',
    'button_text': 'white'
}

class SelectCinemaCityScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Select City and Cinema")
        self.root.geometry("500x400")
        self.root.configure(bg=COLORS['background'])

        self.city_var = tk.StringVar()
        self.cinema_var = tk.StringVar()

        self.city_options = {}
        self.cinema_options = {}

        self.setup_widgets()

    def setup_widgets(self):
        # Dropdown: Select City
        tk.Label(self.root, text="Select City:", bg=COLORS['background'], font=('Arial', 12)).pack(pady=(30, 5))
        self.city_dropdown = ttk.Combobox(self.root, textvariable=self.city_var, state="readonly")
        self.city_dropdown.pack(pady=5)
        self.city_dropdown.bind("<<ComboboxSelected>>", self.update_cinema_dropdown)

        # Dropdown: Select Cinema
        tk.Label(self.root, text="Select Cinema:", bg=COLORS['background'], font=('Arial', 12)).pack(pady=(20, 5))
        self.cinema_dropdown = ttk.Combobox(self.root, textvariable=self.cinema_var, state="readonly")
        self.cinema_dropdown.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.root, bg=COLORS['background'])
        button_frame.pack(pady=40)

        tk.Button(
            button_frame, text="Back", width=12,
            command=self.go_back, bg=COLORS['button'], fg=COLORS['button_text']
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame, text="Next", width=12,
            command=self.go_next, bg=COLORS['button'], fg=COLORS['button_text']
        ).grid(row=0, column=1, padx=10)

        self.load_cities()

    def load_cities(self):
        cities = city_service.get_all_cities()
        if not cities:
            messagebox.showinfo("Info", "No cities found.")
            return

        self.city_options = {city.name: city.city_id for city in cities}
        self.city_dropdown['values'] = list(self.city_options.keys())

    def update_cinema_dropdown(self, event=None):
        selected_city_name = self.city_var.get()
        city_id = self.city_options.get(selected_city_name)

        if not city_id:
            return

        cinemas = cinema_service.get_cinemas_by_city(city_id)
        self.cinema_options = {cinema.name: cinema.cinema_id for cinema in cinemas}
        self.cinema_dropdown['values'] = list(self.cinema_options.keys())
        self.cinema_var.set("")  # Reset cinema selection

    def go_back(self):
        self.root.destroy()
        root = tk.Tk()
        ManagerMainScreen(root)
        root.mainloop()
    
    def go_next(self):
        selected_cinema_name = self.cinema_var.get()
        if not selected_cinema_name:
            messagebox.showwarning("Selection Required", "Please select a cinema before proceeding.")
            return

        cinema_id = self.cinema_options[selected_cinema_name]
        self.root.destroy()

        import subprocess
        import sys
        import os

        script_path = os.path.join(os.path.dirname(__file__), "update_film.py")
        subprocess.Popen([sys.executable, script_path, str(cinema_id)])


def main():
    root = tk.Tk()
    app = SelectCinemaCityScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
