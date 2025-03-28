import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import tkinter as tk
from tkinter import messagebox
from main_components.services.user_service import UserService
from main_components.services.role_service import RoleService
from main_components.services.cinema_service import CinemaService
from main_components.services.city_service import CityService
from database.database_settings import SessionLocal

class LoginFrame(tk.Frame):
    def __init__(self, parent, callback=None):
        super().__init__(parent, bg="#b6b8ba")
        self.callback = callback
        
        # Initialize database session
        self.session = SessionLocal()
        
        # Create service instances
        self.role_service = RoleService(self.session)
        self.cinema_service = CinemaService(self.session)
        self.city_service = CityService(self.session)
        self.user_service = UserService(self.session, self.role_service, self.cinema_service)
        
        # Set up the UI
        self.setup_ui()
        
    def setup_ui(self):
        # Create a frame to center the content
        frame = tk.Frame(self, bg="#b6b8ba")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Test buttons for development (can be removed in production)
        test_frame = tk.Frame(self, bg="#b6b8ba")
        test_frame.pack(side=tk.TOP, pady=10)
        
        create_city_button = tk.Button(test_frame, text="Create Test City", command=self.create_test_city)
        create_city_button.pack(side=tk.LEFT, padx=5)
        
        create_cinema_button = tk.Button(test_frame, text="Create Test Cinema", command=self.create_test_cinema)
        create_cinema_button.pack(side=tk.LEFT, padx=5)
        
        create_role_button = tk.Button(test_frame, text="Create Test Role", command=self.create_test_role)
        create_role_button.pack(side=tk.LEFT, padx=5)
        
        create_user_button = tk.Button(test_frame, text="Create Test User", command=self.create_test_user)
        create_user_button.pack(side=tk.LEFT, padx=5)
        
        # Username field
        label_username = tk.Label(frame, text="Username", font=("Arial", 14), bg="#b6b8ba")
        label_username.grid(row=0, column=0, pady=10, padx=10)
        
        self.entry_username = tk.Entry(frame, font=("Arial", 14), fg="grey", bg="#7a818c", 
                                  insertbackground="black", highlightthickness=0)
        self.entry_username.placeholder = "Enter username"
        self.entry_username.insert(0, self.entry_username.placeholder)
        self.entry_username.bind("<FocusIn>", self.clear_placeholder)
        self.entry_username.bind("<FocusOut>", self.add_placeholder)
        self.entry_username.grid(row=0, column=1, pady=10, padx=20)
        
        # Password field
        label_password = tk.Label(frame, text="Password", font=("Arial", 14), bg="#b6b8ba")
        label_password.grid(row=1, column=0, pady=10, padx=10)
        
        self.entry_password = tk.Entry(frame, font=("Arial", 14), fg="grey", bg="#7a818c", 
                                  insertbackground="black", highlightthickness=0, show="*")
        self.entry_password.placeholder = "Enter password"
        self.entry_password.insert(0, self.entry_password.placeholder)
        self.entry_password.bind("<FocusIn>", self.clear_placeholder)
        self.entry_password.bind("<FocusOut>", self.add_placeholder)
        self.entry_password.grid(row=1, column=1, pady=10, padx=20)
        
        # Buttons frame
        button_frame = tk.Frame(frame, bg="#b6b8ba")
        button_frame.grid(row=2, column=1, pady=20, padx=20, sticky="e")
        
        button_login = tk.Button(button_frame, text="Login", command=self.login, 
                            bd=0, font=("Arial", 14), highlightthickness=1)
        button_login.pack(side=tk.LEFT, padx=10)
        
        button_signup = tk.Button(button_frame, text="Sign Up", command=self.signup, 
                             bd=0, font=("Arial", 14), highlightthickness=1)
        button_signup.pack(side=tk.LEFT, padx=10)

    def clear_placeholder(self, event):
        if event.widget.get() == event.widget.placeholder:
            event.widget.delete(0, tk.END)
            event.widget.configure(fg="white")

    def add_placeholder(self, event):
        if not event.widget.get():
            event.widget.insert(0, event.widget.placeholder)
            event.widget.configure(fg="grey")
    
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        # Check for placeholder text
        if username == self.entry_username.placeholder:
            username = ""
        if password == self.entry_password.placeholder:
            password = ""
        
        # First get the user object
        user = self.user_service.get_by_username(username)
        
        # Then authenticate using the service
        is_authenticated = self.user_service.login(username, password)

        if is_authenticated and user:
            messagebox.showinfo("Login", "Login Successful")
            # Pass both the user type and the user object to the callback
            if self.callback:
                self.callback(user.role.name if user.role else "Unknown", user)
        else:
            messagebox.showerror("Login", "Invalid Credentials")

    def signup(self):
        messagebox.showinfo("Sign Up", "Sign Up functionality is not implemented yet")
    
    # Test utility methods
    def create_test_city(self):
        try:
            existing_city = self.city_service.get_city_by_name("Test City")
            if not existing_city:
                test_city = self.city_service.create_city(
                    name="Test City",
                    country="Test Country"
                )
                messagebox.showinfo("City Creation", "Test city created successfully.")
                return test_city.city_id
            else:
                return existing_city.city_id
        except Exception as e:
            messagebox.showerror("City Creation", f"Failed to create test city: {e}")
            return None

    def create_test_cinema(self):
        city_id = self.create_test_city()
        try:
            existing_cinema = self.cinema_service.get_cinema_by_name("Test Cinema")
            if not existing_cinema:
                test_cinema = self.cinema_service.create_cinema(
                    name="Test Cinema",
                    address="123 Test St",
                    city_id=city_id
                )
                messagebox.showinfo("Cinema Creation", "Test cinema created successfully.")
                return test_cinema.cinema_id
            else:
                return existing_cinema.cinema_id
        except Exception as e:
            messagebox.showerror("Cinema Creation", f"Failed to create test cinema: {e}")
            return None
    
    def create_test_role(self):
        try:
            existing_role = self.role_service.get_role_by_name("Test Role")
            if not existing_role:
                test_role = self.role_service.create_role(name="Test Role")
                messagebox.showinfo("Role Creation", "Test role created successfully.")
                return test_role.role_id
            else:
                return existing_role.role_id
        except Exception as e:
            messagebox.showerror("Role Creation", f"Failed to create test role: {e}")
            return None
            
    def create_test_user(self):
        cinema_id = self.create_test_cinema()
        role_id = self.create_test_role()
        try:
            test_user = self.user_service.create_user(
                username="testuser",
                password="testpassword1$",
                firstname="test",
                lastname="testlast",
                role_id=role_id,
                cinema_id=cinema_id
            )
            messagebox.showinfo("User Creation", "Test user created successfully.")
        except Exception as e:
            messagebox.showerror("User Creation", f"Failed to create test user: {e}")

# Only runs when login.py is executed directly
if __name__ == "__main__":
    root = tk.Tk()
    login = LoginFrame(root)
    root.mainloop()
