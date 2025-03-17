import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize the main application window
def initialize_window():
    root = tk.Tk()
    root.title("WOWOWOWOWOWOWOWOWOWOWOWOWOWOWOW")
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    return root

# Set up the main colors and fonts
header_color = "#333333"
top_bg_color = "#f8f8f8"
text_color = "#333333"
header_font = ("Helvetica", 24, "bold")
subheader_font = ("Helvetica", 14)
button_font = ("Helvetica", 16, "bold")

# Carousel movie data (now genres are separate)
carousel_movies = [
    {"title": "Spider-Man: No Way Home", "genres": ["Action", "Adventure"], "rating": "4.5", "description": "With Spider-Man's identity now revealed...", "showtimes": ["12:00 PM", "3:00 PM", "6:00 PM"], "image_path": "Movie_images/spider_man.png"},
    {"title": "The Matrix Resurrections", "genres": ["Sci-Fi"], "rating": "4.0", "description": "Plagued by strange memories, Neo's life takes an unexpected turn...", "showtimes": ["1:00 PM", "4:00 PM", "8:00 PM"], "image_path": "Movie_images/matrix_ressurection.png"},
    {"title": "Oppenheimer", "genres": ["Biography"], "rating": "4.7", "description": "The story of J. Robert Oppenheimer and his role in the development of the atomic bomb.", "showtimes": ["11:00 AM", "2:00 PM", "5:00 PM"], "image_path": "Movie_images/Oppenheimer.png"},
    {"title": "Inside Out 2", "genres": ["Animation"], "rating": "4.6", "description": "Follow Riley as she navigates new emotions and challenges during her teenage years.", "showtimes": ["12:30 PM", "3:30 PM", "7:30 PM"], "image_path": "Movie_images/inside_out_2.png"},
    {"title": "Venom: Let There Be Carnage", "genres": ["Action", "Sci-Fi"], "rating": "4.1", "description": "Eddie Brock attempts to reignite his career...", "showtimes": ["10:00 AM", "1:00 PM", "4:00 PM"], "image_path": "Movie_images/venom.png"},
    {"title": "Five Nights at Freddy's", "genres": ["Horror"], "rating": "4.0", "description": "A troubled security guard begins working at Freddy Fazbear's Pizza...", "showtimes": ["7:00 PM", "9:00 PM"], "image_path": "Movie_images/five_nights_at_freddy.png"},
    {"title": "Alien: Romulus", "genres": ["Horror"], "rating": "4.0", "description": "A group of young space colonists come face to face with the most terrifying life form in the universe.", "showtimes": ["9:00 PM", "11:00 PM"], "image_path": "Movie_images/alien_romulus.png"},
    {"title": "A Quiet Place: Day One", "genres": ["Horror"], "rating": "4.2", "description": "A young woman named Sam finds herself trapped in New York City during the early stages of an invasion by alien creatures with ultra-sensitive hearing.", "showtimes": ["6:00 PM", "9:00 PM"], "image_path": "Movie_images/a_quiet_place_day_one.png"},
    {"title": "Carnage for Christmas", "genres": ["Horror"], "rating": "3.9", "description": "Lola, a true-crime podcaster, returns home for Christmas only to face a vengeful ghost reenacting the murders of a historical killer.", "showtimes": ["8:00 PM", "10:00 PM"], "image_path": "Movie_images/carnage_for_christmas.png"},
    {"title": "Dune Part 2", "genres": ["Action", "Adventure"], "rating": "4.8", "description": "Paul Atreides unites with the Fremen while on a warpath of revenge.", "showtimes": ["12:00 PM", "3:00 PM", "6:00 PM"], "image_path": "Movie_images/dune_part_2.png"},
    {"title": "Twister", "genres": ["Action", "Adventure"], "rating": "4.4", "description": "Kate Carter, a retired tornado-chaser, is persuaded to return to Oklahoma.", "showtimes": ["1:00 PM", "4:00 PM", "7:00 PM"], "image_path": "Movie_images/twister.png"},
    {"title": "Civil War", "genres": ["Action", "Adventure"], "rating": "4.6", "description": "A journey across a dystopian future America.", "showtimes": ["2:00 PM", "5:00 PM", "8:00 PM"], "image_path": "Movie_images/civil_war.png"},
    {"title": "Mission: Impossible - Dead Reckoning Part One", "genres": ["Action", "Adventure"], "rating": "4.7", "description": "Ethan Hunt and his IMF team must track down a dangerous weapon.", "showtimes": ["10:00 AM", "1:00 PM", "4:00 PM"], "image_path": "Movie_images/mission_impossible.png"},
    {"title": "Gladiator II", "genres": ["Action", "Adventure"], "rating": "4.6", "description": "Maximus returns to seek revenge in a new chapter of his journey.", "showtimes": ["11:00 AM", "2:00 PM", "5:00 PM"], "image_path": "Movie_images/gladiator_ii.png"}
]

