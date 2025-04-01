import tkinter as tk
from tkinter import ttk, messagebox
from database.database_settings import SessionLocal
from main_components.services.city_service import CityService

class CityManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.session = SessionLocal()
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

        tk.Label(main_frame, text="City Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10) #only have the back button.

        self.city_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.city_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_cities() #display the cities on load.

    def manage_cities(self): # Displays all avaialble cities
        self.clear_city_frame()
        self.city_list = ttk.Treeview(self.city_frame, columns=("ID", "Name", "Country", "Morning Price", "Afternoon Price", "Evening Price"), show="headings")
        self.city_list.heading("ID", text="ID")
        self.city_list.heading("Name", text="Name")
        self.city_list.heading("Country", text="Country")
        self.city_list.heading("Morning Price", text="Morning Price")
        self.city_list.heading("Afternoon Price", text="Afternoon Price")
        self.city_list.heading("Evening Price", text="Evening Price")
        self.city_list.pack(expand=True, fill="both")

        cities = self.city_service.get_all_cities()
        for city in cities:
            self.city_list.insert("", tk.END, values=(city.city_id, city.name, city.country, city.price_morning, city.price_afternoon, city.price_evening))

        action_frame = ttk.Frame(self.city_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add City", command=self.add_city).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update City", command=self.update_city).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Remove City", command=self.remove_city).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse City", command=self.browse_city).pack(side=tk.LEFT, padx=5)

        self.city_list.bind("<ButtonRelease-1>", self.select_city)
        self.selected_city_id = None
        self.city_frame.update()
    
    def select_city(self, event): # Takes selected city from user
        selection = self.city_list.selection()
        if selection:
            item = selection[0]
            self.selected_city_id = self.city_list.item(item, "values")[0]
        else:
            self.selected_city_id = None # No item is selected.

    def is_valid_name(self, name):
        return isinstance(name, str) and name.strip() != "" and all(c.isalpha() or c.isspace() for c in name)

    def is_valid_country(self, country):
        return isinstance(country, str) and country.strip() != "" and all(c.isalpha() or c.isspace() for c in country)

    def is_valid_price(self, price):
        if not price:
            return False
        try:
            float(price)
            return True
        except ValueError:
            return False

    def add_city(self): # Takes input from user
        if CityManagement.add_window_open:
            messagebox.showerror("Error", "Add City window is already open.")
            return

        CityManagement.add_window_open = True

        add_frame = ttk.Frame(self.city_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(add_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(add_frame, text="Country:").grid(row=1, column=0)
        self.country_entry = ttk.Entry(add_frame)
        self.country_entry.grid(row=1, column=1)

        tk.Label(add_frame, text="Morning Price:").grid(row=2, column=0)
        self.morning_price_entry = ttk.Entry(add_frame)
        self.morning_price_entry.grid(row=2, column=1)

        tk.Label(add_frame, text="Afternoon Price:").grid(row=3, column=0)
        self.afternoon_price_entry = ttk.Entry(add_frame)
        self.afternoon_price_entry.grid(row=3, column=1)

        tk.Label(add_frame, text="Evening Price:").grid(row=4, column=0)
        self.evening_price_entry = ttk.Entry(add_frame)
        self.evening_price_entry.grid(row=4, column=1)

        def add_city_confirm(): # Creates city using service, only happens if they click confirm, then shows them the cities again.
            name = self.name_entry.get()
            country = self.country_entry.get()
            morning_price = self.morning_price_entry.get()
            afternoon_price = self.afternoon_price_entry.get()
            evening_price = self.evening_price_entry.get()

            if not self.is_valid_name(name):
                messagebox.showerror("Error", "Invalid name. Please enter a valid name.")
                return
            if not self.is_valid_country(country):
                messagebox.showerror("Error", "Invalid country. Please enter a valid country.")
                return
            if not self.is_valid_price(morning_price):
                messagebox.showerror("Error", "Invalid morning price. Please enter a number.")
                return
            if not self.is_valid_price(afternoon_price):
                messagebox.showerror("Error", "Invalid afternoon price. Please enter a number.")
                return
            if not self.is_valid_price(evening_price):
                messagebox.showerror("Error", "Invalid evening price. Please enter a number.")
                return
            
            try:
                self.city_service.create_city(name, country, morning_price, afternoon_price, evening_price)
                CityManagement.add_window_open = False
                self.manage_cities()
                add_frame.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def cancel_add():
            CityManagement.add_window_open = False
            add_frame.destroy()

        ttk.Button(add_frame, text="Confirm Add", command=add_city_confirm).grid(row=5, column=0, pady=5, padx=(0,5))
        ttk.Button(add_frame, text="Cancel", command=cancel_add).grid(row=5, column=1, pady=5, padx=(5,0)) 


    def update_city(self): # Gets info for update.
        if CityManagement.update_window_open:
            messagebox.showerror("Error", "Update City window is already open.")
            return
        
        CityManagement.update_window_open = True

        if self.selected_city_id:
            update_frame = ttk.Frame(self.city_frame)
            update_frame.pack(pady=10)

            city = self.city_service.get_city_by_id(self.selected_city_id) # gets the city thats selected from database.

            tk.Label(update_frame, text="Name:").grid(row=0, column=0)
            self.name_entry = ttk.Entry(update_frame)
            self.name_entry.insert(0, city.name)
            self.name_entry.grid(row=0, column=1)

            tk.Label(update_frame, text="Country:").grid(row=1, column=0)
            self.country_entry = ttk.Entry(update_frame)
            self.country_entry.insert(0, city.country)
            self.country_entry.grid(row=1, column=1)

            tk.Label(update_frame, text="Morning Price:").grid(row=2, column=0)
            self.morning_price_entry = ttk.Entry(update_frame)
            self.morning_price_entry.insert(0, city.price_morning)
            self.morning_price_entry.grid(row=2, column=1)

            tk.Label(update_frame, text="Afternoon Price:").grid(row=3, column=0)
            self.afternoon_price_entry = ttk.Entry(update_frame)
            self.afternoon_price_entry.insert(0, city.price_afternoon)
            self.afternoon_price_entry.grid(row=3, column=1)

            tk.Label(update_frame, text="Evening Price:").grid(row=4, column=0)
            self.evening_price_entry = ttk.Entry(update_frame)
            self.evening_price_entry.insert(0, city.price_evening)
            self.evening_price_entry.grid(row=4, column=1)

            def update_city_confirm(): # Updates it in database, checks for only new info to update. and displays cities again.
                name = self.name_entry.get()
                country = self.country_entry.get()
                morning_price = self.morning_price_entry.get()
                afternoon_price = self.afternoon_price_entry.get()
                evening_price = self.evening_price_entry.get()

                if name and not self.is_valid_name(name):
                    messagebox.showerror("Error", "Invalid name. Please enter a valid name.")
                    return
                if country and not self.is_valid_country(country):
                    messagebox.showerror("Error", "Invalid country. Please enter a valid country.")
                    return
                if morning_price and not self.is_valid_price(morning_price):
                    messagebox.showerror("Error", "Invalid morning price. Please enter a number.")
                    return
                if afternoon_price and not self.is_valid_price(afternoon_price):
                    messagebox.showerror("Error", "Invalid afternoon price. Please enter a number.")
                    return
                if evening_price and not self.is_valid_price(evening_price):
                    messagebox.showerror("Error", "Invalid evening price. Please enter a number.")
                    return

                # Only pass non-empty fields to the updated service.
                try:
                    self.city_service.update_city(
                        self.selected_city_id,
                        name if name else None,
                        country if country else None,
                        morning_price if morning_price else None,
                        afternoon_price if afternoon_price else None,
                        evening_price if evening_price else None,
                    )
                    CityManagement.update_window_open = False
                    self.manage_cities()
                    update_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            
            def cancel_update():
                CityManagement.update_window_open = False 
                update_frame.destroy()

            ttk.Button(update_frame, text="Confirm Update", command=update_city_confirm).grid(row=5, column=0, pady=5, padx=(0, 5))
            ttk.Button(update_frame, text="Cancel", command=cancel_update).grid(row=5, column=1, pady=5, padx=(5, 0)) 
        else:
            messagebox.showerror("Error", "Select a city to update.")
            CityManagement.update_window_open = False
            
    def remove_city(self): # Removes city from database.
        if self.selected_city_id: # If there is a city selected.
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this city?"):
                self.city_service.delete_city(self.selected_city_id)
                self.manage_cities()
        else:
            messagebox.showerror("Error", "Select a city to remove.")
        
    def browse_city(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse City")

        tk.Label(browse_window, text="City ID (Optional):").grid(row=0, column=0)
        city_id_entry = ttk.Entry(browse_window)
        city_id_entry.grid(row=0, column=1)

        city_name_label = tk.Label(browse_window, text="City Name:")
        city_name_entry = ttk.Entry(browse_window)
        country_label = tk.Label(browse_window, text="Country:")
        country_entry = ttk.Entry(browse_window)

        def find_city():
            city_id = city_id_entry.get()
            city_name = city_name_entry.get()
            country = country_entry.get()
            found = False

            if city_id:
                for item in self.city_list.get_children():
                    values = self.city_list.item(item, 'values')
                    if values and len(values) > 0 and str(values[0]) == city_id:
                        self.city_list.see(item)
                        self.city_list.selection_set(item)
                        self.city_list.focus(item)
                        self.selected_city_id = city_id
                        browse_window.destroy()
                        found = True
                        return
            elif city_name and country:
                for item in self.city_list.get_children():
                    values = self.city_list.item(item, 'values')
                    columns = self.city_list['columns']
                    city_name_column_index = columns.index('Name') if 'Name' in columns else -1
                    city_country_column_index = columns.index('Country') if 'Country' in columns else -1

                    if city_name_column_index != -1 and city_country_column_index != -1:
                        try:
                            if values[city_name_column_index] == city_name and values[city_country_column_index] == country:
                                self.city_list.see(item)
                                self.city_list.selection_set(item)
                                self.city_list.focus(item)
                                self.selected_city_id = values[0]
                                browse_window.destroy()
                                found = True
                                return
                        except IndexError:
                            continue

            if not found:
                if city_id == "" and city_name == "" and country == "":
                    messagebox.showerror("Error", "Please enter a City ID or both City Name and Country.")
                else:
                    messagebox.showerror("Error", "No matching city found.")


        def toggle_name_country_inputs():
            if city_id_entry.get():
                city_name_label.grid_forget()
                city_name_entry.grid_forget()
                country_label.grid_forget()
                country_entry.grid_forget()
            else:
                city_name_label.grid(row=1, column=0)
                city_name_entry.grid(row=1, column=1)
                country_label.grid(row=2, column=0)
                country_entry.grid(row=2, column=1)

        city_id_entry.bind("<KeyRelease>", lambda event: toggle_name_country_inputs())
        toggle_name_country_inputs()

        ttk.Button(browse_window, text="Find City", command=find_city).grid(row=3, column=0, columnspan=2, pady=10)

    def clear_city_frame(self):
        for widget in self.city_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")
