import tkinter as tk
from tkinter import ttk
from main_components.management.city_management import CityManagement
from main_components.management.cinema_management import CinemaManagement
from main_components.management.screen_management import ScreenManagement
from main_components.management.seat_management import SeatManagement
from main_components.management.film_management import FilmManagement
from main_components.management.cinema_selector import CinemaSelector
from main_components.management.screening_management import ScreeningManagement
from main_components.management.role_management import RoleManagement
from main_components.management.permission_management import PermissionManagement
from main_components.management.user_management import UserManagement
from main_components.management.booking_management import BookingManagement
from main_components.management.reports_management import ReportsManagement
from main_components.management.Analyse_Predictions import PredictionAnalysisPage

class ManagerPanel(tk.Frame):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent)
        self.user = user
        self.callback = callback
        self.management_frame = ttk.Frame(self)
        self.management_frame.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()
    
    def setup_ui(self):
        self.clear_management_frame() 
        self.cinema_selector = CinemaSelector(self.management_frame, self.on_cinema_selected) # Create the cinema selector.
        self.cinema_selector.pack(pady=20)
    
    def on_cinema_selected(self, cinema_id):
        self.selected_cinema_id = cinema_id
        self.show_management_buttons() #show management buttons after cinema selection.

    def show_management_buttons(self):
        self.clear_management_frame()
        frame = ttk.Frame(self.management_frame, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        self.management_frame.rowconfigure(0, weight=1)
        self.management_frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Manager Panel", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=20) #change pack to grid

        buttons = [
            ("Manage Cities", self.manage_cities),
            ("Manage Cinemas", self.manage_cinemas),
            ("Manage Screens", self.manage_screens),
            ("Manage Screenings", self.manage_screenings),
            ("Manage Seats", self.manage_seats),
            ("Manage Bookings", self.manage_bookings),
            ("Manage Films", self.manage_films),
            ("Manage Permissions", self.manage_permissions),
            ("Manage Users", self.manage_users),
            ("Manage Roles", self.manage_roles),
            ("Generate Reports", self.generate_reports),
            ("Analyse Predictions", self.manage_predictions),
            ("Log Off", self.log_off)
        ]

        row_num = 1
        col_num = 0
        for text, command in buttons:
            ttk.Button(frame, text=text, command=command, padding="10").grid(row=row_num, column=col_num, sticky="ew", padx=5, pady=5)
            col_num += 1
            if col_num > 1:
                col_num = 0
                row_num += 1

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def manage_cities(self):
        self.clear_management_frame()
        city_management = CityManagement(self.management_frame, callback=self.management_callback)
        city_management.pack(fill=tk.BOTH, expand=True)

    def management_callback(self, action):
        if action == "back":
            self.setup_ui() #return to buttons

    def clear_management_frame(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

    def manage_cinemas(self):
        self.clear_management_frame()
        cinema_management = CinemaManagement(self.management_frame, callback=self.management_callback)
        cinema_management.pack(fill=tk.BOTH, expand=True)
    
    def manage_screens(self): 
        self.clear_management_frame()
        screen_management = ScreenManagement(self.management_frame,self.selected_cinema_id, callback=self.management_callback)
        screen_management.pack(fill=tk.BOTH, expand=True)

    def manage_screenings(self):
        self.clear_management_frame()
        screening_management = ScreeningManagement(self.management_frame,self.selected_cinema_id, user=self.user, callback=self.management_callback)
        screening_management.pack(fill=tk.BOTH, expand=True)


    def manage_seats(self):
        self.clear_management_frame()
        seat_management = SeatManagement(self.management_frame, self.selected_cinema_id, callback=self.management_callback)
        seat_management.pack(fill=tk.BOTH, expand=True)

    def manage_bookings(self):
        self.clear_management_frame()
        booking_management = BookingManagement(self.management_frame, self.selected_cinema_id, user=self.user, callback=self.management_callback)
        booking_management.pack(fill=tk.BOTH, expand=True)

    def manage_films(self):
        self.clear_management_frame()
        film_management = FilmManagement(self.management_frame, callback=self.management_callback)
        film_management.pack(fill=tk.BOTH, expand=True)

    def manage_permissions(self):
        self.clear_management_frame()
        permission_management = PermissionManagement(self.management_frame, callback=self.management_callback)
        permission_management.pack(fill=tk.BOTH, expand=True)

    def manage_users(self):
        self.clear_management_frame()
        user_management = UserManagement(self.management_frame, self.selected_cinema_id, callback=self.management_callback)
        user_management.pack(fill=tk.BOTH, expand=True)

    def manage_roles(self):
        self.clear_management_frame()
        role_management = RoleManagement(self.management_frame, callback=self.management_callback)
        role_management.pack(fill=tk.BOTH, expand=True)

    def generate_reports(self):
        self.clear_management_frame()
        reports_management = ReportsManagement(self.management_frame, callback=self.management_callback)
        reports_management.pack(fill=tk.BOTH, expand=True) #show the reports management frame.

    def manage_predictions(self):
        self.clear_management_frame()
        prediction_page = PredictionAnalysisPage(self.management_frame, callback=self.management_callback)
        prediction_page.pack(fill=tk.BOTH, expand=True)

    def log_off(self):
        if self.callback:
            self.callback("logout")