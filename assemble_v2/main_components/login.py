import tkinter as tk
from tkinter import messagebox
from main_components.services.user_service import UserService
from database.database_settings import SessionLocal

class LoginFrame(tk.Frame):
    def __init__(self, parent, callback=None):
        super().__init__(parent, bg="#b6b8ba")
        self.callback = callback
        self.session = SessionLocal()
        self.user_service = UserService(self.session)
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self, bg="#b6b8ba")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_username = tk.Label(frame, text="Username", font=("Arial", 14), bg="#b6b8ba")
        label_username.grid(row=0, column=0, pady=10, padx=10)

        self.entry_username = tk.Entry(frame, font=("Arial", 14), fg="grey", bg="#7a818c",
                                        insertbackground="black", highlightthickness=0)
        self.entry_username.placeholder = "Enter username"
        self.entry_username.insert(0, self.entry_username.placeholder)
        self.entry_username.bind("<FocusIn>", self.clear_placeholder)
        self.entry_username.bind("<FocusOut>", self.add_placeholder)
        self.entry_username.grid(row=0, column=1, pady=10, padx=20)

        label_password = tk.Label(frame, text="Password", font=("Arial", 14), bg="#b6b8ba")
        label_password.grid(row=1, column=0, pady=10, padx=10)

        self.entry_password = tk.Entry(frame, font=("Arial", 14), fg="grey", bg="#7a818c",
                                        insertbackground="black", highlightthickness=0, show="*")
        self.entry_password.placeholder = "Enter password"
        self.entry_password.insert(0, self.entry_password.placeholder)
        self.entry_password.bind("<FocusIn>", self.clear_placeholder)
        self.entry_password.bind("<FocusOut>", self.add_placeholder)
        self.entry_password.grid(row=1, column=1, pady=10, padx=20)

        button_frame = tk.Frame(frame, bg="#b6b8ba")
        button_frame.grid(row=2, column=1, pady=20, padx=20, sticky="e")

        button_login = tk.Button(button_frame, text="Login", command=self.login,
                                    bd=0, font=("Arial", 14), highlightthickness=1)
        button_login.pack(side=tk.LEFT, padx=10)

        quick_frame = tk.Frame(frame, bg="#b6b8ba")
        quick_frame.grid(row=3, column=0, columnspan=2, pady=10)
        quick_logins = [
            {"username": "admin1", "password": "admin1pass$"},
            {"username": "manager1", "password": "manager1pass$"},
            {"username": "staff1", "password": "staff1pass$"}
        ]
        for user in quick_logins:
            btn = tk.Button(quick_frame, text=f"Quick Login: {user['username']}",
                            command=lambda u=user: self.quick_login(u),
                            bd=0, font=("Arial", 12))
            btn.pack(side=tk.LEFT, padx=5)

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

        if username == self.entry_username.placeholder:
            username = ""
        if password == self.entry_password.placeholder:
            password = ""

        user = self.user_service.get_by_username(username)
        is_authenticated = self.user_service.login(username, password)

        if is_authenticated and user:
            print(f"is_authenticated: {is_authenticated}, user: {user}") 
            if self.callback:
                self.callback(user.role.name if user.role else "Unknown", user)
        else:
            messagebox.showerror("Login", "Invalid Credentials")
        
    def quick_login(self, user_info):
        username = user_info["username"]
        password = user_info["password"]
        user = self.user_service.get_by_username(username)
        is_authenticated = self.user_service.login(username, password)
        if is_authenticated and user:
            if self.callback:
                self.callback(user.role.name if user.role else "Unknown", user)
        else:
            messagebox.showerror("Login", f"Quick login failed for {username}")