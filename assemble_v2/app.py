import tkinter as tk
from tkinter import ttk
from main_components.login import LoginFrame
from main_components.main_screen import MainScreen
from main_components.manager_panel import ManagerPanel
from main_components.admin_panel import AdminPanel
from main_components.booking_staff_panel import BookingStaffPanel


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema Management System")
        self.current_user = None
        self.state('zoomed')
        self.setup_menu()

        # Add the style configuration:
        style = ttk.Style()
        style.configure("Selected.TButton", background="gray", foreground="black") #Selected style
        style.configure("Available.TButton", background="green", foreground="black") #Available style
        style.configure("Unavailable.TButton", background="red", foreground="black") #unavailable style.

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.show_login()

    def setup_menu(self):
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Toggle Maximize (F11)", command=self.toggle_maximize)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)
        self.bind("<F11>", lambda event: self.toggle_maximize())

    def toggle_maximize(self):
        if self.state() == 'zoomed':
            self.state('normal')
        else:
            self.state('zoomed')

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_frame()
        login_frame = LoginFrame(self.main_frame, callback=self.login_successful)
        login_frame.pack(fill=tk.BOTH, expand=True)

    def login_successful(self, user_type, user=None):
        self.current_user = user
        if user_type == "Manager": 
            self.show_manager_panel()
        elif user_type == "Admin":
            self.show_admin_panel()
        elif user_type == "Staff":
            self.show_staff_panel()
        else:
            self.show_main_page()

    def show_admin_panel(self):
        self.clear_frame()
        admin_panel = AdminPanel(self.main_frame, user=self.current_user, callback=self.admin_panel_callback)
        admin_panel.pack(fill=tk.BOTH, expand=True)

    def admin_panel_callback(self, action):
        if action == "logout":
            self.current_user = None
            self.show_login()

    def show_manager_panel(self):
        self.clear_frame()
        manager_panel = ManagerPanel(self.main_frame, user=self.current_user, callback=self.manager_panel_callback)  # Corrected callback
        manager_panel.pack(fill=tk.BOTH, expand=True)

    def manager_panel_callback(self, action):  # New callback for ManagerPanel
        if action == "logout":
            self.current_user = None
            self.show_login()

    def show_staff_panel(self):
        self.clear_frame()
        staff_panel = BookingStaffPanel(self.main_frame, user=self.current_user, callback=self.staff_panel_callback)
        staff_panel.pack(fill=tk.BOTH, expand=True)

    def staff_panel_callback(self, action):
        if action == "logout":
            self.current_user = None
            self.show_login()

    def show_main_page(self):
        self.clear_frame()
        main_screen = MainScreen(self.main_frame, user=self.current_user, callback=self.main_screen_callback)
        main_screen.pack(fill=tk.BOTH, expand=True)

    def main_screen_callback(self, action):
        if action == "logout":
            self.current_user = None
            self.show_login()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()