import tkinter as tk

class MainScreen(tk.Frame):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent, bg="#e0e0e0")
        self.user = user  # Save the logged-in user
        self.callback = callback
        self.show_hello()  # Changed: show hello text instead of login UI

    def show_hello(self):
        # Display a simple "HELLO" message and a Log Off button
        frame = tk.Frame(self, bg="#e0e0e0", padx=20, pady=20)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text="HELLO", font=("Arial", 24), bg="#e0e0e0").pack(pady=20)
        logoff_btn = tk.Button(frame, text="Log Off", font=("Arial", 14), command=self.log_off)
        logoff_btn.pack(pady=10)

    def log_off(self):
        if self.callback:
            self.callback("logout")