import tkinter as tk
from tkinter import ttk
from database.database_settings import SessionLocal
from main_components.services.cinema_service import CinemaService

class CinemaSelector(tk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.session = SessionLocal()
        self.cinema_service = CinemaService(self.session)
        self.setup_ui()

    def setup_ui(self):
        self.cinema_label = tk.Label(self, text="Select Cinema:")
        self.cinema_label.pack()

        cinemas = self.cinema_service.get_all_cinemas()
        cinema_names = ["All Cinemas"] + [cinema.name for cinema in cinemas]

        self.cinema_dropdown = ttk.Combobox(self, values=cinema_names, state="readonly")
        self.cinema_dropdown.pack()
        self.cinema_dropdown.current(0)

        self.select_button = tk.Button(self, text="Select", command=self.on_select)
        self.select_button.pack()

    def on_select(self):
        selected_cinema_name = self.cinema_dropdown.get()
        if selected_cinema_name == "All Cinemas":
            self.callback("all")
        else:
            cinema = self.cinema_service.get_cinema_by_name(selected_cinema_name)
            self.callback(cinema.cinema_id)