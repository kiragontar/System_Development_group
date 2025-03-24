import tkinter as tk
from tkinter import messagebox
import os
import sys
import subprocess

# Color scheme for consistency with seat_layout.py
COLORS = {
    'background': '#f0f0f0',
    'header': '#3a7ca5',
    'header_text': 'white',
    'button': '#2c3e50',
    'button_text': 'white',
    'card_bg': '#ffffff',
    'card_border': '#d9d9d9',
    'footer': '#3a7ca5'
}

class ManagerMainScreen:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_header()
        self.create_main_content()
        self.create_footer()
    
    def setup_window(self):
        self.root.title("Cinema Management System - Manager Portal")
        self.root.state('zoomed')  # Full window mode
        self.root.configure(bg=COLORS['background'])
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Set minimum size
        self.root.minsize(1024, 768)
    
    def create_header(self):
        # Create a header frame
        self.header_frame = tk.Frame(self.root, bg=COLORS['header'], height=60)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Add title
        tk.Label(
            self.header_frame, 
            text="Cinema Management System", 
            font=("Arial", 20, "bold"), 
            bg=COLORS['header'], 
            fg=COLORS['header_text']
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        # Add manager label
        tk.Label(
            self.header_frame, 
            text="Manager Portal", 
            font=("Arial", 14), 
            bg=COLORS['header'], 
            fg=COLORS['header_text']
        ).pack(side=tk.RIGHT, padx=20, pady=15)
    
    def create_main_content(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg=COLORS['background'])
        self.main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Welcome message
        welcome_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        welcome_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            welcome_frame,
            text="Welcome to the Manager Portal",
            font=("Arial", 18, "bold"),
            bg=COLORS['background']
        ).pack(anchor="w")
        
        tk.Label(
            welcome_frame,
            text="Select a management function below:",
            font=("Arial", 12),
            bg=COLORS['background']
        ).pack(anchor="w", pady=5)
        
        # Create the management cards grid
        self.create_management_grid()
    
    def create_management_grid(self):
        # Container for the cards
        cards_container = tk.Frame(self.main_container, bg=COLORS['background'])
        cards_container.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Configure grid with 3 columns
        for i in range(3):
            cards_container.columnconfigure(i, weight=1)
        
        # Management functions and their descriptions
        management_functions = [
            {
                "title": "Screen and Seats",
                "description": "Manage cinema screens and seating layouts",
                "icon": "🪑",  # Unicode icon
                "command": self.open_screen_and_seats
            },
            {
                "title": "Movie Management",
                "description": "Add, edit, or remove movies from the system",
                "icon": "🎬",
                "command": self.open_movie_management
            },
            {
                "title": "Scheduling",
                "description": "Manage movie showtimes and scheduling",
                "icon": "🕒",
                "command": self.open_scheduling
            },
            {
                "title": "Staff Management",
                "description": "Manage employee accounts and permissions",
                "icon": "👥",
                "command": self.open_staff_management
            },
            {
                "title": "Reports & Statistics",
                "description": "View sales reports and audience statistics",
                "icon": "📊",
                "command": self.open_reports
            },
            {
                "title": "Pricing & Promotions",
                "description": "Manage ticket prices and special promotions",
                "icon": "💰",
                "command": self.open_pricing
            }
        ]
        
        # Create a card for each management function
        row, col = 0, 0
        for idx, function in enumerate(management_functions):
            self.create_card(cards_container, function, row, col)
            col += 1
            if col > 2:  # Move to next row after 3 cards
                col = 0
                row += 1
    
    def create_card(self, parent, function_data, row, col):
        # Card frame with border effect
        card = tk.Frame(
            parent, 
            bg=COLORS['card_bg'], 
            borderwidth=1,
            relief="solid",
            padx=15, 
            pady=15
        )
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Icon
        tk.Label(
            card,
            text=function_data["icon"],
            font=("Arial", 28),
            bg=COLORS['card_bg']
        ).pack(pady=(0, 10))
        
        # Title
        tk.Label(
            card,
            text=function_data["title"],
            font=("Arial", 14, "bold"),
            bg=COLORS['card_bg']
        ).pack(pady=(0, 5))
        
        # Description
        tk.Label(
            card,
            text=function_data["description"],
            font=("Arial", 10),
            bg=COLORS['card_bg'],
            wraplength=200
        ).pack(pady=(0, 15))
        
        # Button
        button = tk.Button(
            card,
            text="Open",
            command=function_data["command"],
            bg=COLORS['button'],
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            padx=15,
            pady=5
        )
        button.pack(pady=5)
    
    def create_footer(self):
        # Create footer
        self.footer_frame = tk.Frame(self.root, bg=COLORS['footer'], height=30)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add footer text
        tk.Label(
            self.footer_frame,
            text="Cinema Management System © 2025",
            font=("Arial", 10),
            bg=COLORS['footer'],
            fg=COLORS['header_text']
        ).pack(side=tk.LEFT, padx=20, pady=5)
        
        # Add version
        tk.Label(
            self.footer_frame,
            text="v1.0",
            font=("Arial", 10),
            bg=COLORS['footer'],
            fg=COLORS['header_text']
        ).pack(side=tk.RIGHT, padx=20, pady=5)
    
    # Functions for management options
    def open_seat_layout(self):
        try:
            # Get the path to seat_layout.py
            seat_layout_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "seat_layout.py"
            )
            
            # Run the seat layout script
            subprocess.Popen([sys.executable, seat_layout_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Seat Layout Manager: {str(e)}")
    
    def open_screen_and_seats(self):
        try:
            # Get the path to seat_layout.py
            seat_layout_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "seat_layout.py"
            )
            
            # Run the seat layout script
            subprocess.Popen([sys.executable, seat_layout_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Screen and Seats Manager: {str(e)}")
    
    def open_movie_management(self):
        messagebox.showinfo("Movie Management", "Movie Management functionality coming soon")
    
    def open_scheduling(self):
        messagebox.showinfo("Scheduling", "Scheduling functionality coming soon")
    
    def open_staff_management(self):
        try:
            # Get the path to staff_management.py
            staff_management_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "staff_management.py"
            )
            
            # Run the staff management script
            subprocess.Popen([sys.executable, staff_management_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Staff Management: {str(e)}")
    
    def open_reports(self):
        messagebox.showinfo("Reports", "Reports functionality coming soon")
    
    def open_pricing(self):
        messagebox.showinfo("Pricing", "Pricing functionality coming soon")

def main():
    root = tk.Tk()
    app = ManagerMainScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()