carousel_image_labels = []
carousel_index = 0

# Function to sort and categorize movies into their respective sections
def categorize_movies():
    action_adventure_movies = []
    horror_movies = []
    sci_fi_movies = []
    animation_movies = []
    biography_movies = []

    for movie in carousel_movies:
        for genre in movie["genres"]:
            if "Action" in genre:
                action_adventure_movies.append(movie)
            elif genre == "Horror":
                horror_movies.append(movie)
            elif genre == "Sci-Fi":
                sci_fi_movies.append(movie)
            elif genre == "Animation":
                animation_movies.append(movie)
            elif genre == "Biography":
                biography_movies.append(movie)

    return action_adventure_movies, horror_movies, sci_fi_movies, animation_movies, biography_movies

selection_frame = None
overlay_frame = None

def create_header(root):
    global selection_frame, overlay_frame  # Ensure we're referencing the global variables

    # Main header setup
    header_frame = tk.Frame(root, bg=header_color, height=100)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    logo_label = tk.Label(header_frame, text="CineWatch", font=header_font, bg=header_color, fg="white")
    logo_label.pack(side="left", padx=20, pady=10)

    search_entry = tk.Entry(header_frame, width=50, font=subheader_font)
    search_entry.pack(side="left", padx=50)

    login_label = tk.Label(header_frame, text="Hello Guest! Login/Signup", font=subheader_font, bg=header_color, fg="white")
    login_label.pack(side="right", padx=20)
    

    # Select Cinema button
    select_city_button = tk.Button(header_frame, text="Select Cinema", font=subheader_font, bg="#ff4d4d", fg="white", command=open_selection_frame)
    select_city_button.pack(side="left", padx=20, pady=5)

def open_selection_frame():
    global selection_frame, overlay_frame

    # Create the selection frame for city and cinema with a white background and a border
    selection_frame = tk.Frame(root, bg="white", width=600, height=400, relief="solid", bd=3)
    selection_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame
    selection_frame.pack_propagate(False)  # Prevent the frame from shrinking to fit its children

    # Add padding between the elements
    city_label = tk.Label(selection_frame, text="Select City:", font=("Helvetica", 14, "bold"), bg="white")
    city_label.pack(pady=15)

    city_options = ["x", "y", "z", "h"]
    city_dropdown = ttk.Combobox(selection_frame, values=city_options, font=("Helvetica", 12), state="readonly")
    city_dropdown.pack(pady=10, padx=20)

    cinema_label = tk.Label(selection_frame, text="Select Cinema:", font=("Helvetica", 14, "bold"), bg="white")
    cinema_label.pack(pady=15)

    cinema_options = ["Cinema 1", "Cinema 2", "Cinema 3", "Cinema 4"]
    cinema_dropdown = ttk.Combobox(selection_frame, values=cinema_options, font=("Helvetica", 12), state="readonly")
    cinema_dropdown.pack(pady=10, padx=20)

    close_button = tk.Button(selection_frame, text="Close", command=close_selection_frame, font=("Helvetica", 12, "bold"), bg="#ff4d4d", fg="white", relief="solid")
    close_button.pack(pady=20)

def close_selection_frame(event=None):
    global selection_frame, overlay_frame
    if selection_frame:
        selection_frame.destroy()
    if overlay_frame:
        overlay_frame.destroy()
    selection_frame = None
    overlay_frame = None

def create_footer(root):
    footer_frame = tk.Frame(root, bg=header_color, height=60)
    footer_frame.pack(fill="x", side="bottom")

    footer_label = tk.Label(footer_frame, text="©2022 CineWatch", font=("Helvetica", 10), bg=header_color, fg="white")
    footer_label.pack(pady=20)

def create_scrollable_area(root):
    canvas = Canvas(root, bg=top_bg_color, highlightthickness=0)
    canvas.pack(side="top", fill="both", expand=True)

    scrollbar = Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    main_frame = Frame(canvas, bg=top_bg_color)
    canvas.create_window((0, 0), window=main_frame, anchor="nw")

    main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    return main_frame

