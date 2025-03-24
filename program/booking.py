import tkinter as tk
from tkinter import messagebox, ttk
import os
import json
import sys
from datetime import datetime, timedelta

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models and enums for reference (not for active use)
from models.booking import Booking
from models.screening import Screening
from models.seat import Seat
from models.ticket import Ticket
from models.payment import Payment
from enums import PaymentStatus

# Color scheme matching seat layout
COLORS = {
    'background': '#f0f0f0',
    'header': '#3a7ca5',
    'header_text': 'white',
    'button': '#2c3e50',
    'button_text': 'white',
    'empty_seat': '#d9d9d9',
    'seat_border': '#a3a3a3',
    'low_seat': '#81c784',
    'upper_seat': '#64b5f6',
    'vip_seat': '#ba68c8',
    'selected_seat': '#ff9800',
    'unavailable_seat': '#e57373'
}

# Mock classes for testing without database
class MockMovie:
    def __init__(self, movie_id, title, duration, rating):
        self.movie_id = movie_id
        self.title = title
        self.duration = duration
        self.rating = rating

class MockHall:
    def __init__(self, hall_id, name, layout_name, seats=None):
        self.hall_id = hall_id
        self.name = name
        self.layout_name = layout_name
        self.seats = seats or []

class MockScreening:
    def __init__(self, screening_id, movie, hall, start_time, bookings=None):
        self.screening_id = screening_id
        self.movie = movie
        self.hall = hall
        self.start_time = start_time
        self.hall_id = hall.hall_id
        self.bookings = bookings or []

class MockSeat:
    def __init__(self, seat_id, hall_id, row, column, seat_class, price):
        self.seat_id = seat_id
        self.hall_id = hall_id
        self.row = row
        self.column = column
        self.seat_class = seat_class
        self.price = price

# Generate mock data for testing
def generate_mock_data():
    # Mock movies
    movies = [
        MockMovie(1, "The Matrix Resurrections", 148, "PG-13"),
        MockMovie(2, "Dune", 155, "PG-13"),
        MockMovie(3, "No Time To Die", 163, "PG-13"),
    ]
    
    # Create hall with seats
    def create_hall_with_seats(hall_id, name, layout_name, rows, cols):
        seats = []
        for r in range(1, rows+1):
            for c in range(1, cols+1):
                seat_class = 'VIP' if r <= 2 else 'upper' if r <= 5 else 'low'
                price = 15.0 if seat_class == 'VIP' else 12.0 if seat_class == 'upper' else 10.0
                seats.append(MockSeat(
                    f"{hall_id}-{r}-{c}",
                    hall_id,
                    r,
                    c,
                    seat_class,
                    price
                ))
        return MockHall(hall_id, name, layout_name, seats)
    
    # Create halls
    halls = [
        create_hall_with_seats(1, "Hall 1", "standard_hall", 8, 10),
        create_hall_with_seats(2, "Hall 2", "large_hall", 12, 15),
        create_hall_with_seats(3, "VIP Hall", "vip_hall", 6, 8)
    ]
    
    # Create screenings
    now = datetime.now()
    screenings = [
        MockScreening(1, movies[0], halls[0], now + timedelta(hours=2)),
        MockScreening(2, movies[0], halls[1], now + timedelta(hours=5)),
        MockScreening(3, movies[1], halls[2], now + timedelta(hours=3)),
        MockScreening(4, movies[1], halls[0], now + timedelta(days=1, hours=2)),
        MockScreening(5, movies[2], halls[1], now + timedelta(days=1, hours=5)),
    ]
    
    return {
        'movies': movies,
        'halls': halls,
        'screenings': screenings
    }

