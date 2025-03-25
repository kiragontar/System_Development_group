# frontend/cinema.py
import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO
import sys, os

# Add the project root to the path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.role_service import RoleService
from backend.models import Base
from role_management import run_role_management
from permission_management import run_permission_management

# Try importing the role management module
try:
    from role_management import run_role_management
except ImportError as e:
    print(f"Critical import error: {e}")
    def run_role_management(admin_window, session):
        messagebox.showinfo("Info", "Role management module not available.")

engine = None

# ====== Sample Movie Data ======
movies_data = [
    {
        "title": "The Shawshank Redemption",
        "rating": "9.3",
        "shows": [{"show_no": 1, "time": "10:00", "seats": 50}],
        "details": (
            "The Shawshank Redemption\n"
            "IMDb Rating: 9.3\n"
            "Drama, 1994, 2h 22m\n"
            "Cast: Tim Robbins, Morgan Freeman, Bob Gunton\n"
            "Plot: A man wrongfully imprisoned forms an unbreakable bond and hatches a plan for redemption."
        )
    },
    {
        "title": "Inception",
        "rating": "8.8",
        "shows": [{"show_no": 1, "time": "11:00", "seats": 45}],
        "details": (
            "Inception\n"
            "IMDb Rating: 8.8\n"
            "Sci-Fi, Thriller, 2010, 2h 28m\n"
            "Cast: Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page\n"
            "Plot: A skilled thief enters people's dreams to steal secrets, but a new mission challenges his reality."
        )
    },
    {
        "title": "The Dark Knight",
        "rating": "9.0",
        "shows": [{"show_no": 1, "time": "12:00", "seats": 40}],
        "details": (
            "The Dark Knight\n"
            "IMDb Rating: 9.0\n"
            "Action, Crime, 2008, 2h 32m\n"
            "Cast: Christian Bale, Heath Ledger, Aaron Eckhart\n"
            "Plot: Batman faces a new nemesis who aims to plunge Gotham into anarchy."
        )
    },
    {
        "title": "Pulp Fiction",
        "rating": "8.9",
        "shows": [{"show_no": 1, "time": "09:00", "seats": 30}],
        "details": (
            "Pulp Fiction\n"
            "IMDb Rating: 8.9\n"
            "Crime, Drama, 1994, 2h 34m\n"
            "Cast: John Travolta, Uma Thurman, Samuel L. Jackson\n"
            "Plot: Various interconnected stories of criminals in Los Angeles."
        )
    },
    {
        "title": "Forrest Gump",
        "rating": "8.8",
        "shows": [{"show_no": 1, "time": "10:30", "seats": 35}],
        "details": (
            "Forrest Gump\n"
            "IMDb Rating: 8.8\n"
            "Drama, Romance, 1994, 2h 22m\n"
            "Cast: Tom Hanks, Robin Wright, Gary Sinise\n"
            "Plot: A man with a low IQ witnesses and participates in major historical events."
        )
    },
    {
        "title": "The Matrix",
        "rating": "8.7",
        "shows": [{"show_no": 1, "time": "11:30", "seats": 40}],
        "details": (
            "The Matrix\n"
            "IMDb Rating: 8.7\n"
            "Sci-Fi, Action, 1999, 2h 16m\n"
            "Cast: Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss\n"
            "Plot: A hacker discovers a dystopian reality and joins a rebellion."
        )
    }
]