def move_left():
    global carousel_index
    carousel_index = (carousel_index - 1) % len(carousel_movies)
    update_carousel()

def move_right():
    global carousel_index
    carousel_index = (carousel_index + 1) % len(carousel_movies)
    update_carousel()

def update_carousel():
    for i, img_label in enumerate(carousel_image_labels):
        movie_index = (carousel_index + i) % len(carousel_movies)
        movie = carousel_movies[movie_index]
        # Adjusted size for larger images
        # img = Image.open(movie["image_path"]).resize((450, 250), Image.LANCZOS)  
        # photo = ImageTk.PhotoImage(img)
        # img_label.config(image=photo)
        # img_label.image = photo
        # img_label.bind("<Button-1>", lambda e, m=movie: show_movie_details(m))

def create_carousel(main_frame):
    carousel_frame = tk.Frame(main_frame, bg=top_bg_color)
    carousel_frame.pack(pady=50, fill="x", expand=True)

    num_movies = 3  # Show 4 images at once
    carousel_frame.grid_columnconfigure(0, weight=0)  #left arrow
    carousel_frame.grid_columnconfigure(1, weight=1)
    carousel_frame.grid_columnconfigure(2, weight=1)
    carousel_frame.grid_columnconfigure(3, weight=1)
    carousel_frame.grid_columnconfigure(5, weight=0)  # Right arrow, no expansion

    left_arrow = tk.Button(carousel_frame, text="<", command=move_left, font=button_font, bg=header_color, fg="white")
    left_arrow.grid(row=0, column=0, padx=10, pady=10)

    movie_width = (root.winfo_width() - 50) // num_movies
    movie_height = 350

    for i in range(num_movies):
        movie_frame = tk.Frame(carousel_frame, bg=top_bg_color, width=movie_width, height=movie_height)
        movie_frame.grid(row=0, column=i + 1, padx=10, pady=10)

        img_label = tk.Label(movie_frame, bg=top_bg_color)
        img_label.pack(pady=5)

        carousel_image_labels.append(img_label)

    right_arrow = tk.Button(carousel_frame, text=">", command=move_right, font=button_font, bg=header_color, fg="white")
    right_arrow.grid(row=0, column=num_movies+1, padx=10, pady=10)

    update_carousel()


def update_movie_sections():
    action_adventure_movies, horror_movies, sci_fi_movies, animation_movies, biography_movies = categorize_movies()

    display_movie_section(main_frame, "Action & Adventure", action_adventure_movies)
    display_movie_section(main_frame, "Horror", horror_movies)
    display_movie_section(main_frame, "Sci-Fi", sci_fi_movies)
    display_movie_section(main_frame, "Animation", animation_movies)
    display_movie_section(main_frame, "Biography", biography_movies)

