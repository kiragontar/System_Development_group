import tkinter as tk
from tkinter import ttk, messagebox
from database.database_settings import SessionLocal
from main_components.services.role_service import RoleService
from main_components.services.permission_service import PermissionService

class RoleManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.session = SessionLocal()
        self.role_service = RoleService(self.session)
        self.permission_service = PermissionService(self.session)
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

        tk.Label(main_frame, text="Role Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        self.role_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.role_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_roles()

    def manage_roles(self):
        self.clear_role_frame()
        self.role_list = ttk.Treeview(
            self.role_frame,
            columns=("ID", "Name"),
            show="headings",
        )
        self.role_list.heading("ID", text="ID")
        self.role_list.heading("Name", text="Name")
        self.role_list.pack(expand=True, fill="both")

        roles = self.role_service.get_all_roles()
        for role in roles:
            self.role_list.insert("", tk.END, values=(role.role_id, role.name))

        action_frame = ttk.Frame(self.role_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add Role", command=self.add_role).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update Role", command=self.update_role).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Remove Role", command=self.remove_role).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse Role", command=self.browse_role).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Add Permission", command=self.add_permission_to_role_ui).pack(side=tk.LEFT, padx=5) 
        ttk.Button(action_frame, text="Remove Permission", command=self.remove_permission_from_role_ui).pack(side=tk.LEFT, padx=5) 
        ttk.Button(action_frame, text="View Permissions", command=self.view_role_permissions_ui).pack(side=tk.LEFT, padx=5) 

        self.role_list.bind("<ButtonRelease-1>", self.select_role)
        self.selected_role_id = None
        self.role_frame.update()

    def select_role(self, event):
        selection = self.role_list.selection()
        if selection:
            item = selection[0]
            self.selected_role_id = self.role_list.item(item, "values")[0]
        else:
            self.selected_role_id = None

    def is_valid_role_name(self, name):
        return isinstance(name, str) and name.strip() != ""


    def add_role(self):
        if RoleManagement.add_window_open:
            messagebox.showerror("Error", "Add Role window is already open.")
            return

        RoleManagement.add_window_open = True

        add_frame = ttk.Frame(self.role_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Role Name:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(add_frame)
        self.name_entry.grid(row=0, column=1)

        def add_role_confirm():
            name = self.name_entry.get()

            if not self.is_valid_role_name(name):
                messagebox.showerror("Error", "Invalid Role Name. Please enter a valid name.")
                return

            try:
                self.role_service.create_role(name)
                RoleManagement.add_window_open = False
                self.manage_roles()
                add_frame.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def cancel_add():
            RoleManagement.add_window_open = False
            add_frame.destroy()

        ttk.Button(add_frame, text="Confirm Add", command=add_role_confirm).grid(row=1, column=0, pady=5, padx=(0, 5))
        ttk.Button(add_frame, text="Cancel", command=cancel_add).grid(row=1, column=1, pady=5, padx=(5, 0))



    def update_role(self):
        if RoleManagement.update_window_open:
            messagebox.showerror("Error", "Update Role window is already open.")
            return

        RoleManagement.update_window_open = True

        if self.selected_role_id:
            update_frame = ttk.Frame(self.role_frame)
            update_frame.pack(pady=10)

            role = self.role_service.get_role_by_id(self.selected_role_id)

            tk.Label(update_frame, text="Role Name:").grid(row=0, column=0)
            self.name_entry = ttk.Entry(update_frame)
            self.name_entry.insert(0, role.name)
            self.name_entry.grid(row=0, column=1)

            def update_role_confirm():
                name = self.name_entry.get()

                if not self.is_valid_role_name(name):
                    messagebox.showerror("Error", "Invalid Role Name. Please enter a valid name.")
                    return

                try:
                    self.role_service.update_role(self.selected_role_id, name)
                    RoleManagement.update_window_open = False
                    self.manage_roles()
                    update_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            def cancel_update():
                RoleManagement.update_window_open = False
                update_frame.destroy()

            ttk.Button(update_frame, text="Confirm Update", command=update_role_confirm).grid(row=1, column=0, pady=5, padx=(0, 5))
            ttk.Button(update_frame, text="Cancel", command=cancel_update).grid(row=1, column=1, pady=5, padx=(5, 0))

        else:
            messagebox.showerror("Error", "Select a role to update.")
            RoleManagement.update_window_open = False

    
    def remove_role(self):
        if self.selected_role_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this role?"):
                self.role_service.delete_role(self.selected_role_id)
                self.manage_roles()
        else:
            messagebox.showerror("Error", "Select a role to remove.")

    
    def browse_role(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse Role")

        tk.Label(browse_window, text="Role ID (Optional):").grid(row=0, column=0)
        role_id_entry = ttk.Entry(browse_window)
        role_id_entry.grid(row=0, column=1)

        tk.Label(browse_window, text="Role Name (Optional):").grid(row=1, column=0)
        role_name_entry = ttk.Entry(browse_window)
        role_name_entry.grid(row=1, column=1)

        def find_role():
            role_id = role_id_entry.get()
            role_name = role_name_entry.get()
            found = False

            if role_id:
                for item in self.role_list.get_children():
                    values = self.role_list.item(item, 'values')
                    if values and len(values) > 0 and str(values[0]) == role_id:
                        self.role_list.see(item)
                        self.role_list.selection_set(item)
                        self.role_list.focus(item)
                        self.selected_role_id = role_id
                        browse_window.destroy()
                        found = True
                        return
            elif role_name:
                for item in self.role_list.get_children():
                    values = self.role_list.item(item, 'values')
                    if values and len(values) > 1 and values[1] == role_name:
                        self.role_list.see(item)
                        self.role_list.selection_set(item)
                        self.role_list.focus(item)
                        self.selected_role_id = values[0]
                        browse_window.destroy()
                        found = True
                        return
            if not found:
                messagebox.showerror("Error", "No matching role found.")

        ttk.Button(browse_window, text="Find Role", command=find_role).grid(row=2, column=0, columnspan=2, pady=10)


    def add_permission_to_role_ui(self):
        if self.selected_role_id:
            permission_id = self.get_permission_id_from_user()
            if permission_id:
                if self.role_service.add_permission_to_role(self.selected_role_id, permission_id):
                    messagebox.showinfo("Success", "Permission added successfully.")
                else:
                    messagebox.showerror("Error", "Failed to add permission.")
        else:
            messagebox.showerror("Error", "Select a role first.")

    def remove_permission_from_role_ui(self):
        if self.selected_role_id:
            permission_id = self.get_permission_id_from_user()
            if permission_id:
                if self.role_service.remove_permission_from_role(self.selected_role_id, permission_id):
                    messagebox.showinfo("Success", "Permission removed successfully.")
                else:
                    messagebox.showerror("Error", "Failed to remove permission.")
        else:
            messagebox.showerror("Error", "Select a role first.")

    def view_role_permissions_ui(self):
        if self.selected_role_id:
            permissions = self.role_service.get_permissions_for_role(self.selected_role_id)
            if permissions:
                permission_strings = [f"{p.name} ({p.permission_id})" for p in permissions]
                messagebox.showinfo("Role Permissions", "\n".join(permission_strings))
            else:
                messagebox.showinfo("Role Permissions", "No permissions found for this role.")
        else:
            messagebox.showerror("Error", "Select a role first.")

    def get_permission_id_from_user(self):
        permission_id = tk.simpledialog.askinteger("Permission ID", "Enter Permission ID:")
        return permission_id

    def clear_role_frame(self):
        for widget in self.role_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")


