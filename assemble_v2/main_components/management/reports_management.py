import tkinter as tk
from tkinter import ttk
from main_components.management.generate_reports import display_json_report  

class ReportsManagement(tk.Frame):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="Reports Management", font=("Arial", 20)).pack(pady=20)

        ttk.Button(self, text="View Events Log", command=self.view_events_log).pack(pady=10)
        ttk.Button(self, text="Back", command=self.go_back).pack(pady=10)

    def view_events_log(self):
        display_json_report("booking_events.json")  # Display the events log

    def go_back(self):
        if self.callback:
            self.callback("back")