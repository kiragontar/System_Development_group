import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database.database_settings import SessionLocal
from main_components.services.cinema_service import CinemaService
from main_components.services.screen_service import ScreenService
from main_components.services.screening_service import ScreeningService

class ScreenManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, cinema_id, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.cinema_id = cinema_id
        self.session = SessionLocal()
        self.screen_service = ScreenService(self.session)
        self.cinema_service = CinemaService(self.session)
        self.screening_service = ScreeningService(self.session)
        self.selected_screen_id = None
        self.selected_cinema_id = None
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

        tk.Label(main_frame, text="Screen Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        self.screen_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.screen_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_screens()

    def manage_screens(self):
        self.clear_screen_frame()
        self.screen_list = ttk.Treeview(
            self.screen_frame,
            columns=("ID", "Cinema ID", "Total Capacity", "Row Number"),
            show="headings",
        )
        self.screen_list.heading("ID", text="ID")
        self.screen_list.heading("Cinema ID", text="Cinema ID")
        self.screen_list.heading("Total Capacity", text="Total Capacity")
        self.screen_list.heading("Row Number", text="Row Number")
        self.screen_list.pack(expand=True, fill="both")

        if self.cinema_id == "all":  # Get all screens if "all" is selected
            screens = self.screen_service.get_all_screens()
        else:  # Get screens for the specific cinema
            screens = self.screen_service.get_screens_for_cinema(self.cinema_id)

        for screen in screens:
            self.screen_list.insert(
                "",
                tk.END,
                values=(screen.screen_id, screen.cinema_id, screen.total_capacity, screen.row_number),
            )

        action_frame = ttk.Frame(self.screen_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add Screen", command=self.add_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update Screen", command=self.update_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Remove Screen", command=self.remove_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Get Screen for Screening", command=self.get_screen_for_screening).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse Screen", command=self.browse_screen).pack(side=tk.LEFT, padx=5)

        self.screen_list.bind("<ButtonRelease-1>", self.select_screen)
        self.selected_screen_id = None
        self.screen_frame.update()

    def select_screen(self, event):
        selection = self.screen_list.selection()
        if selection:
            item = selection[0]
            values = self.screen_list.item(item, "values")
            self.selected_screen_id = values[0]
            self.selected_cinema_id = values[1] 
        else:
            self.selected_screen_id = None
            self.selected_cinema_id = None

    def is_valid_screen_id(self, screen_id):
        if not isinstance(screen_id, str):
            return False

        if not screen_id.startswith("S"): # Ensure its in the format S + number of screen.
            return False

        number_part = screen_id[1:]  # Get the part after "S"

        try:
            int(number_part)  # Check if the remaining part is a number
            return True
        except ValueError:
            return False
        
    def is_valid_cinema_id(self, cinema_id):
        try:
            cinema_id = int(cinema_id)
            cinema = self.cinema_service.get_cinema_by_id(cinema_id)
            return cinema is not None
        except ValueError:
            return False
    
    def is_valid_total_capacity(self, total_capacity):
        try:
            total_capacity = int(total_capacity)
            return 50 <= total_capacity <= 120
        except ValueError:
            return False
        
    def is_valid_row_number(self, row_number):
        try:
            row_number = int(row_number)
            return 1 <= row_number <= 20
        except ValueError:
            return False

    def add_screen(self):
        if ScreenManagement.add_window_open:
            messagebox.showerror("Error", "Add Screen window is already open.")
            return

        ScreenManagement.add_window_open = True

        add_frame = ttk.Frame(self.screen_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Screen ID:").grid(row=0, column=0)
        self.screen_id_entry = ttk.Entry(add_frame)
        self.screen_id_entry.grid(row=0, column=1)

        tk.Label(add_frame, text="Cinema ID:").grid(row=1, column=0)
        self.cinema_id_entry = ttk.Entry(add_frame)
        self.cinema_id_entry.grid(row=1, column=1)

        tk.Label(add_frame, text="Total Capacity:").grid(row=2, column=0)
        self.total_capacity_entry = ttk.Entry(add_frame)
        self.total_capacity_entry.grid(row=2, column=1)

        tk.Label(add_frame, text="Row Number:").grid(row=3, column=0)
        self.row_number_entry = ttk.Entry(add_frame)
        self.row_number_entry.grid(row=3, column=1)

        def add_screen_confirm():
            screen_id = self.screen_id_entry.get()
            cinema_id = self.cinema_id_entry.get()
            total_capacity = self.total_capacity_entry.get()
            row_number = self.row_number_entry.get()

            if not self.is_valid_screen_id(screen_id):
                messagebox.showerror("Error", "Invalid Screen ID. Please enter a valid Screen ID, in the format : 'S'+ number")
                return
            if not self.is_valid_cinema_id(cinema_id):
                messagebox.showerror("Error", "Invalid Cinema ID. Please enter a valid Cinema ID.")
                return
            if not self.is_valid_total_capacity(total_capacity):
                messagebox.showerror("Error", "Invalid Total Capacity. Please enter an integer between 50 and 120.")
                return
            if not self.is_valid_row_number(row_number):
                messagebox.showerror("Error", "Invalid Row Number. Please enter an integer between 1 and 20.")
                return

            try:
                self.screen_service.create_screen(screen_id, cinema_id, total_capacity, row_number)
                ScreenManagement.add_window_open = False
                self.manage_screens()
                add_frame.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def cancel_add():
            ScreenManagement.add_window_open = False
            add_frame.destroy()

        ttk.Button(add_frame, text="Confirm Add", command=add_screen_confirm).grid(row=4, column=0, pady=5, padx=(0, 5))
        ttk.Button(add_frame, text="Cancel", command=cancel_add).grid(row=4, column=1, pady=5, padx=(5, 0))

    def update_screen(self):
        if ScreenManagement.update_window_open:
            messagebox.showerror("Error", "Update Screen window is already open.")
            return
        ScreenManagement.update_window_open = True

        if self.selected_screen_id and self.selected_cinema_id:
            update_frame = ttk.Frame(self.screen_frame)
            update_frame.pack(pady=10)

            screen = self.screen_service.get_screen_by_id(self.selected_screen_id, self.selected_cinema_id)
            if screen:
                tk.Label(update_frame, text="Total Capacity:").grid(row=0, column=0)
                self.total_capacity_entry = ttk.Entry(update_frame)
                self.total_capacity_entry.insert(0, screen.total_capacity)
                self.total_capacity_entry.grid(row=0, column=1)

                tk.Label(update_frame, text="Row Number:").grid(row=1, column=0)
                self.row_number_entry = ttk.Entry(update_frame)
                self.row_number_entry.insert(0, screen.row_number)
                self.row_number_entry.grid(row=1, column=1)

                def update_screen_confirm():
                    total_capacity_str = self.total_capacity_entry.get()
                    row_number_str = self.row_number_entry.get()

                    total_capacity = None
                    row_number = None

                    if total_capacity_str:
                        if not self.is_valid_total_capacity(total_capacity_str):
                            messagebox.showerror("Error", "Invalid Total Capacity. Please enter an integer between 50 and 120.")
                            return
                        total_capacity = int(total_capacity_str)

                    if row_number_str:
                        if not self.is_valid_row_number(row_number_str):
                            messagebox.showerror("Error", "Invalid Row Number. Please enter an integer between 1 and 20.")
                            return
                        row_number = int(row_number_str)
                    

                    self.screen_service.update_screen_capacities(self.selected_screen_id, self.selected_cinema_id, total_capacity, row_number)
                    ScreenManagement.update_window_open = False
                    self.manage_screens()
                    update_frame.destroy()

                def cancel_update():
                    ScreenManagement.update_window_open = False
                    update_frame.destroy()

                ttk.Button(update_frame, text="Confirm Update", command=update_screen_confirm).grid(row=2, column=0, pady=5, padx=(0, 5))
                ttk.Button(update_frame, text="Cancel", command=cancel_update).grid(row=2, column=1, pady=5, padx=(5, 0))
            
            else:
                messagebox.showerror("Error", "Screen not found.")
                ScreenManagement.update_window_open = False

        else:
            messagebox.showerror("Error", "Select a screen to update.")
            ScreenManagement.update_window_open = False

    def remove_screen(self):
        if self.selected_screen_id and self.selected_cinema_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this screen?"):
                screen = self.screen_service.get_screen_by_id(self.selected_screen_id, self.selected_cinema_id)
                if screen:
                    self.screen_service.delete_screen(self.selected_screen_id, self.selected_cinema_id)
                    self.manage_screens()
                else:
                    messagebox.showerror("Error", "Screen not found.")
        else:
            messagebox.showerror("Error", "Select a screen to remove.")

    def get_screen_for_screening(self):
        screening_id = tk.simpledialog.askstring("Input", "Enter Screening ID:")

        if screening_id:
            screening = self.screening_service.get_screening_by_id(screening_id)
            if screening:
                screen = self.screen_service.get_screen_by_id(screening.screen_id, screening.cinema_id)
                if screen:
                    screen_info = f"Screen ID: {screen.screen_id}\nCinema ID: {screen.cinema_id}\nCapacity: {screen.total_capacity}\nRow Number: {screen.row_number}"
                    messagebox.showinfo("Screen Information", screen_info)
                else:
                    messagebox.showerror("Error", "Screen not found for this screening.")
            else:
                messagebox.showerror("Error", "Screening not found.")
        else:
            messagebox.showerror("Error", "Please enter a Screening ID.")

    def browse_screen(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse Screen")

        tk.Label(browse_window, text="Screen ID:").grid(row=0, column=0)
        screen_id_entry = ttk.Entry(browse_window)
        screen_id_entry.grid(row=0, column=1)

        tk.Label(browse_window, text="Cinema ID:").grid(row=1, column=0)
        cinema_id_entry = ttk.Entry(browse_window)
        cinema_id_entry.grid(row=1, column=1)

        def find_screen():
            screen_id = screen_id_entry.get()
            cinema_id = cinema_id_entry.get()
            found = False
        
            if screen_id and cinema_id:
                for item in self.screen_list.get_children():
                    values = self.screen_list.item(item, 'values')
                    if values and len(values) > 1 and str(values[0]) == screen_id and str(values[1]) == cinema_id:
                        self.screen_list.see(item)
                        self.screen_list.selection_set(item)
                        self.screen_list.focus(item)
                        self.selected_screen_id = screen_id
                        self.selected_cinema_id = cinema_id
                        browse_window.destroy()
                        found = True
                        return
            
            elif screen_id or cinema_id:
                messagebox.showerror("Error", "Please enter both Screen ID and Cinema ID.")
            
            if not found and not screen_id and not cinema_id: # Error for no input.
                messagebox.showerror("Error", "Please enter Screen ID and Cinema ID.")
            elif not found and screen_id and cinema_id:
                messagebox.showerror("Error", "No matching screen found.")

        ttk.Button(browse_window, text="Find Screen", command=find_screen).grid(row=2, column=0, columnspan=2, pady=10)
        
    def clear_screen_frame(self):
        for widget in self.screen_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")
