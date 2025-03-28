import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from database.database_settings import SessionLocal
from main_components.services.cinema_service import CinemaService
from main_components.services.user_service import UserService
from main_components.services.role_service import RoleService
from main_components.services.film_service import CinemaFilmService  # Correct import

class MainScreen(tk.Frame):
    def __init__(self, parent, user=None, callback=None):
        super().__init__(parent, bg="#e0e0e0")
        self.parent = parent
        self.user = user
        self.callback = callback
        
        # Initialize database session
        self.session = SessionLocal()
        
        # Create service instances
        self.cinema_service = CinemaService(self.session)
        self.role_service = RoleService(self.session)
        self.user_service = UserService(self.session, self.role_service, self.cinema_service)
        
        # Get cinema information if user has assigned cinema
        self.cinema = None
        self.cinema_films = []
        self.film_service = None
        
        if user and user.cinema_id:
            self.cinema = self.cinema_service.get_cinema_by_id(user.cinema_id)
            # Initialize film service with cinema
            if self.cinema:
                self.film_service = CinemaFilmService(self.cinema, self.session)
                # Get films for this cinema
                self.cinema_films = self.film_service.get_all_films()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        container = tk.Frame(self, bg="#e0e0e0", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = tk.Frame(container, bg="#4a6984", padx=15, pady=15)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # User information
        user_name = f"{self.user.firstname} {self.user.lastname}" if self.user else "Guest"
        role_name = self.user.role.name if self.user and self.user.role else "No Role"
        
        user_info_label = tk.Label(
            header_frame, 
            text=f"Welcome, {user_name} | Role: {role_name}",
            font=("Arial", 14, "bold"),
            bg="#4a6984",
            fg="white"
        )
        user_info_label.pack(side=tk.LEFT)
        
        # Logout button
        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            command=self.logout,
            bg="#e74c3c",
            fg="white",
            padx=10
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Content area with two frames side by side
        content_frame = tk.Frame(container, bg="#e0e0e0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left navigation panel (different for each role)
        nav_frame = tk.Frame(content_frame, bg="#f0f0f0", width=200, padx=10, pady=10)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        nav_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        nav_label = tk.Label(
            nav_frame,
            text="Navigation",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        )
        nav_label.pack(anchor="w", pady=(0, 10))
        
        # Add navigation buttons based on user role
        self.create_role_specific_navigation(nav_frame)
        
        # Right content area with tabs for different sections
        right_frame = tk.Frame(content_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create notebook (tabbed interface)
        tab_control = ttk.Notebook(right_frame)
        
        # Cinema Info Tab
        cinema_tab = tk.Frame(tab_control, bg="white", padx=15, pady=15)
        tab_control.add(cinema_tab, text="Cinema Info")
        
        # Films Tab
        films_tab = tk.Frame(tab_control, bg="white", padx=15, pady=15)
        tab_control.add(films_tab, text="Films")
        
        tab_control.pack(expand=1, fill="both")
        
        # ---- Cinema Information Tab ----
        cinema_header = tk.Label(
            cinema_tab,
            text="Cinema Information",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        cinema_header.pack(anchor="w", pady=(0, 15))
        
        if self.cinema:
            # Create table-like display for cinema info
            info_table = ttk.Treeview(
                cinema_tab, 
                columns=("property", "value"),
                show="headings",
                height=6
            )
            info_table.heading("property", text="Property")
            info_table.heading("value", text="Value")
            
            info_table.column("property", width=150)
            info_table.column("value", width=300)
            
            # Add cinema properties
            info_table.insert("", "end", values=("Cinema ID", self.cinema.cinema_id))
            info_table.insert("", "end", values=("Name", self.cinema.name))
            info_table.insert("", "end", values=("Address", self.cinema.address))
            
            # Get number of screens
            screens = self.cinema_service.get_screens(self.cinema.cinema_id)
            info_table.insert("", "end", values=("Number of Screens", len(screens) if screens else 0))
            
            # Get staff count
            staff = self.cinema_service.get_staff(self.cinema.cinema_id)
            info_table.insert("", "end", values=("Staff Members", len(staff) if staff else 0))
            
            # Number of films
            info_table.insert("", "end", values=("Number of Films", len(self.cinema_films) if self.cinema_films else 0))
            
            info_table.pack(fill=tk.X, pady=10)
            
            # Add action buttons below the table
            action_frame = tk.Frame(cinema_tab, bg="white")
            action_frame.pack(fill=tk.X, pady=10)
            
            view_screenings_btn = tk.Button(
                action_frame,
                text="View Screenings",
                bg="#3498db",
                fg="white",
                command=self.view_screenings
            )
            view_screenings_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            view_staff_btn = tk.Button(
                action_frame,
                text="View Staff",
                bg="#3498db",
                fg="white",
                command=self.view_staff
            )
            view_staff_btn.pack(side=tk.LEFT)
        else:
            no_cinema_label = tk.Label(
                cinema_tab,
                text="No cinema assigned to this user.",
                font=("Arial", 12),
                bg="white",
                fg="#e74c3c"
            )
            no_cinema_label.pack(pady=20)
        
        # ---- Films Tab ----
        films_header = tk.Label(
            films_tab,
            text="Films Available in This Cinema",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        films_header.pack(anchor="w", pady=(0, 15))
        
        if self.cinema and self.cinema_films:
            # Create table for films
            film_columns = ("id", "name", "director", "runtime", "genre", "release_date", "rating")
            films_table = ttk.Treeview(
                films_tab,
                columns=film_columns,
                show="headings",
                height=10
            )
            
            # Configure columns
            films_table.heading("id", text="ID")
            films_table.heading("name", text="Title")
            films_table.heading("director", text="Director")
            films_table.heading("runtime", text="Duration (min)")
            films_table.heading("genre", text="Genre")
            films_table.heading("release_date", text="Release Date")
            films_table.heading("rating", text="Rating")
            
            films_table.column("id", width=50)
            films_table.column("name", width=200)
            films_table.column("director", width=150)
            films_table.column("runtime", width=100)
            films_table.column("genre", width=100)
            films_table.column("release_date", width=100)
            films_table.column("rating", width=70)
            
            # Add scrollbar
            film_scroll = ttk.Scrollbar(films_tab, orient="vertical", command=films_table.yview)
            films_table.configure(yscrollcommand=film_scroll.set)
            
            # Pack table and scrollbar
            films_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            film_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate films table
            for film in self.cinema_films:
                try:
                    # Handle potential differences in film object structure
                    genre_display = film.genre if isinstance(film.genre, str) else ', '.join(film.genre)
                    release_date = film.release_date.strftime('%Y-%m-%d') if hasattr(film, 'release_date') else ''
                    
                    films_table.insert("", "end", values=(
                        film.film_id,
                        film.name,
                        getattr(film, 'director', 'N/A'),
                        film.runtime,
                        genre_display,
                        release_date,
                        getattr(film, 'critic_rating', 'N/A')
                    ))
                except Exception as e:
                    print(f"Error adding film to table: {e}")
            
            # Button frame below table
            film_action_frame = tk.Frame(films_tab, bg="white", pady=10)
            film_action_frame.pack(fill=tk.X)
            
            add_film_btn = tk.Button(
                film_action_frame,
                text="Add Film to Cinema",
                bg="#3498db",
                fg="white",
                command=self.add_film_to_cinema
            )
            
            # Only show add film button for admin/manager
            if self.user and self.user.role and self.user.role.name.lower() in ["admin", "manager"]:
                add_film_btn.pack(side=tk.LEFT, padx=5)
                
            view_film_details_btn = tk.Button(
                film_action_frame,
                text="View Film Details",
                bg="#3498db",
                fg="white",
                command=self.view_film_details
            )
            view_film_details_btn.pack(side=tk.LEFT, padx=5)
            
            # Double-click to view details
            films_table.bind("<Double-1>", self.on_film_double_click)
            
            # Store reference to the table
            self.films_table = films_table
            
        else:
            no_films_label = tk.Label(
                films_tab,
                text="No films available for this cinema.",
                font=("Arial", 12),
                bg="white",
                fg="#e74c3c"
            )
            no_films_label.pack(pady=20)
            
            # Only show add film button for admin/manager
            if self.cinema and self.user and self.user.role and self.user.role.name.lower() in ["admin", "manager"]:
                add_film_btn = tk.Button(
                    films_tab,
                    text="Add Film to Cinema",
                    bg="#3498db",
                    fg="white",
                    command=self.add_film_to_cinema
                )
                add_film_btn.pack(pady=10)
    
    def create_role_specific_navigation(self, parent_frame):
        """Create navigation buttons based on user role"""
        if not self.user or not self.user.role:
            return
        
        role_name = self.user.role.name.lower()
        
        # Common options for all roles
        btn_view_screenings = tk.Button(
            parent_frame,
            text="View Screenings",
            width=20,
            bg="#3498db",
            fg="white",
            command=self.view_screenings
        )
        btn_view_screenings.pack(anchor="w", pady=5)
        
        # Add Films button for all roles
        btn_view_films = tk.Button(
            parent_frame,
            text="View Films",
            width=20,
            bg="#3498db",
            fg="white",
            command=lambda: self.show_films_tab()
        )
        btn_view_films.pack(anchor="w", pady=5)
        
        # Admin role gets all options
        if role_name == "admin":
            btn_manage_users = tk.Button(
                parent_frame,
                text="Manage Users",
                width=20,
                bg="#3498db",
                fg="white",
                command=self.manage_users
            )
            btn_manage_users.pack(anchor="w", pady=5)
            
            btn_manage_cinemas = tk.Button(
                parent_frame,
                text="Manage Cinemas",
                width=20,
                bg="#3498db",
                fg="white",
                command=self.manage_cinemas
            )
            btn_manage_cinemas.pack(anchor="w", pady=5)
            
            btn_manage_films = tk.Button(
                parent_frame,
                text="Manage Films",
                width=20,
                bg="#3498db",
                fg="white",
                command=self.manage_films
            )
            btn_manage_films.pack(anchor="w", pady=5)
            
        # Manager gets cinema management options
        if role_name in ["admin", "manager"]:
            btn_manage_staff = tk.Button(
                parent_frame,
                text="Manage Staff",
                width=20,
                bg="#3498db",
                fg="white",
                command=self.manage_staff
            )
            btn_manage_staff.pack(anchor="w", pady=5)
            
            btn_add_screenings = tk.Button(
                parent_frame,
                text="Add Screenings",
                width=20,
                bg="#3498db",
                fg="white",
                command=self.add_screenings
            )
            btn_add_screenings.pack(anchor="w", pady=5)
            
        # Staff gets ticket management options
        if role_name in ["admin", "manager", "staff"]:
            btn_sell_tickets = tk.Button(
                parent_frame,
                text="Sell Tickets",
                width=20,
                bg="#3498db",
                fg="white",
                command=self.sell_tickets
            )
            btn_sell_tickets.pack(anchor="w", pady=5)
            
            btn_view_bookings = tk.Button(
                parent_frame,
                text="View Bookings",
                width=20,
                bg="#3498db",
                fg="white",
                command=self.view_bookings
            )
            btn_view_bookings.pack(anchor="w", pady=5)
    
    # Action methods
    def logout(self):
        """Log out the current user"""
        if self.callback:
            self.callback("logout")
    
    def show_films_tab(self):
        """Switch to the films tab"""
        # Find the notebook widget
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Notebook):
                                # Found the notebook, select the Films tab (index 1)
                                grandchild.select(1)
                                return
    
    def on_film_double_click(self, event):
        """Handle double-click on a film"""
        self.view_film_details()
    
    def view_film_details(self):
        """Show details for the selected film"""
        if not hasattr(self, 'films_table'):
            messagebox.showinfo("Error", "No films table available")
            return
            
        try:
            selected_item = self.films_table.selection()[0]
            film_id = self.films_table.item(selected_item)['values'][0]
            
            if self.film_service:
                film = self.film_service.get_all_films_by_id(film_id)
                if film:
                    # Format cast list if it's stored as a string
                    cast_display = film.cast
                    if isinstance(cast_display, str):
                        cast_display = cast_display.replace(',', ', ')
                    elif isinstance(cast_display, list):
                        cast_display = ', '.join(cast_display)
                    
                    # Format genre list if it's stored as a string
                    genre_display = film.genre
                    if isinstance(genre_display, str):
                        genre_display = genre_display.replace(',', ', ')
                    elif isinstance(genre_display, list):
                        genre_display = ', '.join(genre_display)
                    
                    details = f"Title: {film.name}\n"
                    if hasattr(film, 'director'):
                        details += f"Director: {film.director}\n"
                    details += f"Duration: {film.runtime} minutes\n"
                    details += f"Genre: {genre_display}\n"
                    details += f"Cast: {cast_display}\n"
                    if hasattr(film, 'release_date'):
                        details += f"Release Date: {film.release_date.strftime('%Y-%m-%d')}\n"
                    details += f"Age Rating: {film.age_rating}\n"
                    details += f"Critic Rating: {film.critic_rating}\n"
                    details += f"Description: {film.description}\n"
                    
                    messagebox.showinfo(f"Film Details - {film.name}", details)
                else:
                    messagebox.showinfo("Error", f"Film with ID {film_id} not found")
            else:
                messagebox.showinfo("Error", "Film service not available")
        except IndexError:
            messagebox.showinfo("Selection Error", "Please select a film first")
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {str(e)}")
    
    def add_film_to_cinema(self):
        """Add a film to this cinema"""
        messagebox.showinfo("Add Film", "This feature is not implemented yet.")
    
    def view_screenings(self):
        """View screenings for this cinema"""
        messagebox.showinfo("View Screenings", "This feature is not implemented yet.")
    
    def view_staff(self):
        """View staff for this cinema"""
        messagebox.showinfo("View Staff", "This feature is not implemented yet.")
    
    def manage_users(self):
        """Manage users (Admin function)"""
        messagebox.showinfo("Manage Users", "This feature is not implemented yet.")
    
    def manage_cinemas(self):
        """Manage cinemas (Admin function)"""
        messagebox.showinfo("Manage Cinemas", "This feature is not implemented yet.")
    
    def manage_films(self):
        """Manage films (Admin function)"""
        messagebox.showinfo("Manage Films", "This feature is not implemented yet.")
    
    def manage_staff(self):
        """Manage staff (Manager function)"""
        messagebox.showinfo("Manage Staff", "This feature is not implemented yet.")
    
    def add_screenings(self):
        """Add screenings (Manager function)"""
        messagebox.showinfo("Add Screenings", "This feature is not implemented yet.")
    
    def sell_tickets(self):
        """Sell tickets (Staff function)"""
        messagebox.showinfo("Sell Tickets", "This feature is not implemented yet.")
    
    def view_bookings(self):
        """View bookings (Staff function)"""
        messagebox.showinfo("View Bookings", "This feature is not implemented yet.")