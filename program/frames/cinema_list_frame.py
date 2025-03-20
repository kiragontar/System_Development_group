import tkinter as tk

class CinemaListFrame(tk.Frame):
    """The cinema selection screen."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Pick a Cinema", font=("Arial", 14, "bold"))
        label.pack(pady=5)

        self.cinemas_container = tk.Frame(self)
        self.cinemas_container.pack()

        btn_create = tk.Button(
            self,
            text="Create Cinema",
            command=lambda: controller.show_frame("CinemaEdit", "", "", "", "")
        )
        btn_create.pack(pady=5)

        btn_back = tk.Button(
            self,
            text="Back to Main",
            command=lambda: controller.show_frame("MainMenu")
        )
        btn_back.pack(pady=10)

        self.pack(fill="both", expand=True)  # Ensure the frame gets packed into the container

    def refresh_cinema_list(self):
        # Clear old data
        for widget in self.cinemas_container.winfo_children():
            widget.destroy()

        cinemas = self.controller.cinema_service.get_all_cinemas()
        for i in range(len(cinemas)):
            name = cinemas[i].name
            location = cinemas[i].address
            cinema_id = cinemas[i].cinema_id
            city_id = cinemas[i].city_id
            tk.Label(self.cinemas_container, text=f"{name} {location} {city_id} (ID: {cinema_id})").pack()

            edit_button = tk.Button(
                self.cinemas_container,
                text=f"Edit {name}",
                command=lambda n=name, loc=location, cinema_id=cinema_id, city_id=city_id: self.controller.show_frame("CinemaEdit", n, loc, cinema_id, city_id)
            )
            edit_button.pack()
