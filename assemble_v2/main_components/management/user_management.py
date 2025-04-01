import tkinter as tk
from tkinter import ttk, messagebox
from database.database_settings import SessionLocal
from main_components.services.user_service import UserService
from main_components.services.role_service import RoleService
from main_components.services.cinema_service import CinemaService

class UserManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, cinema_id, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.cinema_id = cinema_id
        self.session = SessionLocal()
        self.user_service = UserService(self.session)
        self.role_service = RoleService(self.session)
        self.cinema_service = CinemaService(self.session)
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("LightGreen.TFrame", background="lightgreen")
        style.configure("LightYellow.TFrame", background="lightyellow")
        style.configure("LightBlue.TFrame", background="lightblue")

        main_frame = ttk.Frame(self, padding="20", style="LightGreen.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tk.Label(main_frame, text="User Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        self.user_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.user_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_users()

    def manage_users(self):
        self.clear_user_frame()
        self.user_list = ttk.Treeview(
            self.user_frame,
            columns=("ID", "Username", "First Name", "Last Name", "Role", "Cinema"),
            show="headings",
        )
        self.user_list.heading("ID", text="ID")
        self.user_list.heading("Username", text="Username")
        self.user_list.heading("First Name", text="First Name")
        self.user_list.heading("Last Name", text="Last Name")
        self.user_list.heading("Role", text="Role")
        self.user_list.heading("Cinema", text="Cinema")
        self.user_list.pack(expand=True, fill="both")

        if self.cinema_id == "all":
            users = self.user_service.get_all()
        else:
            users = self.user_service.get_all_at_cinema(self.cinema_id)

        for user in users:
            role = self.role_service.get_role_by_id(user.role_id)
            role_name = role.name if role else "N/A" #Handles null values
            self.user_list.insert("", tk.END, values=(user.user_id, user.username, user.firstname, user.lastname, role_name, user.cinema_id))

        action_frame = ttk.Frame(self.user_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add User", command=self.add_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update User", command=self.update_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Remove User", command=self.remove_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse User", command=self.browse_user).pack(side=tk.LEFT, padx=5)

        self.user_list.bind("<ButtonRelease-1>", self.select_user)
        self.selected_user_id = None
        self.user_frame.update()

    
    def select_user(self, event):
        selection = self.user_list.selection()
        if selection:
            item = selection[0]
            self.selected_user_id = self.user_list.item(item, "values")[0]
        else:
            self.selected_user_id = None

    def is_valid_username(self, username):
        return isinstance(username, str) and username.strip() != ""
    
    def is_valid_password(self, password):
        return self.user_service.validate_password_requirements(password) is True

    def is_valid_name(self, name):
        return isinstance(name, str) and name.strip() != ""
    
    def is_valid_role_id(self, role_id):
        try:
            role_id = int(role_id)
            role = self.role_service.get_role_by_id(role_id)
            return role is not None
        except ValueError:
            return False
        
    def is_valid_cinema_id(self, cinema_id):
        try:
            cinema_id = int(cinema_id)
            cinema = self.cinema_service.get_cinema_by_id(cinema_id)
            return cinema is not None
        except ValueError:
            return False
        
    def add_user(self):
        if UserManagement.add_window_open:
            messagebox.showerror("Error", "Add User window is already open.")
            return

        UserManagement.add_window_open = True

        add_frame = ttk.Frame(self.user_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Username:").grid(row=0, column=0)
        self.username_entry = ttk.Entry(add_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(add_frame, text="Password:").grid(row=1, column=0)
        self.password_entry = ttk.Entry(add_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Label(add_frame, text="First Name:").grid(row=2, column=0)
        self.firstname_entry = ttk.Entry(add_frame)
        self.firstname_entry.grid(row=2, column=1)

        tk.Label(add_frame, text="Last Name:").grid(row=3, column=0)
        self.lastname_entry = ttk.Entry(add_frame)
        self.lastname_entry.grid(row=3, column=1)

        tk.Label(add_frame, text="Role ID:").grid(row=4, column=0)
        self.role_id_entry = ttk.Entry(add_frame)
        self.role_id_entry.grid(row=4, column=1)

        tk.Label(add_frame, text="Cinema ID:").grid(row=5, column=0)
        self.cinema_id_entry = ttk.Entry(add_frame)
        self.cinema_id_entry.grid(row=5, column=1)

        def add_user_confirm():
            username = self.username_entry.get()
            password = self.password_entry.get()
            firstname = self.firstname_entry.get()
            lastname = self.lastname_entry.get()
            role_id = self.role_id_entry.get()
            cinema_id = self.cinema_id_entry.get()

            if not self.is_valid_username(username):
                messagebox.showerror("Error", "Invalid Username.")
                return
            if not self.is_valid_password(password):
                messagebox.showerror("Error", "Invalid Password, Password must be at least 8 characters long, with a digit and a special character.")
            if not self.is_valid_name(firstname):
                messagebox.showerror("Error", "Invalid First Name.")
                return
            if not self.is_valid_name(lastname):
                messagebox.showerror("Error", "Invalid Last Name.")
                return
            if not self.is_valid_role_id(role_id):
                messagebox.showerror("Error", "Invalid Role ID.")
                return
            if not self.is_valid_cinema_id(cinema_id):
                messagebox.showerror("Error", "Invalid Cinema ID.")
                return

            try:
                role_id = int(role_id)
                cinema_id = int(cinema_id)
                self.user_service.create_user(username, password, firstname, lastname, role_id, cinema_id)
                UserManagement.add_window_open = False
                self.manage_users()
                add_frame.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        def cancel_add():
            UserManagement.add_window_open = False
            add_frame.destroy()

        ttk.Button(add_frame, text="Confirm Add", command=add_user_confirm).grid(row=6, column=0, pady=5, padx=(0, 5))
        ttk.Button(add_frame, text="Cancel", command=cancel_add).grid(row=6, column=1, pady=5, padx=(5, 0))


    def update_user(self):
        if UserManagement.update_window_open:
            messagebox.showerror("Error", "Update User window is already open.")
            return

        UserManagement.update_window_open = True

        if self.selected_user_id:
            update_frame = ttk.Frame(self.user_frame)
            update_frame.pack(pady=10)

            user = self.user_service.get_by_user_id(self.selected_user_id)

            tk.Label(update_frame, text="Username:").grid(row=0, column=0)
            self.username_entry = ttk.Entry(update_frame)
            self.username_entry.insert(0, user.username)
            self.username_entry.grid(row=0, column=1)

            tk.Label(update_frame, text="First Name:").grid(row=1, column=0)
            self.firstname_entry = ttk.Entry(update_frame)
            self.firstname_entry.insert(0, user.firstname)
            self.firstname_entry.grid(row=1, column=1)

            tk.Label(update_frame, text="Last Name:").grid(row=2, column=0)
            self.lastname_entry = ttk.Entry(update_frame)
            self.lastname_entry.insert(0, user.lastname)
            self.lastname_entry.grid(row=2, column=1)

            tk.Label(update_frame, text="Role ID:").grid(row=3, column=0)
            self.role_id_entry = ttk.Entry(update_frame)
            self.role_id_entry.insert(0, user.role_id)
            self.role_id_entry.grid(row=3, column=1)

            tk.Label(update_frame, text="Cinema ID:").grid(row=4, column=0)
            self.cinema_id_entry = ttk.Entry(update_frame)
            self.cinema_id_entry.insert(0, user.cinema_id)
            self.cinema_id_entry.grid(row=4, column=1)

            def update_user_confirm():
                username_str = self.username_entry.get()
                firstname_str = self.firstname_entry.get()
                lastname_str = self.lastname_entry.get()
                role_id_str = self.role_id_entry.get()
                cinema_id_str = self.cinema_id_entry.get()

                username = None
                firstname = None
                lastname = None
                role_id = None
                cinema_id = None

                if username_str:
                    if not self.is_valid_username(username_str):
                        messagebox.showerror("Error", "Invalid Username.")
                        return
                    username = username_str

                if firstname_str:
                    if not self.is_valid_name(firstname_str):
                        messagebox.showerror("Error", "Invalid First Name.")
                        return
                    firstname = firstname_str

                if lastname_str:
                    if not self.is_valid_name(lastname_str):
                        messagebox.showerror("Error", "Invalid Last Name.")
                        return
                    lastname = lastname_str

                if role_id_str:
                    if not self.is_valid_role_id(role_id_str):
                        messagebox.showerror("Error", "Invalid Role ID.")
                        return
                    role_id = int(role_id_str)

                if cinema_id_str:
                    if not self.is_valid_cinema_id(cinema_id_str):
                        messagebox.showerror("Error", "Invalid Cinema ID.")
                        return
                    cinema_id = int(cinema_id_str)

                try:
                    role_id = int(role_id)
                    cinema_id = int(cinema_id)
                    self.user_service.update_user(self.selected_user_id, username, firstname, lastname, role_id, cinema_id)
                    UserManagement.update_window_open = False
                    self.manage_users()
                    update_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                except Exception as e:
                    messagebox.showerror("Error", f"An unexpected error occurred: {e}")

            def cancel_update():
                UserManagement.update_window_open = False
                update_frame.destroy()

            ttk.Button(update_frame, text="Confirm Update", command=update_user_confirm).grid(row=5, column=0, pady=5, padx=(0, 5))
            ttk.Button(update_frame, text="Cancel", command=cancel_update).grid(row=5, column=1, pady=5, padx=(5, 0))

        else:
            messagebox.showerror("Error", "Select a user to update.")
            UserManagement.update_window_open = False


    def remove_user(self):
        if self.selected_user_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
                self.user_service.delete_user(self.selected_user_id)
                self.manage_users()
        else:
            messagebox.showerror("Error", "Select a user to remove.")

    
    def browse_user(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse User")

        tk.Label(browse_window, text="User ID (Optional):").grid(row=0, column=0)
        user_id_entry = ttk.Entry(browse_window)
        user_id_entry.grid(row=0, column=1)

        username_label = tk.Label(browse_window, text="Username:")
        username_entry = ttk.Entry(browse_window)

        def find_user():
            user_id = user_id_entry.get()
            username = username_entry.get()
            found = False

            if user_id:
                for item in self.user_list.get_children():
                    values = self.user_list.item(item, 'values')
                    if values and len(values) > 0 and str(values[0]) == user_id:
                        self.user_list.see(item)
                        self.user_list.selection_set(item)
                        self.user_list.focus(item)
                        self.selected_user_id = user_id
                        browse_window.destroy()
                        found = True
                        return
            elif username:
                for item in self.user_list.get_children():
                    values = self.user_list.item(item, 'values')
                    if values and len(values) > 1 and values[1] == username:
                        self.user_list.see(item)
                        self.user_list.selection_set(item)
                        self.user_list.focus(item)
                        self.selected_user_id = values[0]
                        browse_window.destroy()
                        found = True
                        return
            if not found:
                messagebox.showerror("Error", "No matching user found.")
            elif not user_id and not username:
                messagebox.showerror("Error", "Please enter a User ID or Username.")

        def toggle_username_input():
            if user_id_entry.get():
                username_label.grid_forget()
                username_entry.grid_forget()
            else:
                username_label.grid(row=1, column=0)
                username_entry.grid(row=1, column=1)

        user_id_entry.bind("<KeyRelease>", lambda event: toggle_username_input())
        toggle_username_input()

        ttk.Button(browse_window, text="Find User", command=find_user).grid(row=2, column=0, columnspan=2, pady=10)

    def clear_user_frame(self):
        for widget in self.user_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")