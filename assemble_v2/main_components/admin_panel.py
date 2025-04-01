import tkinter as tk
from tkinter import ttk
from main_components.management.film_management import FilmManagement
from main_components.management.screening_management import ScreeningManagement
from main_components.management.reports_management import ReportsManagement 
from main_components.management.booking_management import BookingManagement
from main_components.management.cinema_selector import CinemaSelector

class AdminPanel(tk.Frame):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent)
        self.user = user
        self.callback = callback
        self.admin_frame = ttk.Frame(self)
        self.admin_frame.pack(fill=tk.BOTH, expand=True)
        self.selected_cinema_id = None
        self.setup_ui()

    def setup_ui(self):
        self.clear_admin_frame()
        self.cinema_selector = CinemaSelector(self.admin_frame, self.on_cinema_selected)
        self.cinema_selector.pack(pady=20)

    def on_cinema_selected(self, cinema_id):
        self.selected_cinema_id = cinema_id
        self.show_admin_buttons()

    def show_admin_buttons(self):
        self.clear_admin_frame()
        frame = ttk.Frame(self.admin_frame, padding="20")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Admin Panel", font=("Arial", 24)).pack(pady=20)

        buttons = [
            ("Manage Films", self.manage_films),
            ("Manage Screenings", self.manage_screenings),
            ("Generate Reports", self.generate_reports),
            ("Make Booking", self.make_booking),
            ("Log Off", self.log_off)
        ]

        for text, command in buttons:
            ttk.Button(frame, text=text, command=command, padding="10").pack(pady=5, fill="x")


    def clear_admin_frame(self):
        for widget in self.admin_frame.winfo_children():
            widget.destroy()

    def manage_films(self):
        self.clear_admin_frame()
        film_management = FilmManagement(self.admin_frame, callback=self.management_callback)
        film_management.pack(fill=tk.BOTH, expand=True)

    def manage_screenings(self):
        self.clear_admin_frame()
        screening_management = ScreeningManagement(self.admin_frame, self.selected_cinema_id, user=self.user, callback=self.management_callback) # Allow cinema selection for admins
        screening_management.pack(fill=tk.BOTH, expand=True)

    def generate_reports(self):
        self.clear_admin_frame()
        reports_management = ReportsManagement(self.admin_frame, callback=self.management_callback)
        reports_management.pack(fill=tk.BOTH, expand=True)

    def make_booking(self):
        self.clear_admin_frame()
        booking_management = BookingManagement(self.admin_frame, self.selected_cinema_id, user=self.user, callback=self.management_callback) 
        booking_management.pack(fill=tk.BOTH, expand=True)

    def management_callback(self, action):
        if action == "back":
            self.show_admin_buttons()

    def log_off(self):
        if self.callback:
            self.callback("logout")
