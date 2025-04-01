import tkinter as tk
from tkinter import ttk
from main_components.management.booking_management import BookingManagement
from main_components.management.screening_management import ScreeningManagement

class BookingStaffPanel(tk.Frame):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent)
        self.user = user
        self.callback = callback
        self.cinema_id = self.user.cinema_id  # Get cinema_id from user
        self.staff_frame = ttk.Frame(self)
        self.staff_frame.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        self.clear_staff_frame()
        frame = ttk.Frame(self.staff_frame, padding="20")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Booking Staff Panel", font=("Arial", 24)).pack(pady=20)

        buttons = [
            ("Manage Bookings", self.manage_bookings),
            ("View Screenings", self.view_screenings),
            ("Log Off", self.log_off)
        ]

        for text, command in buttons:
            ttk.Button(frame, text=text, command=command, padding="10").pack(pady=5, fill="x")

    def clear_staff_frame(self):
        for widget in self.staff_frame.winfo_children():
            widget.destroy()

    def manage_bookings(self):
        self.clear_staff_frame()
        booking_management = BookingManagement(self.staff_frame, self.cinema_id, user=self.user, callback=self.management_callback)
        booking_management.pack(fill=tk.BOTH, expand=True)

    def view_screenings(self):
        self.clear_staff_frame()
        screening_management = ScreeningManagement(self.staff_frame, self.cinema_id, user=self.user, callback=self.management_callback)
        screening_management.pack(fill=tk.BOTH, expand=True)

    def management_callback(self, action):
        if action == "back":
            self.setup_ui() # Go back to the main staff buttons

    def log_off(self):
        if self.callback:
            self.callback("logout")