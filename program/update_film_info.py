import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Film, Cinema, CinemaFilm, City  # Import your models
from services.film_service import CinemaFilmService  # Import your service

# Database connection
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Create test data
city = City(name="London", country="UK")
session.add(city)
session.commit()

cinema = Cinema(name="Test Cinema", address="123 Test St", city_id=city.city_id)
session.add(cinema)
session.commit()

film1 = Film(name="Film 1", genre=["Action", "Sci-Fi"], cast=["Actor 1", "Actor 2"],
description="Description 1", age_rating="PG-13", critic_rating=7.5,
runtime=120, release_date=datetime(2024, 1, 1), movie_poster="poster1.jpg")

film2 = Film(name="Film 2", genre=["Comedy"], cast=["Actor 3", "Actor 4"],
description="Description 2", age_rating="PG", critic_rating=8.0,
runtime=105, release_date=datetime(2024, 2, 15), movie_poster="poster2.jpg")

session.add_all([film1, film2])
session.commit()

cinema_film1 = CinemaFilm(cinema_id=cinema.cinema_id, film_id=film1.film_id)

cinema_film2 = CinemaFilm(cinema_id=cinema.cinema_id, 
film_id=film2.film_id)

session.add_all([cinema_film1, cinema_film2])
session.commit()

# Fetch the default cinema (modify as needed)
cinema = session.query(Cinema).first()
cinema_film_service = CinemaFilmService(cinema, session)

# Create the main application window
root = tk.Tk()
root.title("Cinema Film Management")
root.geometry("900x500")

# ===================== UI Components ===================== #

# **Table to Display Films**
columns = ("ID", "Name", "Genre", "Rating", "Runtime")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Genre", text="Genre")
tree.heading("Rating", text="Critic Rating")
tree.heading("Runtime", text="Runtime (min)")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# **Function to Load Films into Table**
def load_films():
    for item in tree.get_children():
        tree.delete(item)  # Clear table
    films = cinema_film_service.get_all_films()
    for film in films:
        tree.insert("", "end", values=(film.film_id, film.name, ", ".join(film.genre), film.critic_rating, film.runtime))

load_films()

# **Search by Genre**
genre_label = tk.Label(root, text="Filter by Genre:")
genre_label.pack()
genre_entry = tk.Entry(root)
genre_entry.pack()

def filter_films():
    genre = genre_entry.get()
    if not genre:
        load_films()
        return
    films = cinema_film_service.get_all_films_by_genre(genre)
    for item in tree.get_children():
        tree.delete(item)
    for film in films:
        tree.insert("", "end", values=(film.film_id, film.name, ", ".join(film.genre), film.critic_rating, film.runtime))

filter_button = tk.Button(root, text="Filter", command=filter_films)
filter_button.pack()

# ===================== Film Management Buttons ===================== #

# **Add Film Form**
add_frame = tk.Frame(root)
add_frame.pack(pady=10)

name_label = tk.Label(add_frame, text="Film Name:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(add_frame)
name_entry.grid(row=0, column=1)

genre_label = tk.Label(add_frame, text="Genre (comma separated):")
genre_label.grid(row=1, column=0)
genre_entry_add = tk.Entry(add_frame)
genre_entry_add.grid(row=1, column=1)

rating_label = tk.Label(add_frame, text="Critic Rating:")
rating_label.grid(row=2, column=0)
rating_entry = tk.Entry(add_frame)
rating_entry.grid(row=2, column=1)

runtime_label = tk.Label(add_frame, text="Runtime (minutes):")
runtime_label.grid(row=3, column=0)
runtime_entry = tk.Entry(add_frame)
runtime_entry.grid(row=3, column=1)

release_label = tk.Label(add_frame, text="Release Date (YYYY-MM-DD):")
release_label.grid(row=4, column=0)
release_entry = tk.Entry(add_frame)
release_entry.grid(row=4, column=1)

# **Function to Add Film**
def add_film():
    name = name_entry.get()
    genre = [g.strip() for g in genre_entry_add.get().split(",") if g.strip()]
    rating = float(rating_entry.get())
    runtime = int(runtime_entry.get())
    release_date = datetime.strptime(release_entry.get(), "%Y-%m-%d")

    film = Film(
        name=name, genre=genre, cast=[], description="New Film", age_rating="PG",
        critic_rating=rating, runtime=runtime, release_date=release_date, movie_poster=""
    )

    session.add(film)
    session.commit()
    cinema_film_service.add_film_to_cinema(film)

    messagebox.showinfo("Success", f"Film '{name}' added successfully!")
    load_films()

add_button = tk.Button(add_frame, text="Add Film", command=add_film)
add_button.grid(row=5, columnspan=2, pady=5)

# **Delete Film**
def delete_film():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a film to delete")
        return

    film_id = tree.item(selected_item, "values")[0]  # Get ID
    cinema_film_service.remove_film_from_cinema(int(film_id))
    messagebox.showinfo("Deleted", "Film removed successfully!")
    load_films()

delete_button = tk.Button(root, text="Delete Selected Film", command=delete_film)
delete_button.pack(pady=5)

# **Update Film Details**
def update_film():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a film to update")
        return

    film_id = int(tree.item(selected_item, "values")[0])
    new_name = name_entry.get()
    new_genre = genre_entry_add.get().split(",")  # Convert string to list
    new_rating = float(rating_entry.get())
    new_runtime = int(runtime_entry.get())
    new_release_date = datetime.strptime(release_entry.get(), "%Y-%m-%d")

    updated_film = cinema_film_service.update_film(
        film_id=film_id,
        name=new_name,
        genre=new_genre,
        critic_rating=new_rating,
        runtime=new_runtime,
        release_date=new_release_date
    )

    if updated_film:
        messagebox.showinfo("Success", "Film updated successfully!")
        load_films()
    else:
        messagebox.showerror("Error", "Film not found!")

update_button = tk.Button(root, text="Update Selected Film", command=update_film)
update_button.pack(pady=5)

# ===================== Run the Application ===================== #
root.mainloop()
