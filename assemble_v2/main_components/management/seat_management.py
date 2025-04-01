import tkinter as tk
from tkinter import ttk, messagebox
from database.database_settings import SessionLocal
from main_components.services.seat_service import SeatService
from main_components.services.screen_service import ScreenService
from main_components.services.cinema_service import CinemaService

class SeatManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, cinema_id, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.cinema_id = cinema_id
        self.session = SessionLocal()
        self.seat_service = SeatService(self.session)
        self.screen_service = ScreenService(self.session)
        self.cinema_service = CinemaService(self.session)
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("LightGreen.TFrame", background="lightgreen")
        style.configure("LightYellow.TFrame", background="lightyellow")
        style.configure("LightBlue.TFrame", background="lightblue")

        main_frame = ttk.Frame(self, padding="20", style="LightGreen.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tk.Label(main_frame, text="Seat Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        self.seat_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.seat_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_seats()

    def manage_seats(self):
        self.clear_seat_frame()
        self.seat_list = ttk.Treeview(
            self.seat_frame,
            columns=("Seat ID", "Screen ID", "Cinema ID", "Seat Type"),
            show="headings",
        )
        self.seat_list.heading("Seat ID", text="Seat ID")
        self.seat_list.heading("Screen ID", text="Screen ID")
        self.seat_list.heading("Cinema ID", text="Cinema ID")
        self.seat_list.heading("Seat Type", text="Seat Type")
        self.seat_list.pack(expand=True, fill="both")

        if self.cinema_id == "all":
            seats = self.seat_service.get_all_seats()
        else:
            seats = self.seat_service.get_seats_by_cinema(self.cinema_id)

        for seat in seats:
            self.seat_list.insert(
                "",
                tk.END,
                values=(seat.seat_id, seat.screen_id, seat.cinema_id, seat.seat_type),
            )

        action_frame = ttk.Frame(self.seat_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add Seat", command=self.add_seat).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update Seat", command=self.update_seat).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Remove Seat", command=self.remove_seat).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse Seat", command=self.browse_seat).pack(side=tk.LEFT, padx=5)

        self.seat_list.bind("<ButtonRelease-1>", self.select_seat)
        self.selected_seat_id = None
        self.selected_screen_id = None
        self.selected_cinema_id = None
        self.selected_seat_type = None
        self.seat_frame.update()

    def select_seat(self, event):
        selection = self.seat_list.selection()
        if selection:
            item = selection[0]
            values = self.seat_list.item(item, "values")
            self.selected_seat_id = values[0]
            self.selected_screen_id = values[1]
            self.selected_cinema_id = values[2]
            self.selected_seat_type = values[3]
        else:
            self.selected_seat_id = None
            self.selected_screen_id = None
            self.selected_cinema_id = None
            self.selected_seat_type = None
    
    def is_valid_screen_id(self, screen_id):
        try:
            screen = self.screen_service.get_screen_by_id(screen_id) 
            return screen is not None
        except ValueError:
            return False

    def is_valid_cinema_id(self, cinema_id):
        try:
            cinema_id = int(cinema_id)
            cinema = self.cinema_service.get_cinema_by_id(cinema_id)
            return cinema is not None
        except ValueError:
            return False

    def is_valid_seat_type(self, seat_type):
        return seat_type in ["Lower", "Upper", "VIP"]

    def add_seat(self):
        if SeatManagement.add_window_open:
            messagebox.showerror("Error", "Add Seat window is already open.")
            return

        SeatManagement.add_window_open = True

        add_frame = ttk.Frame(self.seat_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Screen ID:").grid(row=0, column=0)
        self.screen_id_entry = ttk.Entry(add_frame)
        self.screen_id_entry.grid(row=0, column=1)

        tk.Label(add_frame, text="Cinema ID:").grid(row=1, column=0)
        self.cinema_id_entry = ttk.Entry(add_frame)
        self.cinema_id_entry.grid(row=1, column=1)

        tk.Label(add_frame, text="Seat Type:").grid(row=2, column=0)
        self.seat_type_entry = ttk.Entry(add_frame)
        self.seat_type_entry.grid(row=2, column=1)

        def add_seat_confirm():
            screen_id = self.screen_id_entry.get()
            cinema_id = self.cinema_id_entry.get()
            seat_type = self.seat_type_entry.get()

            if not self.is_valid_screen_id(screen_id):
                messagebox.showerror("Error", "Invalid Screen ID.")
                return
            if not self.is_valid_cinema_id(cinema_id):
                messagebox.showerror("Error", "Invalid Cinema ID.")
                return
            if not self.is_valid_seat_type(seat_type):
                messagebox.showerror("Error", "Invalid Seat Type. Must be Lower, Upper, or VIP.")
                return

            try:
                self.seat_service.create_seat(screen_id, cinema_id, seat_type)
                SeatManagement.add_window_open = False
                self.manage_seats()
                add_frame.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def cancel_add():
            SeatManagement.add_window_open = False
            add_frame.destroy()

        ttk.Button(add_frame, text="Confirm Add", command=add_seat_confirm).grid(row=3, column=0, pady=5, padx=(0, 5))
        ttk.Button(add_frame, text="Cancel", command=cancel_add).grid(row=3, column=1, pady=5, padx=(5, 0))

    def update_seat(self):
        if SeatManagement.update_window_open:
            messagebox.showerror("Error", "Update Seat window is already open.")
            return
        SeatManagement.update_window_open = True

        if self.selected_seat_id:

            update_frame = ttk.Frame(self.seat_frame)
            update_frame.pack(pady=10)

            tk.Label(update_frame, text="Screen ID:").grid(row=0, column=0)
            screen_id_entry = ttk.Entry(update_frame)
            screen_id_entry.grid(row=0, column=1)

            tk.Label(update_frame, text="Cinema ID:").grid(row=1, column=0)
            cinema_id_entry = ttk.Entry(update_frame)
            cinema_id_entry.grid(row=1, column=1)

            tk.Label(update_frame, text="Seat Type:").grid(row=2, column=0)
            seat_type_entry = ttk.Entry(update_frame)
            seat_type_entry.grid(row=2, column=1)

            def update_seat_confirm():
                screen_id_str = screen_id_entry.get()
                cinema_id_str = cinema_id_entry.get()
                seat_type_str = seat_type_entry.get()

                screen_id = None
                cinema_id = None
                seat_type = None

                if screen_id_str:
                    if not self.is_valid_screen_id(screen_id_str):
                        messagebox.showerror("Error", "Invalid Screen ID.")
                        return
                    screen_id = screen_id_str

                if cinema_id_str:
                    if not self.is_valid_cinema_id(cinema_id_str):
                        messagebox.showerror("Error", "Invalid Cinema ID.")
                        return
                    cinema_id = cinema_id_str

                if seat_type_str:
                    if not self.is_valid_seat_type(seat_type_str):
                        messagebox.showerror("Error", "Invalid Seat Type. Must be Lower, Upper, or VIP.")
                        return
                    seat_type = seat_type_str

                try:
                    self.seat_service.update_seat(self.selected_seat_id, screen_id, cinema_id, seat_type)
                    SeatManagement.update_window_open = False
                    self.manage_seats()
                    update_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            def cancel_update():
                SeatManagement.update_window_open = False
                update_frame.destroy()

            ttk.Button(update_frame, text="Confirm Update", command=update_seat_confirm).grid(row=3, column=0, pady=5, padx=(0, 5))
            ttk.Button(update_frame, text="Cancel", command=cancel_update).grid(row=3, column=1, pady=5, padx=(5, 0))

        else:
            messagebox.showerror("Error", "Select a seat to update.")
            SeatManagement.update_window_open = False


    def remove_seat(self):
        if self.selected_screen_id and self.selected_cinema_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this seat?"):
                try:
                    self.seat_service.delete_seat(self.selected_screen_id, self.selected_cinema_id)
                    self.manage_seats()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Select a seat to remove.")

    def browse_seat(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse Seat")

        tk.Label(browse_window, text="Seat ID:").grid(row=0, column=0)
        seat_id_entry = ttk.Entry(browse_window)
        seat_id_entry.grid(row=0, column=1)

        def find_seat():
            seat_id = seat_id_entry.get()
            found = False

            if seat_id:
                for item in self.seat_list.get_children():
                    values = self.seat_list.item(item, 'values')
                    if values and len(values) > 0 and str(values[0]) == seat_id:
                        self.seat_list.see(item)
                        self.seat_list.selection_set(item)
                        self.seat_list.focus(item)
                        self.selected_seat_id = seat_id
                        self.selected_screen_id = values[1]
                        self.selected_cinema_id = values[2]
                        self.selected_seat_type = values[3]
                        browse_window.destroy()
                        found = True
                        return

            if not found:
                if not seat_id:
                    messagebox.showerror("Error", "Please enter a Seat ID.")
                else:
                    messagebox.showerror("Error", "No matching seat found.")

        ttk.Button(browse_window, text="Find Seat", command=find_seat).grid(row=1, column=0, columnspan=2, pady=10)

    def clear_seat_frame(self):
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")