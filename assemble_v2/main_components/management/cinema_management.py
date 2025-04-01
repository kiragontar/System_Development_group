import tkinter as tk
from tkinter import ttk, messagebox
from database.database_settings import SessionLocal
from main_components.services.cinema_service import CinemaService
from main_components.services.city_service import CityService

class CinemaManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.session = SessionLocal()
        self.cinema_service = CinemaService(self.session)
        self.city_service = CityService(self.session)
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

        tk.Label(main_frame, text="Cinema Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        self.cinema_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.cinema_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_cinemas()

    def manage_cinemas(self):
        self.clear_cinema_frame()
        self.cinema_list = ttk.Treeview(
            self.cinema_frame,
            columns=("ID", "City ID", "Name", "Address"),
            show="headings",
        )
        self.cinema_list.heading("ID", text="ID")
        self.cinema_list.heading("City ID", text="City ID")
        self.cinema_list.heading("Name", text="Name")
        self.cinema_list.heading("Address", text="Address")
        self.cinema_list.pack(expand=True, fill="both")

        cinemas = self.cinema_service.get_all_cinemas()
        for cinema in cinemas:
            self.cinema_list.insert(
                "",
                tk.END,
                values=(cinema.cinema_id, cinema.city_id, cinema.name, cinema.address),
            )

        action_frame = ttk.Frame(self.cinema_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add Cinema", command=self.add_cinema).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update Cinema", command=self.update_cinema).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Remove Cinema", command=self.remove_cinema).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse Cinema", command=self.browse_cinema).pack(side=tk.LEFT, padx=5)

        self.cinema_list.bind("<ButtonRelease-1>", self.select_cinema)
        self.selected_cinema_id = None
        self.cinema_frame.update()

    def select_cinema(self, event):
        selection = self.cinema_list.selection()
        if selection:
            item = selection[0]
            self.selected_cinema_id = self.cinema_list.item(item, "values")[0]
        else:
            self.selected_cinema_id = None

    def is_valid_city_id(self, city_id):
        try:
            city_id = int(city_id)
            city = self.city_service.get_city_by_id(city_id)
            return city is not None
        except ValueError:
            return False
        
    def is_valid_name(self, name):
        return isinstance(name, str) and name.strip() != ""

    def is_valid_address(self, address):
        return isinstance(address, str) and address.strip() != ""

    def add_cinema(self):
        if CinemaManagement.add_window_open:
            messagebox.showerror("Error", "Add Cinema window is already open.")
            return

        CinemaManagement.add_window_open = True

        add_frame = ttk.Frame(self.cinema_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="City ID:").grid(row=0, column=0)
        self.city_id_entry = ttk.Entry(add_frame)
        self.city_id_entry.grid(row=0, column=1)

        tk.Label(add_frame, text="Name:").grid(row=1, column=0)
        self.name_entry = ttk.Entry(add_frame)
        self.name_entry.grid(row=1, column=1)

        tk.Label(add_frame, text="Address:").grid(row=2, column=0)
        self.address_entry = ttk.Entry(add_frame)
        self.address_entry.grid(row=2, column=1)

        def add_cinema_confirm():
            city_id = self.city_id_entry.get()
            name = self.name_entry.get()
            address = self.address_entry.get()

            if not self.is_valid_city_id(city_id):
                messagebox.showerror("Error", "Invalid City ID. Please enter a valid integer.")
                return
            if not self.is_valid_name(name):
                messagebox.showerror("Error", "Invalid Name. Please enter a valid name.")
                return
            if not self.is_valid_address(address):
                messagebox.showerror("Error", "Invalid Address. Please enter a valid address.")
                return

            try:
                self.cinema_service.create_cinema(city_id, name, address)
                CinemaManagement.add_window_open = False
                self.manage_cinemas()
                add_frame.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def cancel_add():
            CinemaManagement.add_window_open = False
            add_frame.destroy()

        ttk.Button(add_frame, text="Confirm Add", command=add_cinema_confirm).grid(row=3, column=0, pady=5, padx=(0, 5))
        ttk.Button(add_frame, text="Cancel", command=cancel_add).grid(row=3, column=1, pady=5, padx=(5, 0))

    def update_cinema(self):
        if CinemaManagement.update_window_open:
            messagebox.showerror("Error", "Update Cinema window is already open.")
            return
        CinemaManagement.update_window_open = True

        if self.selected_cinema_id:
            update_frame = ttk.Frame(self.cinema_frame)
            update_frame.pack(pady=10)

            cinema = self.cinema_service.get_cinema_by_id(self.selected_cinema_id)

            tk.Label(update_frame, text="City ID:").grid(row=0, column=0)
            self.city_id_entry = ttk.Entry(update_frame)
            self.city_id_entry.insert(0, cinema.city_id)
            self.city_id_entry.grid(row=0, column=1)

            tk.Label(update_frame, text="Name:").grid(row=1, column=0)
            self.name_entry = ttk.Entry(update_frame)
            self.name_entry.insert(0, cinema.name)
            self.name_entry.grid(row=1, column=1)

            tk.Label(update_frame, text="Address:").grid(row=2, column=0)
            self.address_entry = ttk.Entry(update_frame)
            self.address_entry.insert(0, cinema.address)
            self.address_entry.grid(row=2, column=1)

            def update_cinema_confirm():
                city_id_str = self.city_id_entry.get()
                name = self.name_entry.get()
                address = self.address_entry.get()

                city_id = None

                try:
                    if city_id_str:
                        city_id = int(city_id_str)
                        if not self.is_valid_city_id(city_id):
                            messagebox.showerror("Error", "Invalid City ID. Please enter a valid integer.")
                            return
                except ValueError:
                    if city_id_str:
                        messagebox.showerror("Error", "Invalid City ID. Please enter a valid integer.")
                        return

                if name and not self.is_valid_name(name):
                    messagebox.showerror("Error", "Invalid Name. Please enter a valid name.")
                    return

                if address and not self.is_valid_address(address):
                    messagebox.showerror("Error", "Invalid Address. Please enter a valid address.")
                    return

                try:
                    self.cinema_service.update_cinema(self.selected_cinema_id, city_id, name, address)
                    CinemaManagement.update_window_open = False
                    self.manage_cinemas()
                    update_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                    

            def cancel_update():
                CinemaManagement.update_window_open = False #set to false
                update_frame.destroy()

            ttk.Button(update_frame, text="Confirm Update", command=update_cinema_confirm).grid(row=4, column=0, pady=5, padx=(0,5))
            ttk.Button(update_frame, text="Cancel", command=cancel_update).grid(row=4, column=1, pady=5, padx=(5,0)) #added cancel button
        else:
            messagebox.showerror("Error", "Select a cinema to update.")
            CinemaManagement.update_window_open = False

    def remove_cinema(self):
        if self.selected_cinema_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this cinema?"):
                self.cinema_service.delete_cinema(self.selected_cinema_id)
                self.manage_cinemas()
        else:
            messagebox.showerror("Error", "Select a cinema to remove.")

    def browse_cinema(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse Cinema")

        tk.Label(browse_window, text="Cinema ID (Optional):").grid(row=0, column=0)
        cinema_id_entry = ttk.Entry(browse_window)
        cinema_id_entry.grid(row=0, column=1)

        city_id_label = tk.Label(browse_window, text="City ID:")
        city_id_entry = ttk.Entry(browse_window)
        cinema_name_label = tk.Label(browse_window, text="Cinema Name:")
        cinema_name_entry = ttk.Entry(browse_window)
        cinema_address_label = tk.Label(browse_window, text="Cinema Address:")
        cinema_address_entry = ttk.Entry(browse_window)

        def find_cinema():
            cinema_id = cinema_id_entry.get()
            city_id = city_id_entry.get()
            cinema_name = cinema_name_entry.get()
            cinema_address = cinema_address_entry.get()
            found = False

            if cinema_id:
                for item in self.cinema_list.get_children():
                    values = self.cinema_list.item(item, 'values')
                    if values and len(values) > 0 and str(values[0]) == cinema_id:
                        self.cinema_list.see(item)
                        self.cinema_list.selection_set(item)
                        self.cinema_list.focus(item)
                        self.selected_cinema_id = cinema_id
                        browse_window.destroy()
                        Found = True
                        return
            elif city_id and cinema_name and cinema_address:
                for item in self.cinema_list.get_children():
                    # Retrieve the values by the column identifiers
                    values = self.cinema_list.item(item, 'values')
                    if values and len(values) >= 4:
                        #Retrieve the column ids
                        columns = self.cinema_list['columns']

                        # find the position of each column.
                        city_id_column_index = columns.index('City ID') if 'City ID' in columns else -1
                        cinema_name_column_index = columns.index('Name') if 'Name' in columns else -1
                        cinema_address_column_index = columns.index('Address') if 'Address' in columns else -1

                        #Ensure that the requested columns exist.
                        if city_id_column_index != -1 and cinema_name_column_index != -1 and cinema_address_column_index != -1:
                            try:
                                if str(values[city_id_column_index]) == city_id and values[cinema_name_column_index] == cinema_name and values[cinema_address_column_index] == cinema_address:
                                    self.cinema_list.see(item)
                                    self.cinema_list.selection_set(item)
                                    self.cinema_list.focus(item)
                                    self.selected_cinema_id = values[0]
                                    browse_window.destroy()
                                    Found = True
                                    return
                            except IndexError:
                                continue
            if not found:
                messagebox.showerror("Error", "No matching cinema found.")
            elif not cinema_id and city_id and not cinema_name and not cinema_address:
                messagebox.showerror("Error", "Please enter a Cinema ID or City ID, Cinema Name, and Cinema Address.")

        def toggle_city_name_address_inputs():
            if cinema_id_entry.get():
                city_id_label.grid_forget()
                city_id_entry.grid_forget()
                cinema_name_label.grid_forget()
                cinema_name_entry.grid_forget()
                cinema_address_label.grid_forget()
                cinema_address_entry.grid_forget()
            else:
                city_id_label.grid(row=1, column=0)
                city_id_entry.grid(row=1, column=1)
                cinema_name_label.grid(row=2, column=0)
                cinema_name_entry.grid(row=2, column=1)
                cinema_address_label.grid(row=3, column=0)
                cinema_address_entry.grid(row=3, column=1)

        cinema_id_entry.bind("<KeyRelease>", lambda event: toggle_city_name_address_inputs())
        toggle_city_name_address_inputs()

        ttk.Button(browse_window, text="Find Cinema", command=find_cinema).grid(row=4, column=0, columnspan=2, pady=10)

    def clear_cinema_frame(self):
        for widget in self.cinema_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")