# signup.py - GUI for user sign up
import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base
from backend.user_service import UserService

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
user_service = UserService(session)

def run_signup(parent=None):
    signup_window = tk.Toplevel(parent) if parent else tk.Tk()
    signup_window.title("Sign Up")
    signup_window.geometry("1280x720")
    signup_window.configure(bg="#6e7c91")

    if not parent:
        signup_window.protocol("WM_DELETE_WINDOW", signup_window.destroy)

    frame = tk.Frame(signup_window, bg="#6e7c91")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Username
    label_username = tk.Label(frame, text="Username", font=("Arial", 16), bg="#6e7c91")
    label_username.grid(row=0, column=0, pady=10, padx=10)
    entry_username = tk.Entry(frame, font=("Arial", 16), fg="#aaaebd", bg="#7a818c", highlightthickness=0)
    entry_username.grid(row=0, column=1, pady=10, padx=20)
    entry_username.insert(0, "Enter username")

    # Password
    label_password = tk.Label(frame, text="Password", font=("Arial", 16), bg="#6e7c91")
    label_password.grid(row=1, column=0, pady=10, padx=10)
    entry_password = tk.Entry(frame, font=("Arial", 16), fg="#aaaebd", bg="#7a818c", show="*", highlightthickness=0)
    entry_password.grid(row=1, column=1, pady=10, padx=20)
    entry_password.insert(0, "Enter password")

    # First Name
    label_firstname = tk.Label(frame, text="First Name", font=("Arial", 16), bg="#6e7c91")
    label_firstname.grid(row=2, column=0, pady=10, padx=10)
    entry_firstname = tk.Entry(frame, font=("Arial", 16), fg="#aaaebd", bg="#7a818c", highlightthickness=0)
    entry_firstname.grid(row=2, column=1, pady=10, padx=20)
    entry_firstname.insert(0, "Enter first name")

    # Last Name
    label_lastname = tk.Label(frame, text="Last Name", font=("Arial", 16), bg="#6e7c91")
    label_lastname.grid(row=3, column=0, pady=10, padx=10)
    entry_lastname = tk.Entry(frame, font=("Arial", 16), fg="#aaaebd", bg="#7a818c", highlightthickness=0)
    entry_lastname.grid(row=3, column=1, pady=10, padx=20)
    entry_lastname.insert(0, "Enter last name")

    def clear_placeholder(event):
        if event.widget.get() in ["Enter username", "Enter password", "Enter first name", "Enter last name"]:
            event.widget.delete(0, tk.END)
            event.widget.configure(fg="white")

    def add_placeholder(event):
        if not event.widget.get():
            placeholders = {
                entry_username: "Enter username",
                entry_password: "Enter password",
                entry_firstname: "Enter first name",
                entry_lastname: "Enter last name"
            }
            event.widget.insert(0, placeholders[event.widget])
            event.widget.configure(fg="#aaaebd")

    for widget in (entry_username, entry_password, entry_firstname, entry_lastname):
        widget.bind("<FocusIn>", clear_placeholder)
        widget.bind("<FocusOut>", add_placeholder)

    def create_account():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        firstname = entry_firstname.get().strip()
        lastname = entry_lastname.get().strip()

        if any(field in ["", "Enter username", "Enter password", "Enter first name", "Enter last name"] 
            for field in [username, password, firstname, lastname]):
            messagebox.showerror("Error", "All fields are required")
            return

        new_user, error = user_service.create_user(username, password, firstname, lastname, 2)
        if new_user:
            messagebox.showinfo("Success", "Account created successfully!")
            signup_window.destroy()
            if parent:
                parent.deiconify()
            else:
                import login
                login.run_login()
        else:
            if error == "username_exists":
                messagebox.showerror("Error", "Username already exists")
            elif isinstance(error, list):
                error_msg = "Missing password requirements:\n\n" + "\n".join(error)
                messagebox.showerror("Password Requirements", error_msg)
            else:
                messagebox.showerror("Error", "Account creation failed")

    button_frame = tk.Frame(frame, bg="#6e7c91")
    button_frame.grid(row=4, column=1, pady=20, padx=20, sticky="e")

    button_signup = tk.Button(button_frame, text="Create Account", command=create_account, 
                            bd=0, font=("Arial", 16), highlightthickness=1)
    button_signup.pack(side=tk.LEFT, padx=10)

    def open_login():
        signup_window.destroy()
        if parent:
            parent.deiconify()

    lbl_login = tk.Label(frame, text="Already have an account? Login", fg="#4b86b3",
                     bg="#E6E6E6", font=("Arial", 14), cursor="hand2")

    lbl_login.grid(row=5, columnspan=2, pady=10)
    lbl_login.bind("<Button-1>", lambda e: open_login())

    if not parent:
        signup_window.mainloop()

if __name__ == "__main__":
    run_signup()