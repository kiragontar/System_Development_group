import tkinter as tk

class CinemaEditFrame(tk.Frame):
    """The cinema edit screen."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Edit Cinema", font=("Arial", 14, "bold"))
        label.pack(pady=5)

        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.location_label = tk.Label(self, text="Location:")
        self.location_label.pack()
        self.location_entry = tk.Entry(self)
        self.location_entry.pack()

        self.id_label = tk.Label(self, text="Cinema ID:")
        self.id_label.pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        self.city_id_label = tk.Label(self, text="City ID:")
        self.city_id_label.pack()
        self.city_id_entry = tk.Entry(self)
        self.city_id_entry.pack()

        save_button = tk.Button(self, text="Save", command=self.save_cinema)
        save_button.pack(pady=5)

        btn_back = tk.Button(
            self,
            text="Back to Cinema List",
            command=lambda: controller.show_frame("Cinemas")
        )
        btn_back.pack(pady=10)

    def show_cinema_details(self, name="", location="", cinema_id="", city_id=""):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)

        self.location_entry.delete(0, tk.END)
        self.location_entry.insert(0, location)

        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, cinema_id)

        self.city_id_entry.delete(0, tk.END)
        self.city_id_entry.insert(0, city_id)

    def save_cinema(self):
        # Get values from Entry widgets
        updated_name = self.name_entry.get().strip()
        updated_location = self.location_entry.get().strip()
        updated_id_str = self.id_entry.get().strip()
        updated_city_id_str = self.city_id_entry.get().strip()

        # Convert strings to integers carefully
        # (if these fields could be blank, handle it gracefully)
        updated_id = None
        updated_city_id = None

        if updated_id_str:
            try:
                updated_id = int(updated_id_str)
            except ValueError:
                print("Cinema ID must be an integer if provided.")

        if updated_city_id_str:
            try:
                updated_city_id = int(updated_city_id_str)
            except ValueError:
                print("City ID must be an integer if provided.")

        # 1) Check if cinema exists by ID
        existing_cinema = None
        if updated_id:
            existing_cinema = self.controller.cinema_service.get_cinema_by_id(updated_id)

        # 2) If it exists, update it
        if existing_cinema:
            self.controller.cinema_service.update_cinema(
                cinema_id=updated_id,
                name=updated_name,
                address=updated_location,
                city_id=updated_city_id
            )
            print(f"Cinema {updated_id} updated: {updated_name}, {updated_location}, city_id={updated_city_id}")
        else:
            # 3) If not found or no ID provided, create a new Cinema
            new_cinema = self.controller.cinema_service.create_cinema(
                name=updated_name,
                address=updated_location,
                city_id=updated_city_id
            )
            print(f"New cinema created with ID={new_cinema.cinema_id}, {updated_name}, {updated_location}, city_id={updated_city_id}")

        # Possibly navigate to some other frame
        self.controller.show_frame("Cinemas")

