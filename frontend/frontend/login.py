import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.role_service import RoleService
from backend.models import Base
from backend.user_service import UserService

# Database setup
DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

role_service = RoleService(session) 
user_service = UserService(session)

def run_login(parent=None):
    login_window = tk.Toplevel(parent) if parent else tk.Tk()
    login_window.title("Login Page")
    login_window.geometry("1280x720")
    login_window.configure(bg="#6e7c91")

    # Hidden root window for standalone mode
    if not parent:
        login_window.protocol("WM_DELETE_WINDOW", login_window.destroy)

    frame = tk.Frame(login_window, bg="#6e7c91")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Username
    label_username = tk.Label(frame, text="Username", font=("Arial", 16), bg="#6e7c91")
    label_username.grid(row=0, column=0, pady=10, padx=10)
    entry_username = tk.Entry(frame, font=("Arial", 16), fg="#aaaebd", bg="#7a818c", highlightthickness=0)
    entry_username.insert(0, "Enter username")
    entry_username.grid(row=0, column=1, pady=10, padx=20)

    # Password
    label_password = tk.Label(frame, text="Password", font=("Arial", 16), bg="#6e7c91")
    label_password.grid(row=1, column=0, pady=10, padx=10)
    entry_password = tk.Entry(frame, font=("Arial", 16), fg="#aaaebd", bg="#7a818c", show="*", highlightthickness=0)
    entry_password.insert(0, "Enter password")
    entry_password.grid(row=1, column=1, pady=10, padx=20)

    def clear_placeholder(event):
        if event.widget.get() in ["Enter username", "Enter password"]:
            event.widget.delete(0, tk.END)
            event.widget.configure(fg="white")

    def add_placeholder(event):
        if not event.widget.get():
            placeholders = {
                entry_username: "Enter username",
                entry_password: "Enter password"
            }
            event.widget.insert(0, placeholders[event.widget])
            event.widget.configure(fg="#aaaebd")

    entry_username.bind("<FocusIn>", clear_placeholder)
    entry_username.bind("<FocusOut>", add_placeholder)
    entry_password.bind("<FocusIn>", clear_placeholder)
    entry_password.bind("<FocusOut>", add_placeholder)

    def login():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        
        if username in ["", "Enter username"] or password in ["", "Enter password"]:
            messagebox.showerror("Login", "Please enter credentials")
            return

        user, error = user_service.login(username, password)
        if user:
            messagebox.showinfo("Login", f"Welcome {user.firstname}!")
            login_window.destroy()
            from cinema import main
            main(user=user)
        else:
            if error == "username":
                messagebox.showerror("Login", "Username not found")
            elif error == "password":
                messagebox.showerror("Login", "Invalid password")

    def open_signup():
        login_window.withdraw()
        import signup
        signup.run_signup(login_window)

    button_frame = tk.Frame(frame, bg="#6e7c91")
    button_frame.grid(row=2, column=1, pady=20, padx=20, sticky="e")

    button_login = tk.Button(button_frame, text="Login", command=login, 
                           bd=0, font=("Arial", 16), highlightthickness=1)
    button_login.pack(side=tk.LEFT, padx=10)

    button_signup = tk.Button(button_frame, text="Sign Up", command=open_signup,
                            bd=0, font=("Arial", 16), highlightthickness=1)
    button_signup.pack(side=tk.LEFT, padx=10)

    if not parent:
        login_window.mainloop()

if __name__ == "__main__":
    run_login()
