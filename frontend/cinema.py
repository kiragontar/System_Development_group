import tkinter as tk
from tkinter import ttk
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO

def main():
    root = tk.Tk()
    root.title("Ticket Booking System")
    
    # Set window to 720p resolution
    root.geometry("1280x720")
    
    # ====== Style Configuration ======
    style = ttk.Style(root)
    style.theme_use("clam")  # You can also try "default" or others

    # Overall background
    bg_color = "#"    # Dark gray
    label_color = "#f2d9fc"  # Light purple
    root.configure(bg=bg_color)

    # Define accent colors
    accent_blue   = "#4b86b3"  # Light blue accent
    accent_green  = "#b8f17e"  # Yellow-green accent

    # Frame and Label background
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=label_color, foreground="black")

    # Increase header font size for a larger display
    style.configure("Header.TLabel",
                    background=accent_blue,
                    foreground="white",
                    font=("Arial", 20, "bold"))

    # Treeview styling with increased font size
    style.configure("Treeview",
                    background="#918789",
                    foreground="black",
                    fieldbackground="#ffffff",
                    font=("Arial", 12))
    style.configure("Treeview.Heading",
                    background=accent_green,
                    foreground="black",
                    font=("Arial", 12, "bold"))
    style.map("Treeview",
              background=[("selected", "#a3d0f8")],
              foreground=[("selected", "black")])

    # Buttons with increased font size
    style.configure("Colored.TButton",
                    background=accent_blue,
                    foreground="white",
                    font=("Arial", 12, "bold"))

    # ====== Main Frame ======
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill='both', expand=True)
    
    # ====== Top Bar (Admin Panel & User Icon) ======
    # Create a top bar frame
    top_bar = ttk.Frame(main_frame)
    top_bar.pack(fill='x')
    
    # --- Admin Panel Button ---
    def open_admin_panel():
        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Panel")
        admin_window.geometry("600x400")
        label = ttk.Label(admin_window, text="Welcome to Admin Panel", font=("Arial", 16))
        label.pack(pady=20)
    
    admin_button = ttk.Button(top_bar, text="Admin Panel", style="Colored.TButton", command=open_admin_panel)
    admin_button.pack(side="left", padx=10, pady=10)
    
    # --- User Icon Button with Toggle Menu ---
    # Load the user icon image from the URL
    try:
        url = "https://static.vecteezy.com/system/resources/previews/007/335/692/non_2x/account-icon-template-vector.jpg"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        # Try to use LANCZOS if available (PIL >= 9.1.0), otherwise fall back to older method
        try:
            im = im.resize((40, 40), Image.Resampling.LANCZOS)
        except AttributeError:
            im = im.resize((40, 40), Image.ANTIALIAS)
        user_icon = ImageTk.PhotoImage(im)
    except Exception as e:
        print("Error loading image:", e)
        user_icon = None

    # Variable to track if the menu is currently visible
    user_menu_visible = False
    # Variable to hold the reference to the user menu pop-up
    user_menu = None

    def close_user_menu():
        nonlocal user_menu, user_menu_visible
        if user_menu is not None:
            user_menu.destroy()
            user_menu = None
            user_menu_visible = False
            # Unbind the click event when menu is closed
            root.unbind("<Button-1>")

    def check_click_outside(event):
        nonlocal user_menu
        if user_menu is not None:
            # Get menu position and dimensions
            menu_x = user_menu.winfo_rootx()
            menu_y = user_menu.winfo_rooty()
            menu_width = user_menu.winfo_width()
            menu_height = user_menu.winfo_height()
            
            # Check if click is outside menu area
            if not (menu_x <= event.x_root <= menu_x + menu_width and 
                    menu_y <= event.y_root <= menu_y + menu_height):
                # Don't close if click is on the user icon button
                icon_x = user_icon_btn.winfo_rootx()
                icon_y = user_icon_btn.winfo_rooty()
                icon_width = user_icon_btn.winfo_width()
                icon_height = user_icon_btn.winfo_height()
                
                if not (icon_x <= event.x_root <= icon_x + icon_width and 
                        icon_y <= event.y_root <= icon_y + icon_height):
                    close_user_menu()

    def toggle_user_menu():
        nonlocal user_menu, user_menu_visible
        
        # If menu is already shown, destroy it
        if user_menu_visible and user_menu is not None:
            close_user_menu()
            return
            
        # Otherwise create and show the menu
        user_menu = tk.Toplevel(root)
        user_menu.overrideredirect(True)  # No window decorations
        
        # Position the menu just below the user icon button
        x = user_icon_btn.winfo_rootx()
        y = user_icon_btn.winfo_rooty() + user_icon_btn.winfo_height()
        user_menu.geometry(f"+{x}+{y}")
        
        # Style the menu
        menu_frame = ttk.Frame(user_menu, style="TFrame")
        menu_frame.pack(fill="both", expand=True)
        
        # Add username label and sign-out button to the menu
        user_name_label = ttk.Label(menu_frame, text="Username: user123", padding=5)
        user_name_label.pack(fill='x')
        
        # Sign-out button that also closes the menu
        def sign_out():
            print("Sign out clicked")
            close_user_menu()
            
        signout_btn = ttk.Button(menu_frame, text="Sign Out", command=sign_out)
        signout_btn.pack(fill='x')
        
        user_menu_visible = True
        
        # Bind click event to detect clicks outside the menu
        # Wait a bit to avoid the current click triggering the event
        root.after(100, lambda: root.bind("<Button-1>", check_click_outside))

    # Create the user icon button with the toggle function
    user_icon_btn = ttk.Button(top_bar, command=toggle_user_menu)
    if user_icon:
        user_icon_btn.config(image=user_icon)
        # Keep a reference to avoid garbage collection
        user_icon_btn.image = user_icon
    else:
        user_icon_btn.config(text="User")
    user_icon_btn.pack(side="right", padx=10, pady=10)
    
    # ====== Header Label ======
    header_label = ttk.Label(
        main_frame,
        text="Linity Cinemas\nBristol \nCurated by James Sunderland | 2025",
        style="Header.TLabel",
        anchor="center"
    )
    header_label.pack(pady=10, anchor="center")

    # ====== Treeview (Table) ======
    columns = ("show_no", "movie", "rating", "showtime", "seats")
    showtimes_tree = ttk.Treeview(
        main_frame,
        columns=columns,
        show='headings',
        height=10
    )
    showtimes_tree.pack(fill='x', expand=True, pady=10)

    # Define column headings
    showtimes_tree.heading("show_no", text="Show #")
    showtimes_tree.heading("movie", text="Movie")
    showtimes_tree.heading("rating", text="IMDb Rating")
    showtimes_tree.heading("showtime", text="Showtime")
    showtimes_tree.heading("seats", text="Seats Available")

    # Set column widths (reduced for a more compact layout)
    showtimes_tree.column("show_no", width=40, anchor="center")
    showtimes_tree.column("movie", width=200)
    showtimes_tree.column("rating", width=70, anchor="center")
    showtimes_tree.column("showtime", width=80, anchor="center")
    showtimes_tree.column("seats", width=90, anchor="center")

    # Insert sample data
    showtimes_tree.insert("", "end", values=("1", "The Shawshank Redemption", "9.3", "10:00", "50"))
    showtimes_tree.insert("", "end", values=("2", "The Shawshank Redemption", "9.3", "14:00", "35"))
    showtimes_tree.insert("", "end", values=("3", "The Shawshank Redemption", "9.3", "18:00", "20"))
    showtimes_tree.insert("", "end", values=("4", "The Shawshank Redemption", "9.3", "19:00", "25"))
    showtimes_tree.insert("", "end", values=("1", "Inception", "8.8", "10:00", "45"))
    showtimes_tree.insert("", "end", values=("2", "Inception", "8.8", "14:00", "50"))
    showtimes_tree.insert("", "end", values=("3", "Inception", "8.8", "18:00", "15"))

    # ====== Info Frame (for movie details) ======
    info_frame = ttk.Frame(main_frame, padding=(0, 0))
    info_frame.pack(fill='x')

    info_label = ttk.Label(
        info_frame,
        text="Select a row to see movie details here...",
        font=("Arial", 12)
    )
    info_label.pack(pady=(5, 50))

    def on_select(event):
        """Display detailed info when a user selects a row."""
        selected_item = showtimes_tree.selection()
        if selected_item:
            values = showtimes_tree.item(selected_item[0])["values"]
            movie_title = values[1] if values else ""

            if movie_title == "The Shawshank Redemption":
                details = (
                    "The Shawshank Redemption\n"
                    "Drama, 1994, 2h 22m\n"
                    "Cast: Tim Robbins, Morgan Freeman, Bob Gunton\n"
                    "Plot: A man wrongfully imprisoned forms an unbreakable bond and hatches a plan for redemption."
                )
            elif movie_title == "Inception":
                details = (
                    "Inception\n"
                    "Sci-Fi, Thriller, 2010, 2h 28m\n"
                    "Cast: Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page\n"
                    "Plot: A skilled thief enters people's dreams to steal secrets, but a new mission challenges his reality."
                )
            else:
                details = "No details available."

            info_label.config(text=details)

    showtimes_tree.bind("<<TreeviewSelect>>", on_select)

    # ====== Navigation Buttons ======
    nav_frame = ttk.Frame(main_frame)
    nav_frame.pack(fill='x', pady=10)

    main_menu_btn = ttk.Button(nav_frame, text="Main Menu", style="Colored.TButton")
    main_menu_btn.pack(side='left', padx=5)

    booking_btn = ttk.Button(nav_frame, text="Proceed to Booking", style="Colored.TButton")
    booking_btn.pack(side='left', padx=5)

    prev_day_btn = ttk.Button(nav_frame, text="Previous Day", style="Colored.TButton")
    prev_day_btn.pack(side='right', padx=5)

    next_day_btn = ttk.Button(nav_frame, text="Next Day", style="Colored.TButton")
    next_day_btn.pack(side='right', padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()