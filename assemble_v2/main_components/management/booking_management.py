import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Toplevel, Text, Button
import re
from database.database_settings import SessionLocal
from main_components.services.booking_service import BookingService
from main_components.services.ticket_service import TicketService
from main_components.services.screening_service import ScreeningService
from main_components.models import SeatAvailability, Seat, Booking, Screening
import datetime
import os
import subprocess
import tempfile
import platform
from main_components.management.booking_events_manager import BookingEventsManager
import webbrowser

class BookingManagement(tk.Frame):
    def __init__(self, parent, cinema_id, user, callback=None):
        super().__init__(parent)
        self.user = user
        self.callback = callback
        self.cinema_id = cinema_id
        self.session = SessionLocal()
        self.booking_service = BookingService(self.session, TicketService(self.session))
        self.screening_service = ScreeningService(self.session)
        self.setup_ui()
        self.sort_order = {} # Store the current sort order for each column
        self.event_manager = BookingEventsManager()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tk.Label(main_frame, text="Booking Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        # Booking Creation Frame
        booking_creation_frame = ttk.Frame(main_frame, padding="10")
        booking_creation_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        tk.Label(booking_creation_frame, text="Create Booking").pack()
        ttk.Button(booking_creation_frame, text="Create Booking", command=self.create_booking_ui).pack()

        # Booking Cancellation Frame
        booking_cancellation_frame = ttk.Frame(main_frame, padding="10")
        booking_cancellation_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        tk.Label(booking_cancellation_frame, text="Cancel Booking").pack()
        ttk.Button(booking_cancellation_frame, text="Cancel Booking", command=self.cancel_booking_ui).pack()

        # Booking View Frame
        booking_view_frame = ttk.Frame(main_frame, padding="10")
        booking_view_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        tk.Label(booking_view_frame, text="View Bookings").pack()
        ttk.Button(booking_view_frame, text="View Bookings", command=self.view_bookings_ui).pack()

    def create_booking_ui(self):
        self.create_window = tk.Toplevel(self)
        self.create_window.title("Create Booking")

        # Screening Selection
        tk.Label(self.create_window, text="Select Screening:", anchor='w').grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        if self.cinema_id == "all":
            screenings = self.screening_service.get_all_screenings()
        else:
            screenings = self.screening_service.get_all_screenings_for_cinema(self.cinema_id)

        # Sort screenings by date and time
        def screening_sort_key(screening):
            date_str = screening.date
            time_str = screening.start_time
            try:
                datetime_obj = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                return datetime_obj
            except ValueError:
                return datetime.datetime.min # Put invalid dates at the beginning

        screenings.sort(key=screening_sort_key)

        # Truncate film name and adjust width directly in list comprehension
        screening_names = [
        f"{s.film.name[:30] + '...' if len(s.film.name) > 30 else s.film.name} ({s.film_id}) - {s.date.strftime('%Y-%m-%d')} {s.start_time.strftime('%H:%M')} - Cinema {s.cinema.name if s.cinema else 'Unknown'}"
        for s in screenings
    ]

        self.screening_combobox = ttk.Combobox(self.create_window, values=screening_names, width=60)
        self.screening_combobox.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.screening_combobox.bind("<<ComboboxSelected>>", self.update_seat_selection)

        # Seat Selection Frame
        self.seat_frame = ttk.Frame(self.create_window)
        self.seat_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        # labels for displaying selected seats:
        self.selected_seats_label = ttk.Label(self.create_window, text="Selected Seats: ")
        self.selected_seats_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.selected_seats_display = ttk.Label(self.create_window, text="")
        self.selected_seats_display.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Store a reference to the label for updating
        self.selected_seats_label_ui = self.selected_seats_display

        # Customer Details
        tk.Label(self.create_window, text="Customer Name:", anchor='w').grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        self.name_entry = ttk.Entry(self.create_window)
        self.name_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

        tk.Label(self.create_window, text="Customer Email:", anchor='w').grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        self.email_entry = ttk.Entry(self.create_window)
        self.email_entry.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

        tk.Label(self.create_window, text="Customer Phone:", anchor='w').grid(row=5, column=0, sticky='ew', padx=5, pady=5)
        self.phone_entry = ttk.Entry(self.create_window)
        self.phone_entry.grid(row=5, column=1, sticky='ew', padx=5, pady=5)

        # Confirm Booking Button
        confirm_button = ttk.Button(self.create_window, text="Confirm Booking", command=self.confirm_booking)
        confirm_button.grid(row=6, column=0, columnspan=2, pady=10)
        confirm_button.bind("<Enter>", lambda event: confirm_button.config(cursor="hand2")) #change cursor on hover.
        confirm_button.bind("<Leave>", lambda event: confirm_button.config(cursor=""))

        # Initialize the seat selection UI and display seats.
        self.update_seat_selection(None) # Call update_seat_selection at the end.


    def update_seat_selection(self, event):
        self.clear_seat_frame()
        screening_name = self.screening_combobox.get()
        if self.cinema_id == "all":
            screenings = self.screening_service.get_all_screenings()
        else:
            screenings = self.screening_service.get_all_screenings_for_cinema(self.cinema_id)

        selected_screening = next((s for s in screenings if f"{s.film.name[:30] + '...' if len(s.film.name) > 30 else s.film.name} ({s.film_id}) - {s.date.strftime('%Y-%m-%d')} {s.start_time.strftime('%H:%M')} - Cinema {s.cinema.name if s.cinema else 'Unknown'}" == screening_name), None)

        if selected_screening:

            # Reset selected seats when a new screening is selected.
            self.selected_seats = [] if hasattr(self, 'selected_seats') else []
            self.update_selected_seats_display() #update display to show empty seats.

            seats = self.session.query(Seat).filter(
            Seat.cinema_id == (selected_screening.cinema_id if self.cinema_id != 'all' else selected_screening.cinema_id),
            Seat.screen_id == selected_screening.screen_id,).all()

            # Sort available_seats by Seatnumber
            seats.sort(key=lambda seat: int(seat.seat_id.split('_')[-1])) # Get seatnumber

            self.seat_buttons = {}  # Store seat buttons for color changes
            row = 0
            col = 0
            for seat in seats:
                #check seat availability.
                seat_availability_obj = self.session.query(SeatAvailability).filter(
                SeatAvailability.seat_id == seat.seat_id,
                SeatAvailability.screening_id == selected_screening.screening_id,).first()

                if seat_availability_obj and seat_availability_obj.seat_availability == 1:
                    button_style = "Available.TButton"  # green
                else:
                    button_style = "Unavailable.TButton"  # red

                button = ttk.Button(self.seat_frame, text=seat.seat_id, command=lambda s_id=seat.seat_id: self.select_seat(s_id, selected_screening.screening_id), style=button_style)
                button.grid(row=row, column=col, padx=5, pady=5) 
                self.seat_buttons[seat.seat_id] = button
                col += 1
                if col > 10: # adjust the number of columns
                    col = 0
                    row += 1


    def select_seat(self, seat_id, screening_id):
        seat_availability_obj = self.session.query(SeatAvailability).filter(
        SeatAvailability.seat_id == seat_id,
        SeatAvailability.screening_id == screening_id,).first()

        if seat_availability_obj and seat_availability_obj.seat_availability == 0:
            # Seat is unavailable (red), prevent selection
            return
    
        if not hasattr(self, 'selected_seats'):
            self.selected_seats = []
        if seat_id not in self.selected_seats:
            self.selected_seats.append(seat_id)
            self.seat_buttons[seat_id].config(style="Selected.TButton")  # Change color
        else:
            self.selected_seats.remove(seat_id)
            if seat_id in self.seat_buttons:
                if seat_availability_obj and seat_availability_obj.seat_availability == 1:
                    self.seat_buttons[seat_id].config(style="Available.TButton")  # revert to green
                else:
                    self.seat_buttons[seat_id].config(style="Unavailable.TButton")  # revert to red
        
        # Update the selected seats display
        self.update_selected_seats_display()

    def update_selected_seats_display(self):
        if hasattr(self, 'selected_seats') and hasattr(self, 'selected_seats_label_ui'):
            self.selected_seats_label_ui.config(text=", ".join(self.selected_seats))
        elif hasattr(self, 'selected_seats_label_ui'):
            self.selected_seats_label_ui.config(text="")
        

    def is_valid_screening(self, screening_name):
        if self.cinema_id == "all":
            screenings = self.screening_service.get_all_screenings()
        else:
            screenings = self.screening_service.get_all_screenings_for_cinema(self.cinema_id)
        selected_screening = next((s for s in screenings if f"{s.film.name[:30] + '...' if len(s.film.name) > 30 else s.film.name} ({s.film_id}) - {s.date.strftime('%Y-%m-%d')} {s.start_time.strftime('%H:%M')} - Cinema {s.cinema.name if s.cinema else 'Unknown'}" == screening_name), None)
        return selected_screening is not None

    def is_valid_name(self, name):
        return isinstance(name, str) and name.strip() != ""

    def is_valid_email(self, email):
        return isinstance(email, str) and re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_valid_phone(self, phone):
        return isinstance(phone, str) and re.match(r"^\d{10}$", phone)

    def is_valid_seats(self, seat_ids):
        return isinstance(seat_ids, list) and len(seat_ids) > 0


    def confirm_booking(self):
        screening_name = self.screening_combobox.get()
        customer_name = self.name_entry.get()
        customer_email = self.email_entry.get()
        customer_phone = self.phone_entry.get()
        seat_ids = self.selected_seats if hasattr(self, 'selected_seats') else []

        if not self.is_valid_screening(screening_name):
            messagebox.showerror("Error", "Invalid screening selection.")
            return

        if not self.is_valid_name(customer_name):
            messagebox.showerror("Error", "Please enter a customer name.")
            return

        if not self.is_valid_email(customer_email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        if not self.is_valid_phone(customer_phone):
            messagebox.showerror("Error", "Please enter a valid 10-digit phone number.")
            return

        if not self.is_valid_seats(seat_ids):
            messagebox.showerror("Error", "Please select at least one seat.")
            return

        # Extract screening ID
        screening_id = None
        if self.cinema_id == "all":
            screenings = self.screening_service.get_all_screenings()
            selected_screening = next((s for s in screenings if f"{s.film.name[:30] + '...' if len(s.film.name) > 30 else s.film.name} ({s.film_id}) - {s.date.strftime('%Y-%m-%d')} {s.start_time.strftime('%H:%M')} - Cinema {s.cinema.name if s.cinema else 'Unknown'}" == screening_name), None)
        else:
            screenings = self.screening_service.get_all_screenings_for_cinema(self.cinema_id)
            selected_screening = next((s for s in screenings if f"{s.film.name[:30] + '...' if len(s.film.name) > 30 else s.film.name} ({s.film_id}) - {s.date.strftime('%Y-%m-%d')} {s.start_time.strftime('%H:%M')} - Cinema {s.cinema.name if s.cinema else 'Unknown'}" == screening_name), None)

        screening_id = selected_screening.screening_id

        # confirmation dialog:
        confirmation_message = f"Confirm booking:\n\n" \
                               f"Screening: {screening_name}\n" \
                               f"Customer: {customer_name}\n" \
                               f"Email: {customer_email}\n" \
                               f"Phone: {customer_phone}\n" \
                               f"Seats: {', '.join(seat_ids)}"
        
        if messagebox.askyesno("Confirm Booking", confirmation_message): 
            try:
                booking_objects = self.booking_service.create_booking(seat_ids, customer_name, customer_email, customer_phone, screening_id)
                if booking_objects is None:
                    messagebox.showerror("Error", "Booking creation failed. Please check the logs for details.")
                    return

                messagebox.showinfo("Success", "Booking created successfully.")

                # Generate and print receipt for the booking
                if booking_objects: #check there are bookings.
                    self.generate_receipt(booking_objects[0].booking_id)

                # Extract booking IDs
                booking_ids = [booking.booking_id for booking in booking_objects]
            
                # Log booking event
                booking_data = {
                    "seat_ids": seat_ids,
                    "customer_name": customer_name,
                    "customer_email": customer_email,
                    "customer_phone": customer_phone,
                    "screening_id": screening_id
                }
                self.event_manager.log_event(booking_ids, self.user.user_id, "booking", booking_data)

            except ValueError as e:
                messagebox.showerror("Error", str(e))
        self.create_window.destroy() #destroy the window.




    def cancel_booking_ui(self):
        cancel_window = tk.Toplevel(self)
        cancel_window.title("Cancel Booking")

        # Filter input fields
        filter_frame = tk.Frame(cancel_window)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Name:").pack(side=tk.LEFT)
        name_entry = tk.Entry(filter_frame)
        name_entry.pack(side=tk.LEFT)

        tk.Label(filter_frame, text="Email:").pack(side=tk.LEFT)
        email_entry = tk.Entry(filter_frame)
        email_entry.pack(side=tk.LEFT)

        tree = ttk.Treeview(cancel_window, columns=("Booking ID", "Customer Name", "Customer Email", "Customer Phone", "Screening", "Seat ID"), show="headings") #Add customer email, phone.
        tree.heading("Booking ID", text="Booking ID")
        tree.heading("Customer Name", text="Customer Name")
        tree.heading("Customer Email", text="Customer Email") 
        tree.heading("Customer Phone", text="Customer Phone") 
        tree.heading("Screening", text="Screening")
        tree.heading("Seat ID", text="Seat ID")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        def select_for_cancellation(event):
            selected_items = tree.selection()
            if selected_items:
                item = selected_items[0]
                booking_id = tree.item(item, "values")[0]  # Get booking ID from the selected row
                if messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel booking {booking_id}?"):
                    try:
                        self.booking_service.cancel_booking(booking_id)
                        messagebox.showinfo("Success", f"Booking ID {booking_id} canceled successfully.")
                        refresh_treeview()  # Refresh the treeview after cancellation

                        # Log cancellation event
                        cancellation_data = {"cancellation_reason": "User Initiated Cancellation"} 
                        self.event_manager.log_event(booking_id, self.user.user_id, "cancellation", cancellation_data) 
                    
                        cancel_window.destroy()  # Destroy the cancel_window after successful cancellation

                    except ValueError as e:
                        # Check for the specific error related to screening start time
                        if "cannot be cancelled as the screening has already started" in str(e):
                            messagebox.showerror("Error", str(e))
                        else:
                            messagebox.showerror("Error", str(e))
                    except Exception as e:
                        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        def refresh_treeview():
            for item in tree.get_children():
                tree.delete(item)  # Clear the treeview

            name_filter = name_entry.get()
            email_filter = email_entry.get()

            query = self.session.query(Booking)

            # Apply cinema_id filter based on self.cinema_id
            if self.cinema_id != "all":
                query = query.join(SeatAvailability).join(Screening).filter(Screening.cinema_id == self.cinema_id)


            if name_filter and email_filter:
                query = query.filter(
                    Booking.customer_name.ilike(f"%{name_filter}%"),
                    Booking.customer_email.ilike(f"%{email_filter}%")
                )
            elif name_filter:
                query = query.filter(Booking.customer_name.ilike(f"%{name_filter}%"))
            elif email_filter:
                query = query.filter(Booking.customer_email.ilike(f"%{email_filter}%"))

            bookings = query.all()
            selected_items = []  # List to store the item IDs of selected bookings

            for booking in bookings:
                seat_availability = self.session.query(SeatAvailability).filter(
                    SeatAvailability.booking_id == booking.booking_id,
                    SeatAvailability.seat_id == booking.seat_id
                ).first()

                screening_info = "N/A"
                if seat_availability and seat_availability.screening_id:
                    screening = self.session.query(Screening).filter(Screening.screening_id == seat_availability.screening_id).first()
                    if screening:
                        screening_info = f"{screening.film.name[:30] + '...' if len(screening.film.name) > 30 else screening.film.name} ({screening.film_id}) - {screening.date.strftime('%Y-%m-%d')} {screening.start_time.strftime('%H:%M')} - Cinema {screening.cinema.cinema_id if screening.cinema else 'Unknown'}"

                item_id = tree.insert("", tk.END, values=(booking.booking_id, booking.customer_name, booking.customer_email, booking.customer_phone, screening_info, booking.seat_id))
                selected_items.append(item_id)  # Add the item ID to the list

            if selected_items:  # Only select if there are items
                tree.selection_set(selected_items)

        # Initial population of the treeview (with cinema_id filter)
        query = self.session.query(Booking)
        if self.cinema_id != "all":
            query = query.join(SeatAvailability).join(Screening).filter(Screening.cinema_id == self.cinema_id)

        bookings = query.all()
        for booking in bookings:
            seat_availability = self.session.query(SeatAvailability).filter(
                SeatAvailability.booking_id == booking.booking_id,
                SeatAvailability.seat_id == booking.seat_id
            ).first()

            screening_info = "N/A"
            if seat_availability and seat_availability.screening_id:
                screening = self.session.query(Screening).filter(Screening.screening_id == seat_availability.screening_id).first()
                if screening:
                    screening_info = f"{screening.film.name[:30] + '...' if len(screening.film.name) > 30 else screening.film.name} ({screening.film_id}) - {screening.date.strftime('%Y-%m-%d')} {screening.start_time.strftime('%H:%M')} - Cinema {screening.cinema.cinema_id if screening.cinema else 'Unknown'}"

            tree.insert("", tk.END, values=(booking.booking_id, booking.customer_name, booking.customer_email, booking.customer_phone, screening_info, booking.seat_id))

        # Refresh button
        refresh_button = tk.Button(cancel_window, text="Search", command=refresh_treeview)
        refresh_button.pack(pady=5)

        tree.bind("<Double-1>", select_for_cancellation)
    
    def view_bookings_ui(self):
        view_window = tk.Toplevel(self)
        view_window.title("View Bookings")

        filter_frame = ttk.Frame(view_window)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Name:").pack(side=tk.LEFT)
        name_entry = ttk.Entry(filter_frame)
        name_entry.pack(side=tk.LEFT)

        tk.Label(filter_frame, text="Email:").pack(side=tk.LEFT)
        email_entry = ttk.Entry(filter_frame)
        email_entry.pack(side=tk.LEFT)



        def apply_filter():
            refresh_treeview()

        ttk.Button(filter_frame, text="Apply Filter", command=apply_filter).pack(side=tk.LEFT)

        tree = ttk.Treeview(view_window, columns=("Booking ID", "Customer Name", "Customer Email", "Customer Phone", "Screening", "Seat ID"), show="headings")
        tree.heading("Booking ID", text="Booking ID", command=lambda col="Booking ID": self.sort_column(tree, col, False))
        tree.heading("Customer Name", text="Customer Name", command=lambda col="Customer Name": self.sort_column(tree, col, False))
        tree.heading("Customer Email", text="Customer Email", command=lambda col="Customer Email": self.sort_column(tree, col, False))
        tree.heading("Customer Phone", text="Customer Phone", command=lambda col="Customer Phone": self.sort_column(tree, col, False))
        tree.heading("Screening", text="Screening", command=lambda col="Screening": self.sort_column(tree, col, False))
        tree.heading("Seat ID", text="Seat ID", command=lambda col="Seat ID": self.sort_column(tree, col, False))
        tree.pack(fill=tk.BOTH, expand=True)

        def refresh_treeview():
            for item in tree.get_children():
                tree.delete(item)

            name_filter = name_entry.get()
            email_filter = email_entry.get()

            query = self.session.query(Booking)

            # Apply cinema_id filter based on self.cinema_id
            if self.cinema_id != "all":
                query = query.join(SeatAvailability).join(Screening).filter(Screening.cinema_id == self.cinema_id)

            if name_filter and email_filter:
                query = query.filter(
                    Booking.customer_name.ilike(f"%{name_filter}%"),
                    Booking.customer_email.ilike(f"%{email_filter}%")
                )
            elif name_filter:
                query = query.filter(Booking.customer_name.ilike(f"%{name_filter}%"))
            elif email_filter:
                query = query.filter(Booking.customer_email.ilike(f"%{email_filter}%"))

            bookings = query.all()

            if not bookings:
                messagebox.showinfo("Info", "No bookings found.")
                return
            
            selected_items = [] #Store item IDs.

            for booking in bookings:
                seat_availability = self.session.query(SeatAvailability).filter(
                    SeatAvailability.booking_id == booking.booking_id,
                    SeatAvailability.seat_id == booking.seat_id
                ).first()

                if seat_availability:
                    screening = self.session.query(Screening).filter(Screening.screening_id == seat_availability.screening_id).first()
                    screening_info = f"{screening.film.name[:30] + '...' if len(screening.film.name) > 30 else screening.film.name} ({screening.film_id}) - {screening.date.strftime('%Y-%m-%d')} {screening.start_time.strftime('%H:%M')} - Cinema {screening.cinema.cinema_id if screening.cinema else 'Unknown'}" if screening else "N/A"
                else:
                    screening_info = "N/A"

                item_id = tree.insert("", tk.END, values=(booking.booking_id, booking.customer_name, booking.customer_email, booking.customer_phone, screening_info, booking.seat_id))
                selected_items.append(item_id) #Add item id to list.
            if selected_items:
                tree.selection_set(selected_items)
        
        # Initial population of the treeview (with cinema_id filter)
        query = self.session.query(Booking)
        if self.cinema_id != "all":
            query = query.join(SeatAvailability).join(Screening).filter(Screening.cinema_id == self.cinema_id)

        bookings = query.all()
        for booking in bookings:
            seat_availability = self.session.query(SeatAvailability).filter(
                SeatAvailability.booking_id == booking.booking_id,
                SeatAvailability.seat_id == booking.seat_id
            ).first()

            screening_info = "N/A"
            if seat_availability and seat_availability.screening_id:
                screening = self.session.query(Screening).filter(Screening.screening_id == seat_availability.screening_id).first()
                if screening:
                    screening_info = f"{screening.film.name[:30] + '...' if len(screening.film.name) > 30 else screening.film.name} ({screening.film_id}) - {screening.date.strftime('%Y-%m-%d')} {screening.start_time.strftime('%H:%M')} - Cinema {screening.cinema.cinema_id if screening.cinema else 'Unknown'}"

            tree.insert("", tk.END, values=(booking.booking_id, booking.customer_name, booking.customer_email, booking.customer_phone, screening_info, booking.seat_id))
            

    def sort_column(self, tree, col, reverse):
        bookings = [(tree.set(item, col), item) for item in tree.get_children("")]
        bookings.sort(reverse=reverse)

        for index, (val, item) in enumerate(bookings):
            tree.move(item, '', index)

        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))


    def generate_receipt(self, booking_id):
        try:
            bookings = self.session.query(Booking).filter(Booking.booking_id == booking_id).all()
            if not bookings:
                messagebox.showerror("Error", "Booking not found.")
                return

            receipt_content = f"""
            <html>
            <head>
                <title>Booking Receipt</title>
                <style>
                    body {{ font-family: sans-serif; }}
                    .receipt {{ width: 600px; margin: 20px auto; border: 1px solid #ccc; padding: 20px; }}
                    .title {{ text-align: center; font-size: 20px; margin-bottom: 10px; }}
                    .section {{ margin-bottom: 10px; }}
                    .seats {{ list-style-type: none; padding: 0; }}
                    .seats li {{ margin-bottom: 5px; }}
                </style>
            </head>
            <body>
                <div class="receipt">
                    <div class="title">Booking Receipt</div>
                    <div class="section"><strong>Booking ID:</strong> {booking_id}</div>
                    <div class="section"><strong>Customer Name:</strong> {bookings[0].customer_name}</div>
                    <div class="section"><strong>Customer Email:</strong> {bookings[0].customer_email}</div>
                    <div class="section"><strong>Customer Phone:</strong> {bookings[0].customer_phone}</div>
                    <div class="section"><strong>Seats:</strong>
                        <ul class="seats">
            """

            # Add seat IDs and screening info to the receipt
            for booking in bookings:
                seat_availability = self.session.query(SeatAvailability).filter(
                    SeatAvailability.booking_id == booking.booking_id,
                    SeatAvailability.seat_id == booking.seat_id
                ).first()

                screening = self.session.query(Screening).filter(Screening.screening_id == seat_availability.screening_id).first()
                screening_info = f"{screening.film.name[:30] + '...' if len(screening.film.name) > 30 else screening.film.name} ({screening.film_id}) - {screening.date.strftime('%Y-%m-%d')} {screening.start_time.strftime('%H:%M')} - Cinema {screening.cinema.cinema_id if screening.cinema else 'Unknown'}"

                receipt_content += f"    Seat: {booking.seat_id} - Screening: {screening_info}\n"

            receipt_content += f"""
                Booking Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """

            receipt_content += f"""
                        </ul>
                    </div>
                    <div class="section"><strong>Booking Date:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
            </body>
            </html>
            """

            # Preview Window
            preview_window = Toplevel(self)
            preview_window.title("Receipt Preview")

            text_widget = Text(preview_window, wrap="word", width=60, height=20)
            text_widget.insert("1.0", receipt_content)
            text_widget.config(state="disabled")
            text_widget.pack(padx=10, pady=10)

            def print_receipt():
                with tempfile.NamedTemporaryFile(mode='w+t', delete=False, suffix=".html") as temp_file:
                    temp_file.write(receipt_content)
                    temp_filename = temp_file.name
                    temp_file.close() #close the file, so webbrowser can access it

                os_name = platform.system()
                try:
                    if os_name == "Windows":
                        webbrowser.open_new_tab("file://" + os.path.abspath(temp_filename))
                    elif os_name == "Darwin":
                        subprocess.run(["lp", temp_filename], check=True)
                    elif os_name == "Linux":
                        subprocess.run(["lp", temp_filename], check=True)
                    else:
                        messagebox.showerror("Error", "Printing is not supported on this OS.")
                        return
                except Exception as e:
                    messagebox.showerror("Error", f"Printing failed: {e}")
                    return

                preview_window.destroy()
                messagebox.showinfo("Receipt Printed", "Please print from your browser.")

                try:
                    os.remove(temp_filename)
                except:
                    pass #do nothing if the file can not be removed.


            print_button = Button(preview_window, text="Print", command=print_receipt)
            print_button.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")











    def clear_seat_frame(self):
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")