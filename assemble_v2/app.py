import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import components
from main_components.login import LoginFrame
from main_components.main_screen import MainScreen

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema Management System")
        
        # Store current user
        self.current_user = None
        
        # Start with maximized window
        self.state('zoomed')
        
        # Set up menu
        self.setup_menu()
        
        # Create a main frame to hold content
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize with the login screen
        self.show_login()
    
    def setup_menu(self):
        """Setup application menu"""
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Toggle Maximize (F11)", command=self.toggle_maximize)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)
        
        # Bind F11 key to toggle maximize/restore
        self.bind("<F11>", lambda event: self.toggle_maximize())
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window size"""
        if self.state() == 'zoomed':
            self.state('normal')
        else:
            self.state('zoomed')
    
    def clear_frame(self):
        """Clear the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        """Show the login screen"""
        self.clear_frame()
        login_frame = LoginFrame(self.main_frame, callback=self.login_successful)
        login_frame.pack(fill=tk.BOTH, expand=True)
    
    def login_successful(self, user_type, user=None):
        """Callback for when login is successful"""
        self.current_user = user
        print(f"Login successful as {user_type}")
        
        # Show main page
        self.show_main_page()
    
    def show_main_page(self):
        """Show the main page after login"""
        self.clear_frame()
        main_screen = MainScreen(self.main_frame, user=self.current_user, callback=self.main_screen_callback)
        main_screen.pack(fill=tk.BOTH, expand=True)

    def main_screen_callback(self, action):
        """Handle callbacks from main screen"""
        if action == "logout":
            self.current_user = None
            self.show_login()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()