def main(user=None):
    """
    The main function now accepts a 'user' parameter which holds the logged-in user's information.
    """
    global engine
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Database setup
    DATABASE_URL = "mysql+pymysql://shrimp:shrimp@127.0.0.1:3306/cinema"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    RoleService(session)
    # Main window configuration
    root = tk.Tk()
    root.title("Ticket Booking System")
    root.geometry("1280x720")
    bg_color = "#6e7c91"
    label_color = "#4378a1"
    root.configure(bg=bg_color)
    
    style = ttk.Style(root)
    style.theme_use("clam")
    accent_blue = "#4b86b3"
    accent_green = "#b8f17e"
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=label_color, foreground="white")
    style.configure("Header.TLabel", background=accent_blue, foreground="white", font=("Arial", 20, "bold"))
    style.configure("ShowHeader.TLabel", background=accent_blue, foreground="white", font=("Arial", 12, "bold"))
    style.configure("Treeview", background="#7495b3", foreground="white", fieldbackground="#7495b3", font=("Arial", 12))
    style.configure("Treeview.Heading", background=accent_blue, foreground="white", font=("Arial", 12, "bold"))
    style.configure("Colored.TButton", background=accent_blue, foreground="white", font=("Arial", 12, "bold"))
    style.configure("User.TButton", background=accent_blue, foreground="white", font=("Arial", 12, "bold"))
    
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill='both', expand=True)
    
    # Top bar with admin panel and user info
    top_bar = ttk.Frame(main_frame)
    top_bar.pack(fill='x')
    
    def open_admin_panel():
        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Panel")
        admin_window.geometry("600x400")
        if user and user.role.name == "Admin":
            ttk.Button(admin_window, text="Manage Roles", 
                     command=lambda: run_role_management(admin_window, session),
                     style="Colored.TButton").pack(pady=20)
            ttk.Button(admin_window, text="Manage Permissions", 
                     command=lambda: run_permission_management(admin_window, session),
                     style="Colored.TButton").pack(pady=20)
        else:
            ttk.Label(admin_window, text="⛔ Admin Access Required", 
                    style="Header.TLabel").pack(pady=50)
    
    admin_button = ttk.Button(top_bar, text="Admin Panel", style="Colored.TButton", command=open_admin_panel)
    admin_button.pack(side="left", padx=10, pady=10)
    
    # Load user icon image (optional)
    user_display = user.firstname if user and hasattr(user, "firstname") else "User"
    try:
        url = "https://static.vecteezy.com/system/resources/previews/007/335/692/non_2x/account-icon-template-vector.jpg"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        if hasattr(Image, 'Resampling'):
            im = im.resize((40, 40), Image.Resampling.LANCZOS)
        else:
            im = im.resize((40, 40), Image.ANTIALIAS)
        user_icon = ImageTk.PhotoImage(im)
    except Exception as e:
        print("Error loading image:", e)
        user_icon = None

    user_icon_btn = ttk.Button(top_bar, text=user_display, style="User.TButton")
    if user_icon:
        user_icon_btn.config(image=user_icon, compound="left")
        user_icon_btn.image = user_icon
    user_icon_btn.pack(side="right", padx=10, pady=10)
    
    # User menu toggling functionality
    user_menu_visible = False
    user_menu = None

    def close_user_menu():
        nonlocal user_menu, user_menu_visible
        if user_menu is not None:
            user_menu.destroy()
            user_menu = None
            user_menu_visible = False
            root.unbind("<Button-1>")

    def check_click_outside(event):
        nonlocal user_menu
        if user_menu is not None:
            menu_x = user_menu.winfo_rootx()
            menu_y = user_menu.winfo_rooty()
            menu_width = user_menu.winfo_width()
            menu_height = user_menu.winfo_height()
            if not (menu_x <= event.x_root <= menu_x + menu_width and 
                    menu_y <= event.y_root <= menu_y + menu_height):
                icon_x = user_icon_btn.winfo_rootx()
                icon_y = user_icon_btn.winfo_rooty()
                icon_width = user_icon_btn.winfo_width()
                icon_height = user_icon_btn.winfo_height()
                if not (icon_x <= event.x_root <= icon_x + icon_width and 
                        icon_y <= event.y_root <= icon_y + icon_height):
                    close_user_menu()

    def toggle_user_menu():
        nonlocal user_menu, user_menu_visible
        if user_menu_visible and user_menu is not None:
            close_user_menu()
            return
        user_menu = tk.Toplevel(root)
        user_menu.overrideredirect(True)
        menu_frame = ttk.Frame(user_menu, style="TFrame")
        menu_frame.pack(fill="both", expand=True)
        
        actual_username = user.username if user and hasattr(user, "username") else "N/A"
        user_name_label = ttk.Label(menu_frame, text=f"Username: {actual_username}", padding=5,
                                    background=accent_blue, foreground="white", font=("Arial", 12))
        user_name_label.pack(fill='x')
        user_name_label.bind("<Button-1>", lambda event: close_user_menu())
        
        def sign_out():
            close_user_menu()
            messagebox.showinfo("Sign Out", "Signed out successfully")
            root.destroy()   # Close cinema window
            import login
            login.run_login()  # Link back to login screen
        
        signout_btn = ttk.Button(menu_frame, text="Sign Out", command=sign_out, style="Colored.TButton")
        signout_btn.pack(fill='x')
        
        user_menu_visible = True
        user_menu.update_idletasks()
        menu_width = user_menu.winfo_width()
        icon_x = user_icon_btn.winfo_rootx()
        icon_y = user_icon_btn.winfo_rooty()
        icon_width = user_icon_btn.winfo_width()
        x = icon_x + icon_width - menu_width + 18
        y = icon_y + user_icon_btn.winfo_height()
        user_menu.geometry(f"+{x}+{y}")
        root.after(100, lambda: root.bind("<Button-1>", check_click_outside))

    user_icon_btn.config(command=toggle_user_menu)
    
    # Header label
    header_label = ttk.Label(main_frame, text="Linity Cinemas\nBristol \nCurated by James Sunderland | 2025",
                             style="Header.TLabel", anchor="center")
    header_label.pack(pady=10, anchor="center")
    
    # Movie tables grid
    tables_frame = ttk.Frame(main_frame)
    tables_frame.pack(fill='both', expand=True)
    
    columns = ("showtime", "seats")
    
    # Define the callback first so it is available for binding.
    def on_select(event, movie):
        info_label.config(text=movie["details"])

    for i, movie in enumerate(movies_data):
        row = i // 3
        col = i % 3
        movie_frame = ttk.Frame(tables_frame, padding=5)
        movie_frame.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
        tables_frame.columnconfigure(col, weight=1)
        tables_frame.rowconfigure(row, weight=1)
        show_header = ttk.Label(movie_frame, text="Show 1", style="ShowHeader.TLabel",
                                anchor="center", padding=(0, 5))
        show_header.pack(fill='x')
        tree = ttk.Treeview(movie_frame, columns=columns, show='headings', height=1)
        tree.pack(fill='both', expand=True)
        tree.heading("showtime", text="Time", anchor="center")
        tree.heading("seats", text="Seats", anchor="center")
        tree.column("showtime", width=70, anchor="center")
        tree.column("seats", width=60, anchor="center")
        for show in movie["shows"]:
            tree.insert("", "end", values=(show["time"], show["seats"]))
        title_label = ttk.Label(movie_frame, text=movie["title"], style="TLabel",
                                font=("Arial", 12, "bold"), anchor="center", padding=(0, 5))
        title_label.pack(fill='x')
        tree.bind("<<TreeviewSelect>>", lambda e, m=movie: on_select(e, m))
    
    # Movie details display
    info_label = ttk.Label(main_frame, text="Select a show to see movie details...", font=("Arial", 12),
                           wraplength=1200, anchor="center")
    info_label.pack(pady=10, fill='x')
    
    # Navigation buttons
    nav_frame = ttk.Frame(main_frame)
    nav_frame.pack(fill='x', pady=10)
    main_menu_btn = ttk.Button(nav_frame, text="Main Menu", style="Colored.TButton")
    main_menu_btn.pack(side='left', padx=5)
    booking_btn = ttk.Button(nav_frame, text="Proceed to Booking", style="Colored.TButton")
    booking_btn.pack(side='left', padx=5)
    next_day_btn = ttk.Button(nav_frame, text="Next Day", style="Colored.TButton")
    next_day_btn.pack(side='right', padx=5)
    prev_day_btn = ttk.Button(nav_frame, text="Previous Day", style="Colored.TButton")
    prev_day_btn.pack(side='right', padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
