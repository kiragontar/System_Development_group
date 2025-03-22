import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Film, Cinema, CinemaFilm, City
from services.film_service import CinemaFilmService
import os
import subprocess

# ===================== Database Setup ===================== #
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

cinema = session.query(Cinema).first()
if not cinema:
    messagebox.showerror("Error", "No cinema found in the database!")
    exit()

cinema_film_service = CinemaFilmService(cinema, session)

# ===================== GUI Setup ===================== #
root = tk.Tk()
root.title("Add New Film")
root.state('zoomed')  # Fullscreen

poster_images = {}
selected_poster_path = None

# ===================== Poster Display Frame ===================== #
poster_frame = tk.Frame(root)
poster_frame.pack(side=tk.LEFT, padx=10, pady=10)

poster_label = tk.Label(poster_frame, text="Movie Poster")
poster_label.pack()

poster_canvas = tk.Label(poster_frame)
poster_canvas.pack()

def display_poster(film):
    if film and film.movie_poster and os.path.exists(film.movie_poster):
        img = Image.open(film.movie_poster)
        img = img.resize((150, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        poster_canvas.config(image=img)
        poster_canvas.image = img
        poster_label.config(text="")
    else:
        poster_canvas.config(image="")
        poster_canvas.image = None
        poster_label.config(text="Movie Poster")

def select_poster():
    global selected_poster_path
    file_path = filedialog.askopenfilename(
        title="Select Movie Poster",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    if file_path:
        selected_poster_path = os.path.relpath(file_path)
        messagebox.showinfo("Success", f"Poster selected: {selected_poster_path}")

def open_update_film():
    try:
        subprocess.Popen(["python", "program\\update_film.py"])
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Update Film page:\n{e}")

def clear_form():
    name_entry.delete(0, tk.END)
    genre_entry_add.delete(0, tk.END)
    rating_entry.delete(0, tk.END)
    runtime_entry.delete(0, tk.END)
    release_entry.delete(0, tk.END)
    cast_entry.delete(0, tk.END)
    age_rating_var.set("U")
    description_entry.delete("1.0", tk.END)
    poster_canvas.config(image="")
    poster_canvas.image = None
    global selected_poster_path
    selected_poster_path = None
    poster_label.config(text="Movie Poster")

# ===================== Film Table ===================== #
table_frame = tk.Frame(root)
table_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

columns = ("ID", "Name", "Genre", "Rating", "Runtime", "Age Rating", "Cast")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Genre", width=200)
tree.column("Rating", width=70)
tree.column("Runtime", width=80)
tree.column("Age Rating", width=80)
tree.column("Cast", width=200)

tree.pack(pady=10, fill=tk.BOTH, expand=True)

def load_films():
    tree.delete(*tree.get_children())
    films = cinema_film_service.get_all_films()
    for film in films:
        genre_str = ", ".join(film.get_genre())
        tree.insert(
            "",
            "end",
            values=(
                film.film_id,
                film.name,
                genre_str,
                film.critic_rating,
                film.runtime,
                film.age_rating,
                film.cast
            )
        )

# ===================== Add Film Function ===================== #
def add_film_button():
    name = name_entry.get().strip()
    genres = genre_entry_add.get().strip().split(",")
    rating = rating_entry.get().strip()
    runtime = runtime_entry.get().strip()
    release = release_entry.get().strip()
    cast = cast_entry.get().strip()
    age_rating = age_rating_var.get()
    description = description_entry.get("1.0", tk.END).strip()

    if not all([name, genres, rating, runtime, release, description, cast, age_rating]):
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    try:
        release_date = datetime.strptime(release, "%Y-%m-%d")
        new_film = Film(
            name=name,
            critic_rating=float(rating),
            runtime=int(runtime),
            release_date=release_date,
            description=description,
            movie_poster=selected_poster_path,
            genre=[g.strip() for g in genres],
            cast=cast,
            age_rating=age_rating
        )
        session.add(new_film)
        session.commit()

        link = CinemaFilm(cinema_id=cinema.cinema_id, film_id=new_film.film_id)
        session.add(link)
        session.commit()

        messagebox.showinfo("Success", "New film added successfully!")
        load_films()
        clear_form()

    except Exception as e:
        session.rollback()
        messagebox.showerror("Error", f"Failed to add film:\n{e}")

# ===================== Delete Film Function ===================== #
def delete_film():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a film to delete")
        return

    film_id = int(tree.item(selected_item, "values")[0])

    session.query(CinemaFilm).filter_by(film_id=film_id).delete()
    session.query(Film).filter_by(film_id=film_id).delete()
    session.commit()

    messagebox.showinfo("Success", "Film deleted successfully!")
    load_films()

# ===================== Form Section ===================== #
form_frame = tk.Frame(root)
form_frame.pack(side=tk.RIGHT, padx=20, pady=10)

labels = [
    "Film Name:",
    "Genre (comma separated):",
    "Critic Rating:",
    "Runtime (minutes):",
    "Release Date (YYYY-MM-DD):",
    "Cast:",
    "Age Rating:",
    "Description:"
]

for i, label_text in enumerate(labels):
    tk.Label(form_frame, text=label_text).grid(row=i, column=0, padx=5, pady=2, sticky="w")

name_entry = tk.Entry(form_frame)
name_entry.grid(row=0, column=1, padx=5, pady=2)

genre_entry_add = tk.Entry(form_frame)
genre_entry_add.grid(row=1, column=1, padx=5, pady=2)

rating_entry = tk.Entry(form_frame)
rating_entry.grid(row=2, column=1, padx=5, pady=2)

runtime_entry = tk.Entry(form_frame)
runtime_entry.grid(row=3, column=1, padx=5, pady=2)

release_entry = tk.Entry(form_frame)
release_entry.grid(row=4, column=1, padx=5, pady=2)

cast_entry = tk.Entry(form_frame)
cast_entry.grid(row=5, column=1, padx=5, pady=2)

age_rating_var = tk.StringVar()
age_rating_dropdown = ttk.Combobox(form_frame, textvariable=age_rating_var, state="readonly")
age_rating_dropdown['values'] = ["U", "PG", "12A", "12", "15", "18", "R18"]
age_rating_dropdown.current(0)
age_rating_dropdown.grid(row=6, column=1, padx=5, pady=2)

description_entry = tk.Text(form_frame, height=4, width=30)
description_entry.grid(row=7, column=1, padx=5, pady=2)

# ===================== Poster Button ===================== #
poster_button = tk.Button(form_frame, text="Select Poster", command=select_poster)
poster_button.grid(row=8, columnspan=2, pady=5)

# ===================== Action Buttons ===================== #
button_frame = tk.Frame(form_frame)
button_frame.grid(row=9, columnspan=2, pady=10)

add_button = tk.Button(button_frame, text="Add Film", command=add_film_button)
add_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete Film", command=delete_film)
delete_button.pack(side=tk.LEFT, padx=5)

edit_film_button = tk.Button(button_frame, text="Edit Films", command=open_update_film)
edit_film_button.pack(side=tk.LEFT, padx=5)

# ===================== Initial Load ===================== #
load_films()
root.mainloop()