def display_movie_section(main_frame, section_title, movies):
    section_label = tk.Label(main_frame, text=section_title, font=subheader_font, bg=top_bg_color, fg=text_color)
    section_label.pack(anchor="w", pady=5)

    section_movie_frame = tk.Frame(main_frame, bg=top_bg_color)
    section_movie_frame.pack(anchor="w", pady=5, fill="x")

    # Store the movie frames in the section and the current visible index
    section_movie_frame.movie_frames = []
    section_movie_frame.first_visible_index = 0  # Track the first visible movie index

    # Check if more than 6 movies exist, then add navigation arrows
    if len(movies) > 6:
        # Left arrow button
        left_button = tk.Button(section_movie_frame, text="<", command=lambda: scroll_movies(section_movie_frame, movies, -1), font=button_font, bg=header_color, fg="white")
        left_button.pack(side="left", padx=10, pady=10)

        # Right arrow button
        right_button = tk.Button(section_movie_frame, text=">", command=lambda: scroll_movies(section_movie_frame, movies, 1), font=button_font, bg=header_color, fg="white")
        right_button.pack(side="right", padx=10, pady=10)

    # Create the first set of movie frames (6 movies)
    movie_frames = []
    for i in range(6):  # Display the first 6 movies by default
        if i < len(movies):
            movie = movies[i]
            movie_frame = tk.Frame(section_movie_frame, bg="white", bd=2, relief="raised", width=220, height=350)
            movie_frame.pack(side="left", padx=10, pady=10)
            movie_frame.pack_propagate(False)

            img = Image.open(movie["image_path"]).resize((200, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(movie_frame, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(pady=5)
            img_label.bind("<Button-1>", lambda e, m=movie: show_movie_details(m))

            # Display the title in the genre section
            title_label = tk.Label(movie_frame, text=movie["title"], font=("Helvetica", 12, "bold"), fg=text_color, bg="white", wraplength=200, anchor="center")
            title_label.pack(pady=5)
            title_label.bind("<Button-1>", lambda e, m=movie: show_movie_details(m))

            genre_label = tk.Label(movie_frame, text=movie.get("genre", ""), font=("Helvetica", 10), fg="gray", bg="white")
            genre_label.pack(pady=5)

            movie_frames.append(movie_frame)

    # Store the frames in the section for scrolling
    section_movie_frame.movie_frames = movie_frames

def scroll_movies(section_movie_frame, movies, direction):
    """Scroll through the movies when clicking left or right arrow"""
    # Get the current first visible movie index
    first_visible_movie_index = section_movie_frame.first_visible_index

    # Calculate the new first visible movie index based on the direction
    if direction == -1:  # Move left
        first_visible_movie_index = max(0, first_visible_movie_index - 1)
    elif direction == 1:  # Move right
        first_visible_movie_index = min(len(movies) - 6, first_visible_movie_index + 1)

    # Clear the current movie frames but keep the arrows
    for widget in section_movie_frame.winfo_children():
        if isinstance(widget, tk.Frame):  # Only destroy movie frames
            widget.destroy()

    # Create new movie frames based on the new first visible movie index
    for i in range(first_visible_movie_index, first_visible_movie_index + 6):
        if i < len(movies):
            movie = movies[i]
            movie_frame = tk.Frame(section_movie_frame, bg="white", bd=2, relief="raised", width=220, height=350)
            movie_frame.pack(side="left", padx=10, pady=10)
            movie_frame.pack_propagate(False)

            img = Image.open(movie["image_path"]).resize((200, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(movie_frame, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(pady=5)
            img_label.bind("<Button-1>", lambda e, m=movie: show_movie_details(m))

            # Display the title in the genre section
            title_label = tk.Label(movie_frame, text=movie["title"], font=("Helvetica", 12, "bold"), fg=text_color, bg="white", wraplength=200, anchor="center")
            title_label.pack(pady=5)
            title_label.bind("<Button-1>", lambda e, m=movie: show_movie_details(m))

            genre_label = tk.Label(movie_frame, text=movie.get("genre", ""), font=("Helvetica", 10), fg="gray", bg="white")
            genre_label.pack(pady=5)

    # Update the first visible movie index
    section_movie_frame.first_visible_index = first_visible_movie_index

def show_movie_details(movie):
    details_window = tk.Toplevel(root)
    details_window.title(movie["title"])
    details_window.configure(bg=top_bg_color)
    details_window.attributes("-fullscreen", True)

    tk.Label(details_window, text=movie["title"], font=header_font, bg=top_bg_color, fg=text_color).pack(pady=10)
    img = Image.open(movie["image_path"]).resize((300, 450), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(details_window, image=photo, bg=top_bg_color)
    img_label.image = photo
    img_label.pack(pady=10)

    tk.Label(details_window, text=f"Genre: {', '.join(movie['genres'])}", font=subheader_font, bg=top_bg_color, fg=text_color).pack(pady=5)
    tk.Label(details_window, text=f"Rating: {movie['rating']} ★", font=subheader_font, bg=top_bg_color, fg=text_color).pack(pady=5)
    tk.Label(details_window, text="Description:", font=subheader_font, bg=top_bg_color, fg=text_color).pack(pady=5)
    tk.Label(details_window, text=movie["description"], wraplength=750, bg=top_bg_color, fg=text_color).pack(pady=5)
    tk.Label(details_window, text="Showtimes:", font=subheader_font, bg=top_bg_color, fg=text_color).pack(pady=10)
    for time in movie["showtimes"]:
        tk.Label(details_window, text=time, bg=top_bg_color, fg=text_color).pack()

    close_button = tk.Button(details_window, text="Close", command=details_window.destroy, font=button_font, bg=header_color, fg="white")
    close_button.pack(pady=20)

# Main execution
root = initialize_window()
create_header(root)
main_frame = create_scrollable_area(root)
create_carousel(main_frame)
update_movie_sections()  # Update movie sections with new data
create_footer(root)
root.mainloop()
