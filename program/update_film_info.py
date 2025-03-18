import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Film, Cinema, CinemaFilm, City  # Import your models
from services.film_service import CinemaFilmService  # Import your service
import os

# Database connection
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Fetch the default cinema
cinema = session.query(Cinema).first()
if not cinema:
    messagebox.showerror("Error", "No cinema found in the database!")
    exit()

cinema_film_service = CinemaFilmService(cinema, session)

# Create the main application window
root = tk.Tk()
root.title("Cinema Film Management")
root.geometry("1200x700")

# Dictionary to store image references
poster_images = {}
selected_poster_path = None

# ===================== UI Components ===================== #

# **Frame to display movie posters**
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
    file_path = filedialog.askopenfilename(title="Select Movie Poster", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        selected_poster_path = os.path.relpath(file_path)
        messagebox.showinfo("Success", f"Poster selected: {selected_poster_path}")

# **Table to Display Films**
table_frame = tk.Frame(root)
table_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
columns = ("ID", "Name", "Genre", "Rating", "Runtime")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Genre", text="Genre")
tree.heading("Rating", text="Rating")
tree.heading("Runtime", text="Runtime")

tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Genre", width=200)
tree.column("Rating", width=100)
tree.column("Runtime", width=100)

def load_films():
    tree.delete(*tree.get_children())
    films = cinema_film_service.get_all_films()
    for film in films:
        genre_str = ", ".join(film.get_genre())
        tree.insert("", "end", values=(film.film_id, film.name, genre_str, film.critic_rating, film.runtime))

def edit_film():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a film to edit")
        return
    
    film_id = int(tree.item(selected_item, "values")[0])
    film = session.query(Film).get(film_id)
    
    if not film:
        messagebox.showerror("Error", "Film not found!")
        return
    
    display_poster(film)
    
    name_entry.delete(0, tk.END)
    genre_entry_add.delete(0, tk.END)
    rating_entry.delete(0, tk.END)
    runtime_entry.delete(0, tk.END)
    release_entry.delete(0, tk.END)
    description_entry.delete(1.0, tk.END)
    
    name_entry.insert(0, film.name)
    genre_entry_add.insert(0, ", ".join(film.get_genre()))
    rating_entry.insert(0, str(film.critic_rating))
    runtime_entry.insert(0, str(film.runtime))
    release_entry.insert(0, film.release_date.strftime("%Y-%m-%d"))
    description_entry.insert(tk.END, film.description)

def update_film():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a film to update")
        return
    
    film_id = int(tree.item(selected_item, "values")[0])
    film = session.query(Film).get(film_id)
    
    if not film:
        messagebox.showerror("Error", "Film not found!")
        return
    
    film.name = name_entry.get()
    film.critic_rating = float(rating_entry.get())
    film.runtime = int(runtime_entry.get())
    film.release_date = datetime.strptime(release_entry.get(), "%Y-%m-%d")
    film.description = description_entry.get("1.0", tk.END).strip()
    film.set_genre(genre_entry_add.get().split(", "))
    
    global selected_poster_path
    if selected_poster_path:
        film.movie_poster = selected_poster_path
    
    session.commit()
    messagebox.showinfo("Success", "Film updated successfully!")
    load_films()

def delete_film():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a film to delete")
        return
    
    film_id = int(tree.item(selected_item, "values")[0])
    cinema_film_service.remove_film_from_cinema(film_id)
    messagebox.showinfo("Success", "Film deleted successfully!")
    load_films()

tree.pack(pady=10, fill=tk.BOTH, expand=True)

# **Film Management Form (On Right Side, Aligned with Buttons)**
form_frame = tk.Frame(root)
form_frame.pack(side=tk.RIGHT, padx=20, pady=10)

for i, label_text in enumerate(["Film Name:", "Genre (comma separated):", "Critic Rating:", "Runtime (minutes):", "Release Date (YYYY-MM-DD):", "Description:"]):
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

description_entry = tk.Text(form_frame, height=4, width=30)
description_entry.grid(row=5, column=1, padx=5, pady=2)

poster_button = tk.Button(form_frame, text="Select Poster", command=select_poster)
poster_button.grid(row=6, columnspan=2, pady=5)

button_frame = tk.Frame(form_frame)
button_frame.grid(row=7, columnspan=2, pady=10)

edit_button = tk.Button(button_frame, text="Edit Selected Film", command=edit_film)
edit_button.pack(side=tk.LEFT, padx=5)

update_button = tk.Button(button_frame, text="Update Film", command=update_film)
update_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete Film", command=delete_film)
delete_button.pack(side=tk.LEFT, padx=5)


load_films()
root.mainloop()
