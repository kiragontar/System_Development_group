import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.database_settings import SessionLocal
from main_components.services.screening_service import ScreeningService
from main_components.services.screen_service import ScreenService
from main_components.services.film_service import FilmService
from main_components.services.cinema_service import CinemaService
from main_components.services.role_service import RoleService

class ScreeningManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, cinema_id, user=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.cinema_id = cinema_id
        self.user = user
        self.session = SessionLocal()
        self.screening_service = ScreeningService(self.session)
        self.screen_service = ScreenService(self.session)
        self.film_service = FilmService(self.session)
        self.cinema_service = CinemaService(self.session)
        self.role_service = RoleService(self.session)
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

        tk.Label(main_frame, text="Screening Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        self.screening_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.screening_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_screenings()


    def manage_screenings(self):
        self.clear_screening_frame()
        self.screening_list = ttk.Treeview(
            self.screening_frame,
            columns=("Screening ID", "Film ID", "Screen ID", "Cinema ID", "Date", "Start Time", "Availability"),
            show="headings",
        )
        self.screening_list.heading("Screening ID", text="Screening ID")
        self.screening_list.heading("Film ID", text="Film ID")
        self.screening_list.heading("Screen ID", text="Screen ID")
        self.screening_list.heading("Cinema ID", text="Cinema ID")
        self.screening_list.heading("Date", text="Date")
        self.screening_list.heading("Start Time", text="Start Time")
        self.screening_list.heading("Availability", text="Availability")
        self.screening_list.pack(expand=True, fill="both")

        if self.cinema_id == "all":
            screenings = self.screening_service.get_all_screenings() #get all screenings.
        else:
            screenings = self.screening_service.get_all_screenings_for_cinema(self.cinema_id) #get screenings by cinema id.

        for screening in screenings:
            self.screening_list.insert(
                "",
                tk.END,
                values=(screening.screening_id, screening.film_id, screening.screen_id, screening.cinema_id,screening.date, screening.start_time, screening.screening_availability),
            )

        action_frame = ttk.Frame(self.screening_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        if self.user and hasattr(self.user, 'role_id'):
            role = self.role_service.get_role_by_id(self.user.role_id)
            if role and role.name in ["Admin", "Manager"]:
                ttk.Button(action_frame, text="Add Screening", command=self.add_screening).pack(side=tk.LEFT, padx=5)
                ttk.Button(action_frame, text="Update Screening", command=self.update_screening).pack(side=tk.LEFT, padx=5)
                ttk.Button(action_frame, text="Remove Screening", command=self.remove_screening).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse Screening", command=self.browse_screening).pack(side=tk.LEFT, padx=5)

        self.screening_list.bind("<ButtonRelease-1>", self.select_screening)
        self.selected_screening_id = None
        self.screening_frame.update()

    def select_screening(self, event):
        selection = self.screening_list.selection()
        if selection:
            item = selection[0]
            values = self.screening_list.item(item, "values")
            self.selected_screening_id = values[0]
        else:
            self.selected_screening_id = None

    
    def is_valid_film_id(self, film_id):
        try:
            film_id = int(film_id)
            film = self.film_service.get_film_by_id(film_id)
            return film is not None
        except ValueError:
            return False

    def is_valid_cinema_id(self, cinema_id):
        try:
            cinema_id = int(cinema_id)
            cinema = self.cinema_service.get_cinema_by_id(cinema_id)
            return cinema is not None
        except ValueError:
            return False

    def is_valid_screen_id(self, screen_id):
        try:
            if not isinstance(screen_id, str):
                return False
            screen = self.screen_service.get_screen_by_id(screen_id)
            return screen is not None
        except Exception:
            return False

    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d").date()
            return True
        except ValueError:
            return False

    def is_valid_time(self, time_str):
        try:
            datetime.strptime(time_str, "%H:%M").time()
            return True
        except ValueError:
            return False

    def is_valid_availability(self, availability):
        try:
            availability = int(availability)
            return availability in [0,1]
        except ValueError:
            return False


    def add_screening(self):
        if ScreeningManagement.add_window_open:
            messagebox.showerror("Error", "Add Screening window is already open.")
            return

        ScreeningManagement.add_window_open = True

        add_frame = ttk.Frame(self.screening_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Film ID:").grid(row=0, column=0)
        film_id_entry = ttk.Entry(add_frame)
        film_id_entry.grid(row=0, column=1)

        tk.Label(add_frame, text="Screen ID:").grid(row=1, column=0)
        screen_id_entry = ttk.Entry(add_frame)
        screen_id_entry.grid(row=1, column=1)

        tk.Label(add_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
        date_entry = ttk.Entry(add_frame)
        date_entry.grid(row=2, column=1)

        tk.Label(add_frame, text="Start Time (HH:MM):").grid(row=3, column=0)
        start_time_entry = ttk.Entry(add_frame)
        start_time_entry.grid(row=3, column=1)

        tk.Label(add_frame, text="Availability:").grid(row=4, column=0)
        availability_entry = ttk.Entry(add_frame)
        availability_entry.grid(row=4, column=1)

        if self.cinema_id == "all":
            tk.Label(add_frame, text="Cinema ID:").grid(row=5, column=0)
            cinema_id_entry = ttk.Entry(add_frame)
            cinema_id_entry.grid(row=5, column=1)
            button_row = 6
        else:
            cinema_id_entry = None
            button_row = 5

        def add_screening_confirm():
            try:
                film_id = int(film_id_entry.get())
                screen_id = screen_id_entry.get()
                date_str = date_entry.get()
                start_time_str = start_time_entry.get()
                availability = int(availability_entry.get())

                if not self.is_valid_film_id(film_id):
                    messagebox.showerror("Error", "Invalid Film ID.")
                    return
                if not self.is_valid_screen_id(screen_id):
                    messagebox.showerror("Error", "Invalid Screen ID.")
                    return
                if not self.is_valid_date(date_str):
                    messagebox.showerror("Error", "Invalid Date. Format Should be YYYY-MM-DD")
                    return
                if not self.is_valid_time(start_time_str):
                    messagebox.showerror("Error", "Invalid Start Time. Format Should be HH:MM")
                    return
                if not self.is_valid_availability(availability):
                    messagebox.showerror("Error", "Invalid Availability (0 or 1). Either 0 or 1")
                    return

                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()
                availability_int = int(availability)

                if self.cinema_id == "all":
                    cinema_id = int(cinema_id_entry.get())
                else:
                    cinema_id = self.cinema_id

                if not self.is_valid_cinema_id(cinema_id):
                    messagebox.showerror("Error", "Invalid Cinema ID.")
                    return
                try: 
                    self.screening_service.create_screening(film_id, screen_id, cinema_id, date_obj, start_time_obj, availability_int)
                    ScreeningManagement.add_window_open = False
                    self.manage_screenings()
                    add_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            except ValueError as e:
                messagebox.showerror("Error", str(e))
            
        def cancel_add():
            ScreeningManagement.add_window_open = False
            add_frame.destroy()

        ttk.Button(add_frame, text="Confirm Add", command=add_screening_confirm).grid(row=button_row, column=0, pady=5, padx=(0, 5))
        ttk.Button(add_frame, text="Cancel", command=cancel_add).grid(row=button_row, column=1, pady=5, padx=(5, 0))


    def update_screening(self):
        if ScreeningManagement.update_window_open:
            messagebox.showerror("Error", "Update Screening window is already open.")
            return
        ScreeningManagement.update_window_open = True

        if self.selected_screening_id:
            update_frame = ttk.Frame(self.screening_frame)
            update_frame.pack(pady=10)

            # Input fields
            tk.Label(update_frame, text="Film ID:").grid(row=0, column=0)
            film_id_entry = ttk.Entry(update_frame)
            film_id_entry.grid(row=0, column=1)

            tk.Label(update_frame, text="Screen ID:").grid(row=1, column=0)
            screen_id_entry = ttk.Entry(update_frame)
            screen_id_entry.grid(row=1, column=1)

            tk.Label(update_frame, text="Cinema ID:").grid(row=2, column=0)
            cinema_id_entry = ttk.Entry(update_frame)
            cinema_id_entry.grid(row=2, column=1)

            tk.Label(update_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0)
            date_entry = ttk.Entry(update_frame)
            date_entry.grid(row=3, column=1)

            tk.Label(update_frame, text="Start Time (HH:MM):").grid(row=4, column=0)
            start_time_entry = ttk.Entry(update_frame)
            start_time_entry.grid(row=4, column=1)

            tk.Label(update_frame, text="Availability:").grid(row=5, column=0)
            availability_entry = ttk.Entry(update_frame)
            availability_entry.grid(row=5, column=1)

            def update_screening_confirm():
                
                film_id_str = film_id_entry.get()
                screen_id_str = screen_id_entry.get()
                cinema_id_str = cinema_id_entry.get()
                date_str = date_entry.get()
                start_time_str = start_time_entry.get()
                availability_str = availability_entry.get()

                film_id = None
                screen_id = None
                cinema_id = None
                date_obj = None
                start_time_obj = None
                availability_int = None

                # Validation and conversion
                if film_id_str:
                    if not self.is_valid_film_id(film_id_str):
                        messagebox.showerror("Error", "Invalid Film ID.")
                        return
                    film_id = int(film_id_str)

                if screen_id_str:
                    if not self.is_valid_screen_id(screen_id_str):
                        messagebox.showerror("Error", "Invalid Screen ID.")
                        return
                    screen_id = screen_id_str

                if cinema_id_str:
                    if not self.is_valid_cinema_id(cinema_id_str):
                        messagebox.showerror("Error", "Invalid Cinema ID.")
                        return
                    cinema_id = int(cinema_id_str)

                if date_str:
                    if not self.is_valid_date(date_str):
                        messagebox.showerror("Error", "Invalid Date. Format Should be YYYY-MM-DD")
                        return
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

                if start_time_str:
                    if not self.is_valid_time(start_time_str):
                        messagebox.showerror("Error", "Invalid Start Time. Format should be HH:MM")
                        return
                    start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()

                if availability_str:
                    if not self.is_valid_availability(availability_str):
                        messagebox.showerror("Error", "Invalid Availability. Either 0 or 1")
                        return
                    availability_int = int(availability_str)

                try:
                    self.screening_service.update_screening(
                        self.selected_screening_id, film_id, screen_id, cinema_id, date_obj, start_time_obj, availability_int
                    )
                    ScreeningManagement.update_window_open = False
                    self.manage_screenings()
                    update_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            def cancel_update():
                ScreeningManagement.update_window_open = False
                update_frame.destroy()

            ttk.Button(update_frame, text="Confirm Update", command=update_screening_confirm).grid(row=6, column=0, pady=5, padx=(0, 5)) #row 6.
            ttk.Button(update_frame, text="Cancel", command=cancel_update).grid(row=6, column=1, pady=5, padx=(5, 0)) #row 6.
        else:
            messagebox.showerror("Error", "Select a screening to update.")
            ScreeningManagement.update_window_open = False

    
    def remove_screening(self):
        if self.selected_screening_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this screening?"):
                try:
                    self.screening_service.delete_screening(self.selected_screening_id)
                    self.manage_screenings()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Select a screening to remove.")

    
    def browse_screening(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse Screening")

        tk.Label(browse_window, text="Screening ID (Optional):").grid(row=0, column=0)
        screening_id_entry = ttk.Entry(browse_window)
        screening_id_entry.grid(row=0, column=1)

        screen_id_label = tk.Label(browse_window, text="Screen ID:")
        screen_id_entry = ttk.Entry(browse_window)
        cinema_id_label = tk.Label(browse_window, text="Cinema ID:")
        cinema_id_entry = ttk.Entry(browse_window)
        
        def find_screening():
            screening_id = screening_id_entry.get()
            screen_id = screen_id_entry.get()
            cinema_id = cinema_id_entry.get()
            found = False

            if screening_id:
                for item in self.screening_list.get_children():
                    values = self.screening_list.item(item, 'values')
                    if values and len(values) > 0 and str(values[0]) == screening_id:
                        self.screening_list.see(item)
                        self.screening_list.selection_set(item)
                        self.screening_list.focus(item)
                        self.selected_screening_id = screening_id
                        browse_window.destroy()
                        found = True
                        return

            elif screen_id and cinema_id:
                for item in self.screening_list.get_children():
                    values = self.screening_list.item(item, 'values')
                    if values and len(values) >= 3:
                        columns = self.screening_list['columns']

                        screen_id_column_index = columns.index('Screen ID') if 'Screen ID' in columns else -1
                        cinema_id_column_index = columns.index('Cinema ID') if 'Cinema ID' in columns else -1

                        if screen_id_column_index != -1 and cinema_id_column_index != -1:
                            try:
                                if str(values[screen_id_column_index]) == screen_id and str(values[cinema_id_column_index]) == cinema_id:
                                    self.screening_list.see(item)
                                    self.screening_list.selection_set(item)
                                    self.screening_list.focus(item)
                                    self.selected_screening_id = values[0]
                                    browse_window.destroy()
                                    found = True
                                    return
                            except IndexError:
                                continue

            if not found:
                if not screening_id and not screen_id and not cinema_id:
                    messagebox.showerror("Error", "Please enter a Screening ID or Screen ID and Cinema ID.")
                else:
                    messagebox.showerror("Error", "No matching screening found.")

        def toggle_screen_cinema_inputs():
            if screening_id_entry.get():
                screen_id_label.grid_forget()
                screen_id_entry.grid_forget()
                cinema_id_label.grid_forget()
                cinema_id_entry.grid_forget()
            else:
                screen_id_label.grid(row=1, column=0)
                screen_id_entry.grid(row=1, column=1)
                cinema_id_label.grid(row=2, column=0)
                cinema_id_entry.grid(row=2, column=1)

        screening_id_entry.bind("<KeyRelease>", lambda event: toggle_screen_cinema_inputs())
        toggle_screen_cinema_inputs()

        ttk.Button(browse_window, text="Find Screening", command=find_screening).grid(row=3, column=0, columnspan=2, pady=10)

    def clear_screening_frame(self):
        for widget in self.screening_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")