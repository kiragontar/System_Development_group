import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from database.database_settings import SessionLocal
from main_components.services.film_service import FilmService

class FilmManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.session = SessionLocal()
        self.film_service = FilmService(self.session)
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

        tk.Label(main_frame, text="Film Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        self.film_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.film_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_films()

    
    def manage_films(self):
        self.clear_film_frame()
        self.film_list = ttk.Treeview(
            self.film_frame,
            columns=("Film ID", "Name", "Genre", "Cast", "Description", "Age Rating", "Critic Rating", "Runtime", "Release Date"),
            show="headings",
        )
        self.film_list.heading("Film ID", text="Film ID")
        self.film_list.heading("Name", text="Name")
        self.film_list.heading("Genre", text="Genre")
        self.film_list.heading("Cast", text="Cast")
        self.film_list.heading("Description", text="Description")
        self.film_list.heading("Age Rating", text="Age Rating")
        self.film_list.heading("Critic Rating", text="Critic Rating")
        self.film_list.heading("Runtime", text="Runtime")
        self.film_list.heading("Release Date", text="Release Date")
        self.film_list.pack(expand=True, fill="both")

        films = self.film_service.get_all_films()
        for film in films:
            self.film_list.insert(
                "",
                tk.END,
                values=(film.film_id, film.name, film.genre, film.cast, film.description, film.age_rating, film.critic_rating, film.runtime, film.release_date),
            )

        action_frame = ttk.Frame(self.film_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add Film", command=self.add_film).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update Film", command=self.update_film).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Remove Film", command=self.remove_film).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse Film", command=self.browse_film).pack(side=tk.LEFT, padx=5)

        self.film_list.bind("<ButtonRelease-1>", self.select_film)
        self.selected_film_id = None
        self.selected_name = None
        self.selected_genre = None
        self.selected_cast = None
        self.selected_description = None
        self.selected_age_rating = None
        self.selected_critic_rating = None
        self.selected_runtime = None
        self.selected_release_date = None
        self.film_frame.update()

    def select_film(self, event):
        selection = self.film_list.selection()
        if selection:
            item = selection[0]
            values = self.film_list.item(item, "values")
            self.selected_film_id = values[0]
            self.selected_name = values[1]
            self.selected_genre = values[2]
            self.selected_cast = values[3]
            self.selected_description = values[4]
            self.selected_age_rating = values[5]
            self.selected_critic_rating = values[6]
            self.selected_runtime = values[7]
            self.selected_release_date = values[8]
        else:
            self.selected_film_id = None
            self.selected_name = None
            self.selected_genre = None
            self.selected_cast = None
            self.selected_description = None
            self.selected_age_rating = None
            self.selected_critic_rating = None
            self.selected_runtime = None
            self.selected_release_date = None

    def is_valid_name(self, name):
        return isinstance(name, str) and name.strip() != ""

    def is_valid_genre(self, genre):
        if not isinstance(genre, str):
            return False
        genres = [g.strip() for g in genre.split(',')]
        return all(g for g in genres)

    def is_valid_cast(self, cast):
        if not isinstance(cast, str):
            return False
        cast_members = [c.strip() for c in cast.split(',')]
        return all(c != "" for c in cast_members)
    
    def is_valid_description(self, description):
        return isinstance(description, str)

    def is_valid_age_rating(self, age_rating):
        return isinstance(age_rating, str) and age_rating in ["G", "PG", "PG-13", "R", "NC-17"]

    def is_valid_critic_rating(self, critic_rating):
        try:
            rating = float(critic_rating)
            return 0.0 <= rating <= 10.0
        except ValueError:
            return False

    def is_valid_runtime(self, runtime):
        try:
            runtime = int(runtime)
            return runtime > 0
        except ValueError:
            return False

    def is_valid_release_date(self, release_date):
        try:
            datetime.datetime.strptime(release_date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
        
    
    def add_film(self):
        if FilmManagement.add_window_open:
            messagebox.showerror("Error", "Add Film window is already open.")
            return

        FilmManagement.add_window_open = True

        add_frame = ttk.Frame(self.film_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        title_entry = ttk.Entry(add_frame)
        title_entry.grid(row=0, column=1, sticky=tk.W)

        tk.Label(add_frame, text="Genre:").grid(row=1, column=0, sticky=tk.W)
        genre_entry = ttk.Entry(add_frame)
        genre_entry.grid(row=1, column=1, sticky=tk.W)

        tk.Label(add_frame, text="Cast:").grid(row=2, column=0, sticky=tk.W)
        cast_entry = ttk.Entry(add_frame)
        cast_entry.grid(row=2, column=1, sticky=tk.W)

        tk.Label(add_frame, text="Description:").grid(row=3, column=0, sticky=tk.W)
        description_entry = tk.Text(add_frame, height=4, width=30)
        description_entry.grid(row=3, column=1, sticky=tk.W)

        tk.Label(add_frame, text="Age Rating:").grid(row=4, column=0, sticky=tk.W)
        age_rating_entry = ttk.Entry(add_frame)
        age_rating_entry.grid(row=4, column=1, sticky=tk.W)

        tk.Label(add_frame, text="Critic Rating:").grid(row=5, column=0, sticky=tk.W)
        critic_rating_entry = ttk.Entry(add_frame)
        critic_rating_entry.grid(row=5, column=1, sticky=tk.W)

        tk.Label(add_frame, text="Runtime:").grid(row=6, column=0, sticky=tk.W)
        runtime_entry = ttk.Entry(add_frame)
        runtime_entry.grid(row=6, column=1, sticky=tk.W)

        tk.Label(add_frame, text="Release Date:").grid(row=7, column=0, sticky=tk.W)
        release_date_entry = ttk.Entry(add_frame)
        release_date_entry.grid(row=7, column=1, sticky=tk.W)


        def add_film_confirm():
            name = title_entry.get()
            genre_string = genre_entry.get()
            genre = [g.strip() for g in genre_string.split(',')] if genre_string else []
            cast_string = cast_entry.get()
            cast = [c.strip() for c in cast_string.split(',')] if cast_string else []
            description = description_entry.get("1.0", tk.END).strip()
            age_rating = age_rating_entry.get()
            critic_rating = critic_rating_entry.get()
            runtime = runtime_entry.get()
            release_date = release_date_entry.get()

            if not self.is_valid_name(name):
                messagebox.showerror("Error", "Invalid Name. Must be a non-empty string.")
                return
            if not self.is_valid_genre(genre_string):
                messagebox.showerror("Error", "Invalid Genre. Must be a string with no numbers in each genre and genres seperated by commas.")
                return
            if not self.is_valid_cast(cast_string):
                messagebox.showerror("Error", "Invalid Cast. Must be a string seperated by commas.")
                return
            if not self.is_valid_description(description):
                messagebox.showerror("Error", "Invalid Description. Must be a string.")
                return
            if not self.is_valid_age_rating(age_rating):
                messagebox.showerror("Error", "Invalid Age Rating. Must be G, PG, PG-13, R, or NC-17.")
                return
            if not self.is_valid_critic_rating(critic_rating):
                messagebox.showerror("Error", "Invalid Critic Rating. Must be a number between 0.0 and 10.0.")
                return
            if not self.is_valid_runtime(runtime):
                messagebox.showerror("Error", "Invalid Runtime. Must be a positive integer.")
                return
            if not self.is_valid_release_date(release_date):
                messagebox.showerror("Error", "Invalid Release Date. Must be in YYYY-MM-DD format.")
                return

            try:
                self.film_service.create_film(name, genre, cast, description, age_rating, float(critic_rating), int(runtime), release_date)
                FilmManagement.add_window_open = False
                self.manage_films()
                add_frame.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def cancel_add():
            FilmManagement.add_window_open = False
            add_frame.destroy()

        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=5)

        ttk.Button(button_frame, text="Confirm Add", command=add_film_confirm).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=cancel_add).pack(side=tk.LEFT, padx=(5, 0))

    
    def update_film(self):
        if FilmManagement.update_window_open:
            messagebox.showerror("Error", "Update Film window is already open.")
            return
        FilmManagement.update_window_open = True

        if self.selected_film_id:

            update_frame = ttk.Frame(self.film_frame)
            update_frame.pack(pady=10)

            tk.Label(update_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
            name_entry = ttk.Entry(update_frame)
            name_entry.grid(row=0, column=1, sticky=tk.W)
            name_entry.insert(0, self.selected_name)

            tk.Label(update_frame, text="Genre:").grid(row=1, column=0, sticky=tk.W)
            genre_entry = ttk.Entry(update_frame)
            genre_entry.grid(row=1, column=1, sticky=tk.W)
            genre_entry.insert(0, self.selected_genre)

            tk.Label(update_frame, text="Cast:").grid(row=2, column=0, sticky=tk.W)
            cast_entry = ttk.Entry(update_frame)
            cast_entry.grid(row=2, column=1, sticky=tk.W)
            cast_entry.insert(0, self.selected_cast)

            tk.Label(update_frame, text="Description:").grid(row=3, column=0, sticky=tk.W)
            description_entry = tk.Text(update_frame, height=4, width=30)
            description_entry.grid(row=3, column=1, sticky=tk.W)
            description_entry.insert(tk.END, self.selected_description)

            tk.Label(update_frame, text="Age Rating:").grid(row=4, column=0, sticky=tk.W)
            age_rating_entry = ttk.Entry(update_frame)
            age_rating_entry.grid(row=4, column=1, sticky=tk.W)
            age_rating_entry.insert(0, self.selected_age_rating)

            tk.Label(update_frame, text="Critic Rating:").grid(row=5, column=0, sticky=tk.W)
            critic_rating_entry = ttk.Entry(update_frame)
            critic_rating_entry.grid(row=5, column=1, sticky=tk.W)
            critic_rating_entry.insert(0, self.selected_critic_rating)

            tk.Label(update_frame, text="Runtime:").grid(row=6, column=0, sticky=tk.W)
            runtime_entry = ttk.Entry(update_frame)
            runtime_entry.grid(row=6, column=1, sticky=tk.W)
            runtime_entry.insert(0, self.selected_runtime)

            tk.Label(update_frame, text="Release Date:").grid(row=7, column=0, sticky=tk.W)
            release_date_entry = ttk.Entry(update_frame)
            release_date_entry.grid(row=7, column=1, sticky=tk.W)
            release_date_entry.insert(0, self.selected_release_date)

            def update_film_confirm():
                name_str = name_entry.get()
                genre_str = genre_entry.get()
                cast_str = cast_entry.get()
                description_str = description_entry.get("1.0", tk.END).strip()
                age_rating_str = age_rating_entry.get()
                critic_rating_str = critic_rating_entry.get()
                runtime_str = runtime_entry.get()
                release_date_str = release_date_entry.get()

                name = None
                genre = None
                cast = None
                description = None
                age_rating = None
                critic_rating = None
                runtime = None
                release_date = None


                if name_str:
                    if not self.is_valid_name(name_str):
                        messagebox.showerror("Error", "Invalid Name. Must be a non-empty string.")
                        return
                    name = name_str

                if genre_str:
                    if not self.is_valid_genre(genre_str):
                        messagebox.showerror("Error", "Invalid Genre. Must be a string with no numbers in each genre, and genres separated by commas.")
                        return
                    genre = [g.strip() for g in genre_str.split(',')] if genre_str else None

                if cast_str:
                    if not self.is_valid_cast(cast_str):
                        messagebox.showerror("Error", "Invalid Cast. Must be a string separated by commas.")
                        return
                    cast = [c.strip() for c in cast_str.split(',')] if cast_str else None

                if description_str:
                    if not self.is_valid_description(description_str):
                        messagebox.showerror("Error", "Invalid Description. Must be a string.")
                        return
                    description = description_str

                if age_rating_str:
                    if not self.is_valid_age_rating(age_rating_str):
                        messagebox.showerror("Error", "Invalid Age Rating. Must be G, PG, PG-13, R, or NC-17.")
                        return
                    age_rating = age_rating_str

                if critic_rating_str:
                    if not self.is_valid_critic_rating(critic_rating_str):
                        messagebox.showerror("Error", "Invalid Critic Rating. Must be a number between 0.0 and 10.0.")
                        return
                    critic_rating = float(critic_rating_str)

                if runtime_str:
                    if not self.is_valid_runtime(runtime_str):
                        messagebox.showerror("Error", "Invalid Runtime. Must be a positive integer.")
                        return
                    runtime = int(runtime_str)

                if release_date_str:
                    if not self.is_valid_release_date(release_date_str):
                        messagebox.showerror("Error", "Invalid Release Date. Must be in YYYY-MM-DD format.")
                        return
                    release_date = release_date_str

                
                try:
                    self.film_service.update_film(self.selected_film_id, name, genre, cast, description, age_rating, critic_rating, runtime, release_date)
                    FilmManagement.update_window_open = False
                    self.manage_films()
                    update_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            def cancel_update():
                FilmManagement.update_window_open = False
                update_frame.destroy()

            button_frame = ttk.Frame(update_frame)
            button_frame.grid(row=8, column=0, columnspan=2, pady=5)

            ttk.Button(button_frame, text="Confirm Update", command=update_film_confirm).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(button_frame, text="Cancel", command=cancel_update).pack(side=tk.LEFT, padx=(5, 0))
        
        else:
            messagebox.showerror("Error", "Select a film to update.")
            FilmManagement.update_window_open = False


    def remove_film(self):
        if self.selected_film_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this film?"):
                try:
                    self.film_service.delete_film(self.selected_film_id)
                    self.manage_films()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Select a film to remove.")


    def browse_film(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse Film")

        tk.Label(browse_window, text="Film ID:").grid(row=0, column=0)
        film_id_entry = ttk.Entry(browse_window)
        film_id_entry.grid(row=0, column=1)

        def find_film():
            film_id = film_id_entry.get()
            found = False

            if film_id:
                for item in self.film_list.get_children():
                    values = self.film_list.item(item, 'values')
                    if values and len(values) > 0 and str(values[0]) == film_id:
                        self.film_list.see(item)
                        self.film_list.selection_set(item)
                        self.film_list.focus(item)
                        self.selected_film_id = values[0]
                        self.selected_name = values[1]
                        self.selected_genre = values[2]
                        self.selected_cast = values[3]
                        self.selected_description = values[4]
                        self.selected_age_rating = values[5]
                        self.selected_critic_rating = values[6]
                        self.selected_runtime = values[7]
                        self.selected_release_date = values[8]
                        browse_window.destroy()
                        found = True
                        return

            if not found:
                if not film_id:
                    messagebox.showerror("Error", "Please enter a Film ID.")
                else:
                    messagebox.showerror("Error", "No matching film found.")

        ttk.Button(browse_window, text="Find Film", command=find_film).grid(row=1, column=0, columnspan=2, pady=10)

    def clear_film_frame(self):
        for widget in self.film_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")
        
    

