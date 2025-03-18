import tkinter as tk
from tkinter import messagebox

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Check if the username and password are correct
    if username == "admin" and password == "password":
        messagebox.showinfo("Login", "Login Successful")
    else:
        messagebox.showerror("Login", "Invalid Credentials")

# Function to handle signup (not implemented)
def signup():
    messagebox.showinfo("Sign Up", "Sign Up functionality is not implemented yet")

# Function to clear placeholder text when user focuses on the field
def clear_placeholder(event):
    if event.widget.get() == event.widget.placeholder:
        event.widget.delete(0, tk.END)
        event.widget.configure(fg="white")

# Function to add placeholder text if the field is empty
def add_placeholder(event):
    if not event.widget.get():
        event.widget.insert(0, event.widget.placeholder)
        event.widget.configure(fg="grey")

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("1280x720")
root.configure(bg="#b6b8ba")

# Create a frame to center the content
frame = tk.Frame(root, bg="#b6b8ba")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create username label and entry field
label_username = tk.Label(frame, text="Username", font=("Arial", 14), bg="#b6b8ba")
label_username.grid(row=0, column=0, pady=10, padx=10)
entry_username = tk.Entry(frame, font=("Arial", 14), fg="grey", bg="#7a818c", insertbackground="black", highlightthickness=0)
entry_username.placeholder = "Enter username"
entry_username.insert(0, entry_username.placeholder)
entry_username.bind("<FocusIn>", clear_placeholder)
entry_username.bind("<FocusOut>", add_placeholder)
entry_username.grid(row=0, column=1, pady=10, padx=20)

# Create password label and entry field
label_password = tk.Label(frame, text="Password", font=("Arial", 14), bg="#b6b8ba")
label_password.grid(row=1, column=0, pady=10, padx=10)
entry_password = tk.Entry(frame, font=("Arial", 14), fg="grey", bg="#7a818c", insertbackground="black", highlightthickness=0)
entry_password.placeholder = "Enter password"
entry_password.insert(0, entry_password.placeholder)
entry_password.bind("<FocusIn>", clear_placeholder)
entry_password.bind("<FocusOut>", add_placeholder)
entry_password.grid(row=1, column=1, pady=10, padx=20)

# Create a frame for buttons and align them to the right
button_frame = tk.Frame(frame, bg="#b6b8ba")
button_frame.grid(row=2, column=1, pady=20, padx=20, sticky="e")

# Create and place the login button
button_login = tk.Button(button_frame, text="Login", command=login, bd=0, font=("Arial", 14), highlightthickness=1)
button_login.pack(side=tk.LEFT, padx=10)

# Create and place the sign up button
button_signup = tk.Button(button_frame, text="Sign Up", command=signup, bd=0, font=("Arial", 14), highlightthickness=1)
button_signup.pack(side=tk.LEFT, padx=10)

# Start the Tkinter event loop
root.mainloop()