class BookingProcess:
    def __init__(self, master=None):
        """Initialize the booking process window"""
        if master:
            self.window = tk.Toplevel(master)
        else:
            self.window = tk.Tk()
            
        self.window.title("Cinema Booking System")
        self.window.state('zoomed')  # Full window mode
        self.window.configure(bg=COLORS['background'])
        
        # Initialize variables
        self.selected_screening = None
        self.selected_seats = []
        self.seat_layout = []
        self.customer_name = ""
        self.customer_email = ""
        self.customer_phone = ""
        self.total_price = 0.0
        
        # Load mock data
        self.mock_data = generate_mock_data()
        
        # Setup UI
        self.create_header()
        self.create_main_container()
        
        # Start with the screening selection step
        self.show_screening_selection()
    
    def create_header(self):
        """Create the header with title"""
        header_frame = tk.Frame(self.window, bg=COLORS['header'], height=60)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(
            header_frame, 
            text="Cinema Booking System", 
            font=("Arial", 18, "bold"), 
            bg=COLORS['header'], 
            fg=COLORS['header_text']
        ).pack(side=tk.LEFT, padx=20, pady=10)
    
    def create_main_container(self):
        """Create the main container for content"""
        self.main_container = tk.Frame(self.window, bg=COLORS['background'])
        self.main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Status bar at the bottom
        self.status_frame = tk.Frame(self.window, bg=COLORS['header'], height=30)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = tk.Label(
            self.status_frame, 
            text="Status: Starting booking process", 
            font=("Arial", 10), 
            bg=COLORS['header'], 
            fg=COLORS['header_text'],
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def clear_main_container(self):
        """Clear the main container before showing a new step"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_screening_selection(self):
        """Show the screening selection step"""
        self.clear_main_container()
        
        # Create heading
        tk.Label(
            self.main_container,
            text="Select a Screening",
            font=("Arial", 16, "bold"),
            bg=COLORS['background']
        ).pack(pady=20)
        
        # Create frame for screenings
        screenings_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        screenings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Use mock screenings instead of database query
        screenings = self.mock_data['screenings']
        
        # Create headers
        headers = ["Movie Title", "Date", "Time", "Hall", "Available Seats", "Select"]
        for i, header in enumerate(headers):
            tk.Label(
                screenings_frame,
                text=header,
                font=("Arial", 12, "bold"),
                bg=COLORS['header'],
                fg=COLORS['header_text'],
                padx=10,
                pady=5,
                borderwidth=1,
                relief="solid",
                width=15 if i != 0 else 30
            ).grid(row=0, column=i, sticky="ew", padx=2, pady=5)
        
        # Function to handle screening selection
        def select_screening(screening):
            self.selected_screening = screening
            self.status_label.config(text=f"Status: Selected screening of {screening.movie.title}")
            self.show_seat_selection()
        
        # Populate screenings
        for i, screening in enumerate(screenings):
            # Calculate available seats
            total_seats = len(screening.hall.seats)
            # Mock some bookings
            booked_seats = i * 2  # Just a mock formula for demonstration
            available_seats = total_seats - booked_seats
            
            # Movie title
            tk.Label(
                screenings_frame,
                text=screening.movie.title,
                font=("Arial", 11),
                bg=COLORS['background'],
                anchor="w",
                padx=10,
                width=30
            ).grid(row=i+1, column=0, sticky="w", pady=3)
            
            # Date
            tk.Label(
                screenings_frame,
                text=screening.start_time.strftime("%Y-%m-%d"),
                font=("Arial", 11),
                bg=COLORS['background'],
                width=15
            ).grid(row=i+1, column=1, pady=3)
            
            # Time
            tk.Label(
                screenings_frame,
                text=screening.start_time.strftime("%H:%M"),
                font=("Arial", 11),
                bg=COLORS['background'],
                width=15
            ).grid(row=i+1, column=2, pady=3)
            
            # Hall
            tk.Label(
                screenings_frame,
                text=screening.hall.name,
                font=("Arial", 11),
                bg=COLORS['background'],
                width=15
            ).grid(row=i+1, column=3, pady=3)
            
            # Available seats
            tk.Label(
                screenings_frame,
                text=f"{available_seats}/{total_seats}",
                font=("Arial", 11),
                bg=COLORS['background'],
                width=15
            ).grid(row=i+1, column=4, pady=3)
            
            # Select button
            select_button = tk.Button(
                screenings_frame,
                text="Select",
                command=lambda s=screening: select_screening(s),
                font=("Arial", 11),
                bg=COLORS['button'],
                fg=COLORS['button_text'],
                width=10,
                relief="flat"
            )
            select_button.grid(row=i+1, column=5, pady=3)
            
            # Disable button if no seats available
            if available_seats == 0:
                select_button.config(state="disabled", bg=COLORS['unavailable_seat'])
        
        # If no screenings
        if not screenings:
            tk.Label(
                screenings_frame,
                text="No screenings available at the moment.",
                font=("Arial", 12, "italic"),
                bg=COLORS['background'],
                fg="#555555",
                pady=20
            ).grid(row=1, column=0, columnspan=6)
                
        # Back button
        back_button = tk.Button(
            self.main_container,
            text="Back to Main Menu",
            command=self.window.destroy,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20
        )
        back_button.pack(side=tk.BOTTOM, pady=20)
    
    def show_seat_selection(self):
        """Show the seat selection step"""
        self.clear_main_container()
        
        # Create heading with movie info
        movie_info_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        movie_info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            movie_info_frame,
            text=f"Select Seats for: {self.selected_screening.movie.title}",
            font=("Arial", 16, "bold"),
            bg=COLORS['background']
        ).grid(row=0, column=0, columnspan=3, pady=5, sticky="w")
        
        tk.Label(
            movie_info_frame,
            text=f"Date: {self.selected_screening.start_time.strftime('%Y-%m-%d')}",
            font=("Arial", 12),
            bg=COLORS['background']
        ).grid(row=1, column=0, pady=2, sticky="w")
        
        tk.Label(
            movie_info_frame,
            text=f"Time: {self.selected_screening.start_time.strftime('%H:%M')}",
            font=("Arial", 12),
            bg=COLORS['background']
        ).grid(row=1, column=1, pady=2, sticky="w", padx=20)
        
        tk.Label(
            movie_info_frame,
            text=f"Hall: {self.selected_screening.hall.name}",
            font=("Arial", 12),
            bg=COLORS['background']
        ).grid(row=1, column=2, pady=2, sticky="w")
        
        # Try to load layout or create a mock layout
        try:
            # Try to load the layout file if it exists
            layout_name = self.selected_screening.hall.layout_name
            layouts_dir = os.path.join("program", "manager_screen_shit", "layouts")
            file_path = os.path.join(layouts_dir, f"{layout_name}.json")
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    self.seat_layout = json.load(file)
            else:
                # Create a mock layout based on hall size
                rows = 8
                cols = 10
                if self.selected_screening.hall.name == "Hall 2":
                    rows = 12
                    cols = 15
                elif self.selected_screening.hall.name == "VIP Hall":
                    rows = 6
                    cols = 8
                    
                self.seat_layout = []
                for r in range(rows):
                    row = []
                    for c in range(cols):
                        if r < 2:
                            seat_class = 'VIP'
                        elif r < 5:
                            seat_class = 'upper'
                        else:
                            seat_class = 'low'
                        row.append(seat_class)
                    self.seat_layout.append(row)
                    
            # Mock already booked seats
            # For this example, we'll mark the first few seats as booked
            screening_index = next(
                (i for i, s in enumerate(self.mock_data['screenings']) if s.screening_id == self.selected_screening.screening_id), 
                0
            )
            booked_seat_count = screening_index * 2
            booked_seat_ids = []
            for seat in self.selected_screening.hall.seats[:booked_seat_count]:
                booked_seat_ids.append(seat.seat_id)
                
            # Create a frame for the seat layout
            layout_container = tk.Frame(self.main_container, bg=COLORS['background'])
            layout_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Create canvas for the seat layout
            canvas = tk.Canvas(layout_container, highlightthickness=0, bg=COLORS['background'])
            canvas.pack(side="left", expand=True, fill="both")
            
            # Create a frame inside the canvas for the seat layout
            inner_frame = tk.Frame(canvas, bg=COLORS['background'])
            canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")
            
            # Add scrollbars
            h_scrollbar = tk.Scrollbar(layout_container, orient=tk.HORIZONTAL, command=canvas.xview)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            
            v_scrollbar = tk.Scrollbar(layout_container, orient=tk.VERTICAL, command=canvas.yview)
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
            
            # Calculate seat size
            seat_size = 40  # Default size
            padding = 3
            
            # Create seat legend
            legend_frame = tk.Frame(self.main_container, bg=COLORS['background'])
            legend_frame.pack(fill=tk.X, pady=10)
            
            # Available seats
            available_frame = tk.Frame(legend_frame, bg=COLORS['background'])
            available_frame.pack(side=tk.LEFT, padx=20)
            tk.Label(
                available_frame,
                text=" " * 2,
                font=("Arial", 12),
                bg=COLORS['low_seat'],
                width=2,
                relief="solid"
            ).pack(side=tk.LEFT, padx=5)
            tk.Label(
                available_frame,
                text="Available",
                font=("Arial", 10),
                bg=COLORS['background']
            ).pack(side=tk.LEFT)
            
            # Selected seats
            selected_frame = tk.Frame(legend_frame, bg=COLORS['background'])
            selected_frame.pack(side=tk.LEFT, padx=20)
            tk.Label(
                selected_frame,
                text=" " * 2,
                font=("Arial", 12),
                bg=COLORS['selected_seat'],
                width=2,
                relief="solid"
            ).pack(side=tk.LEFT, padx=5)
            tk.Label(
                selected_frame,
                text="Selected",
                font=("Arial", 10),
                bg=COLORS['background']
            ).pack(side=tk.LEFT)
            
            # Booked seats
            booked_frame = tk.Frame(legend_frame, bg=COLORS['background'])
            booked_frame.pack(side=tk.LEFT, padx=20)
            tk.Label(
                booked_frame,
                text=" " * 2,
                font=("Arial", 12),
                bg=COLORS['unavailable_seat'],
                width=2,
                relief="solid"
            ).pack(side=tk.LEFT, padx=5)
            tk.Label(
                booked_frame,
                text="Booked",
                font=("Arial", 10),
                bg=COLORS['background']
            ).pack(side=tk.LEFT)
            
            # Counter for selected seats
            selected_count = tk.StringVar()
            selected_count.set("Selected: 0 seats")
            
            selected_count_label = tk.Label(
                legend_frame,
                textvariable=selected_count,
                font=("Arial", 10, "bold"),
                bg=COLORS['background']
            )
            selected_count_label.pack(side=tk.RIGHT, padx=20)
            
            # Draw the seat layout
            seat_frame = tk.Frame(inner_frame, bg=COLORS['background'])
            seat_frame.pack(padx=20, pady=20)
            
            # Store seat buttons for reference
            self.seat_buttons = []
            
            # Function to handle seat selection
            def toggle_seat(row, col, seat_button, seat_class):
                seat_coords = f"R{row+1}C{col+1}"
                
                # Find the matching seat in our mock data
                hall_id = self.selected_screening.hall.hall_id
                matching_seats = [s for s in self.selected_screening.hall.seats 
                                if s.row == row+1 and s.column == col+1]
                
                if not matching_seats:
                    messagebox.showerror("Error", f"Seat {seat_coords} not found!")
                    return
                
                seat = matching_seats[0]
                    
                # Check if seat is already in selected seats
                if seat in self.selected_seats:
                    # Remove from selection
                    self.selected_seats.remove(seat)
                    # Update button appearance
                    if seat_class == 'low':
                        seat_button.config(bg=COLORS['low_seat'])
                    elif seat_class == 'upper':
                        seat_button.config(bg=COLORS['upper_seat'])
                    elif seat_class == 'VIP':
                        seat_button.config(bg=COLORS['vip_seat'])
                else:
                    # Add to selection
                    self.selected_seats.append(seat)
                    seat_button.config(bg=COLORS['selected_seat'])
                    
                # Update selected count
                selected_count.set(f"Selected: {len(self.selected_seats)} seats")
                
                # Calculate total price
                self.total_price = sum(seat.price for seat in self.selected_seats)
                self.status_label.config(text=f"Status: Selected {len(self.selected_seats)} seats - Total: ${self.total_price:.2f}")
            
            # Draw seats
            for r in range(len(self.seat_layout)):
                for c, seat_class in enumerate(self.seat_layout[r]):
                    if seat_class:
                        # Find the matching seat in our mock data
                        hall_id = self.selected_screening.hall_id
                        matching_seats = [s for s in self.selected_screening.hall.seats 
                                        if s.row == r+1 and s.column == c+1]
                        
                        # Skip if seat doesn't exist in our mock data
                        if not matching_seats:
                            continue
                            
                        db_seat = matching_seats[0]
                            
                        # Check if seat is already booked
                        is_booked = db_seat.seat_id in booked_seat_ids
                        
                        # Set color based on seat class and availability
                        if is_booked:
                            bg_color = COLORS['unavailable_seat']
                        elif seat_class == 'low':
                            bg_color = COLORS['low_seat']
                        elif seat_class == 'upper':
                            bg_color = COLORS['upper_seat']
                        elif seat_class == 'VIP':
                            bg_color = COLORS['vip_seat']
                        
                        # Create the seat button
                        seat_button = tk.Button(
                            seat_frame,
                            text=f"{r+1}-{c+1}",
                            font=("Arial", 8),
                            width=4,
                            height=2,
                            borderwidth=1,
                            relief="solid",
                            bg=bg_color
                        )
                        
                        seat_button.grid(row=r, column=c, padx=padding, pady=padding)
                        
                        # Store the button reference
                        self.seat_buttons.append(seat_button)
                        
                        # Make the seat clickable if not already booked
                        if not is_booked:
                            seat_button.config(
                                command=lambda r=r, c=c, btn=seat_button, sc=seat_class: toggle_seat(r, c, btn, sc)
                            )
                            
                            # Add tooltip with price information
                            tooltip_text = f"Seat {r+1}-{c+1}\n{seat_class.upper()} class\nPrice: ${db_seat.price:.2f}"
                            ToolTip(seat_button, tooltip_text)
                        else:
                            # Add tooltip for booked seats
                            ToolTip(seat_button, f"Seat {r+1}-{c+1}\nAlready booked")
            
            # Update the canvas scroll region
            inner_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading seat layout: {str(e)}")
            self.show_screening_selection()
            return
        
        # Bottom buttons frame
        buttons_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, pady=15)
        
        # Back button
        back_button = tk.Button(
            buttons_frame,
            text="Back to Screenings",
            command=self.show_screening_selection,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20
        )
        back_button.pack(side=tk.LEFT, padx=20)
        
        # Continue button
        def continue_to_details():
            if not self.selected_seats:
                messagebox.showwarning("No Seats Selected", "Please select at least one seat to continue.")
                return
            self.show_customer_details()
            
        continue_button = tk.Button(
            buttons_frame,
            text="Continue to Checkout",
            command=continue_to_details,
            font=("Arial", 12),
            bg=COLORS['button'],
            fg=COLORS['button_text'],
            relief="flat",
            padx=20
        )
        continue_button.pack(side=tk.RIGHT, padx=20)
    
    def show_customer_details(self):
        """Show the customer details form"""
        self.clear_main_container()
        
        # Create heading
        tk.Label(
            self.main_container,
            text="Enter Customer Details",
            font=("Arial", 16, "bold"),
            bg=COLORS['background']
        ).pack(pady=20)
        
        # Create form
        form_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)
        
        # Name field
        tk.Label(
            form_frame,
            text="Full Name *",
            font=("Arial", 12),
            bg=COLORS['background'],
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 2))
        
        name_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Email field
        tk.Label(
            form_frame,
            text="Email",
            font=("Arial", 12),
            bg=COLORS['background'],
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 2))
        
        email_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        email_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Phone field
        tk.Label(
            form_frame,
            text="Phone",
            font=("Arial", 12),
            bg=COLORS['background'],
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 2))
        
        phone_entry = tk.Entry(form_frame, font=("Arial", 12), width=40)
        phone_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Required fields note
        tk.Label(
            form_frame,
            text="* Required field",
            font=("Arial", 10, "italic"),
            bg=COLORS['background'],
            fg="#555555",
            anchor="w"
        ).pack(fill=tk.X, pady=10)
        
        # Order summary
        summary_frame = tk.LabelFrame(
            form_frame,
            text="Order Summary",
            font=("Arial", 12, "bold"),
            bg=COLORS['background']
        )
        summary_frame.pack(fill=tk.X, pady=20)
        
        # Movie title
        tk.Label(
            summary_frame,
            text="Movie:",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=self.selected_screening.movie.title,
            font=("Arial", 11, "bold"),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Date and time
        tk.Label(
            summary_frame,
            text="Date/Time:",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=f"{self.selected_screening.start_time.strftime('%Y-%m-%d %H:%M')}",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Hall
        tk.Label(
            summary_frame,
            text="Hall:",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=self.selected_screening.hall.name,
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Seat count
        tk.Label(
            summary_frame,
            text="Seats:",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=f"{len(self.selected_seats)} seats selected",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Total price
        tk.Label(
            summary_frame,
            text="Total Price:",
            font=("Arial", 11, "bold"),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=f"${self.total_price:.2f}",
            font=("Arial", 11, "bold"),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=4, column=1, sticky="w", padx=10, pady=5)
        
        # Bottom buttons frame
        buttons_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, pady=15)
        
        # Back button
        back_button = tk.Button(
            buttons_frame,
            text="Back to Seat Selection",
            command=self.show_seat_selection,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20
        )
        back_button.pack(side=tk.LEFT, padx=20)
        
        # Checkout button
        def proceed_to_checkout():
            # Validate required fields
            customer_name = name_entry.get().strip()
            if not customer_name:
                messagebox.showwarning("Required Field", "Please enter your full name.")
                return
            
            # Store customer details
            self.customer_name = customer_name
            self.customer_email = email_entry.get().strip()
            self.customer_phone = phone_entry.get().strip()
            
            # Proceed to payment
            self.show_payment()
            
        checkout_button = tk.Button(
            buttons_frame,
            text="Proceed to Payment",
            command=proceed_to_checkout,
            font=("Arial", 12),
            bg=COLORS['button'],
            fg=COLORS['button_text'],
            relief="flat",
            padx=20
        )
        checkout_button.pack(side=tk.RIGHT, padx=20)
    
    def process_payment(self, payment_frame, selected_method):
        """Process payment without using database sessions"""
        # Show a processing indicator
        processing_label = tk.Label(
            payment_frame,
            text="Processing payment...",
            font=("Arial", 12, "italic"),
            bg=COLORS['background']
        )
        processing_label.pack(pady=10)
        payment_frame.update()
        
        # Simulate processing delay
        self.window.after(2000)
        processing_label.destroy()
        
        # Create a mock booking ID
        import uuid
        booking_id = str(uuid.uuid4())
        
        # Show confirmation
        self.show_confirmation(booking_id)

    def show_payment(self):
        """Show the payment screen"""
        self.clear_main_container()
        
        # Create heading
        tk.Label(
            self.main_container,
            text="Payment",
            font=("Arial", 16, "bold"),
            bg=COLORS['background']
        ).pack(pady=20)
        
        # Create payment frame
        payment_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        payment_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)
        
        # Order summary (similar to previous step)
        summary_frame = tk.LabelFrame(
            payment_frame,
            text="Order Summary",
            font=("Arial", 12, "bold"),
            bg=COLORS['background']
        )
        summary_frame.pack(fill=tk.X, pady=20)
        
        # Movie title
        tk.Label(
            summary_frame,
            text="Movie:",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=self.selected_screening.movie.title,
            font=("Arial", 11, "bold"),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Date and time
        tk.Label(
            summary_frame,
            text="Date/Time:",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=f"{self.selected_screening.start_time.strftime('%Y-%m-%d %H:%M')}",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Customer info
        tk.Label(
            summary_frame,
            text="Customer:",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=self.customer_name,
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Seats
        seat_labels = []
        for seat in self.selected_seats:
            seat_labels.append(f"Row {seat.row}, Col {seat.column}")
        
        tk.Label(
            summary_frame,
            text="Seats:",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        seats_text = ", ".join(seat_labels)
        tk.Label(
            summary_frame,
            text=seats_text if len(seats_text) < 50 else f"{len(self.selected_seats)} seats",
            font=("Arial", 11),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Total price
        tk.Label(
            summary_frame,
            text="Total Price:",
            font=("Arial", 11, "bold"),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(
            summary_frame,
            text=f"${self.total_price:.2f}",
            font=("Arial", 11, "bold"),
            bg=COLORS['background'],
            anchor="w"
        ).grid(row=4, column=1, sticky="w", padx=10, pady=5)
        
        # Payment methods
        methods_frame = tk.LabelFrame(
            payment_frame,
            text="Payment Method",
            font=("Arial", 12, "bold"),
            bg=COLORS['background']
        )
        methods_frame.pack(fill=tk.X, pady=20)
        
        # Payment method selection
        selected_method = tk.StringVar(value="credit_card")
        
        tk.Radiobutton(
            methods_frame,
            text="Credit Card",
            variable=selected_method,
            value="credit_card",
            font=("Arial", 11),
            bg=COLORS['background']
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Radiobutton(
            methods_frame,
            text="Debit Card",
            variable=selected_method,
            value="debit_card",
            font=("Arial", 11),
            bg=COLORS['background']
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Radiobutton(
            methods_frame,
            text="Pay at Counter",
            variable=selected_method,
            value="counter",
            font=("Arial", 11),
            bg=COLORS['background']
        ).pack(anchor="w", padx=10, pady=5)
        
        # Payment details frame (will show based on selection)
        payment_details = tk.Frame(payment_frame, bg=COLORS['background'])
        payment_details.pack(fill=tk.X, pady=10)
        
        # Bottom buttons frame
        buttons_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, pady=15)
        
        # Back button
        back_button = tk.Button(
            buttons_frame,
            text="Back to Customer Details",
            command=self.show_customer_details,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20
        )
        back_button.pack(side=tk.LEFT, padx=20)
        
        # Complete payment button
        complete_button = tk.Button(
            buttons_frame,
            text="Complete Payment",
            command=lambda: self.process_payment(payment_frame, selected_method),
            font=("Arial", 12),
            bg=COLORS['button'],
            fg=COLORS['button_text'],
            relief="flat",
            padx=20
        )
        complete_button.pack(side=tk.RIGHT, padx=20)
    
    def show_confirmation(self, booking_id):
        """Show booking confirmation"""
        self.clear_main_container()
        
        # Create success frame with green background
        success_frame = tk.Frame(self.main_container, bg="#d4edda", padx=20, pady=20)
        success_frame.pack(fill=tk.X, pady=30, padx=50)
        
        # Success icon (checkmark)
        tk.Label(
            success_frame,
            text="✓",
            font=("Arial", 48),
            fg="#155724",
            bg="#d4edda"
        ).pack()
        
        # Success message
        tk.Label(
            success_frame,
            text="Booking Confirmed!",
            font=("Arial", 18, "bold"),
            fg="#155724",
            bg="#d4edda"
        ).pack(pady=10)
        
        # Booking ID
        tk.Label(
            success_frame,
            text=f"Booking ID: {booking_id}",
            font=("Arial", 12),
            fg="#155724",
            bg="#d4edda"
        ).pack(pady=5)
        
        # Additional info
        info_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        info_frame.pack(fill=tk.X, pady=20, padx=50)
        
        tk.Label(
            info_frame,
            text="Booking Details",
            font=("Arial", 14, "bold"),
            bg=COLORS['background']
        ).pack(anchor="w", pady=10)
        
        # Movie details
        movie_frame = tk.Frame(info_frame, bg=COLORS['background'])
        movie_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            movie_frame,
            text="Movie:",
            font=("Arial", 12, "bold"),
            bg=COLORS['background'],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            movie_frame,
            text=self.selected_screening.movie.title,
            font=("Arial", 12),
            bg=COLORS['background'],
            anchor="w"
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Date/Time
        datetime_frame = tk.Frame(info_frame, bg=COLORS['background'])
        datetime_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            datetime_frame,
            text="Date/Time:",
            font=("Arial", 12, "bold"),
            bg=COLORS['background'],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            datetime_frame,
            text=self.selected_screening.start_time.strftime('%Y-%m-%d %H:%M'),
            font=("Arial", 12),
            bg=COLORS['background'],
            anchor="w"
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Customer
        customer_frame = tk.Frame(info_frame, bg=COLORS['background'])
        customer_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            customer_frame,
            text="Customer:",
            font=("Arial", 12, "bold"),
            bg=COLORS['background'],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            customer_frame,
            text=self.customer_name,
            font=("Arial", 12),
            bg=COLORS['background'],
            anchor="w"
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Seat count
        seats_frame = tk.Frame(info_frame, bg=COLORS['background'])
        seats_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            seats_frame,
            text="Seats:",
            font=("Arial", 12, "bold"),
            bg=COLORS['background'],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            seats_frame,
            text=f"{len(self.selected_seats)} seats",
            font=("Arial", 12),
            bg=COLORS['background'],
            anchor="w"
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Total price
        price_frame = tk.Frame(info_frame, bg=COLORS['background'])
        price_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            price_frame,
            text="Total Price:",
            font=("Arial", 12, "bold"),
            bg=COLORS['background'],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            price_frame,
            text=f"${self.total_price:.2f}",
            font=("Arial", 12),
            bg=COLORS['background'],
            anchor="w"
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Note about tickets
        note_frame = tk.Frame(self.main_container, bg="#e2e3e5", padx=15, pady=15)
        note_frame.pack(fill=tk.X, pady=20, padx=50)
        
        tk.Label(
            note_frame,
            text="Note: Please check your email for e-tickets or collect physical tickets at the counter.",
            font=("Arial", 11),
            bg="#e2e3e5",
            fg="#383d41",
            wraplength=600,
            justify="left"
        ).pack(anchor="w")
        
        # Buttons
        buttons_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # New booking button
        new_booking_button = tk.Button(
            buttons_frame,
            text="Make Another Booking",
            command=self.show_screening_selection,
            font=("Arial", 12),
            bg=COLORS['button'],
            fg=COLORS['button_text'],
            relief="flat",
            padx=20
        )
        new_booking_button.pack(side=tk.LEFT, padx=50)
        
        # Exit button
        exit_button = tk.Button(
            buttons_frame,
            text="Back to Main Menu",
            command=self.window.destroy,
            font=("Arial", 12),
            bg="#6c757d",
            fg="white",
            relief="flat",
            padx=20
        )
        exit_button.pack(side=tk.RIGHT, padx=50)

# Simple tooltip implementation (same as in seat_layout.py)
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip, 
            text=self.text, 
            bg="#ffffcc", 
            relief="solid", 
            borderwidth=1,
            font=("Arial", 9),
            padx=5,
            pady=2
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# Run the booking process if this script is run directly
if __name__ == "__main__":
    app = BookingProcess()
    app.window.mainloop()