import tkinter as tk
from tkinter import ttk, messagebox
from database.database_settings import SessionLocal
from main_components.services.permission_service import PermissionService

class PermissionManagement(tk.Frame):
    add_window_open = False
    update_window_open = False

    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.session = SessionLocal()
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

        tk.Label(main_frame, text="Permission Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Back", command=self.go_back).grid(row=1, column=1, pady=10)

        self.permission_frame = ttk.Frame(main_frame, style="LightYellow.TFrame")
        self.permission_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.manage_permissions()

    def manage_permissions(self):
        self.clear_permission_frame()
        self.permission_list = ttk.Treeview(
            self.permission_frame,
            columns=("ID", "Name"),
            show="headings",
        )
        self.permission_list.heading("ID", text="ID")
        self.permission_list.heading("Name", text="Name")
        self.permission_list.pack(expand=True, fill="both")

        permissions = self.permission_service.get_all_permissions()
        for permission in permissions:
            self.permission_list.insert("", tk.END, values=(permission.permission_id, permission.name))

        action_frame = ttk.Frame(self.permission_frame, style="LightBlue.TFrame")
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add Permission", command=self.add_permission).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update Permission", command=self.update_permission).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Remove Permission", command=self.remove_permission).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Browse Permission", command=self.browse_permission).pack(side=tk.LEFT, padx=5)

        self.permission_list.bind("<ButtonRelease-1>", self.select_permission)
        self.selected_permission_id = None
        self.permission_frame.update()

    def select_permission(self, event):
        selection = self.permission_list.selection()
        if selection:
            item = selection[0]
            self.selected_permission_id = self.permission_list.item(item, "values")[0]
        else:
            self.selected_permission_id = None

    def is_valid_permission_name(self, name):
        return isinstance(name, str) and name.strip() != ""


    def add_permission(self):
        if PermissionManagement.add_window_open:
            messagebox.showerror("Error", "Add Permission window is already open.")
            return

        PermissionManagement.add_window_open = True

        add_frame = ttk.Frame(self.permission_frame)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Permission Name:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(add_frame)
        self.name_entry.grid(row=0, column=1)

        def add_permission_confirm():
            name = self.name_entry.get()

            if not self.is_valid_permission_name(name):
                messagebox.showerror("Error", "Invalid Permission Name. Please enter a valid name.")
                return

            try:
                self.permission_service.create_permission(name)
                PermissionManagement.add_window_open = False
                self.manage_permissions()
                add_frame.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def cancel_add():
            PermissionManagement.add_window_open = False
            add_frame.destroy()

        ttk.Button(add_frame, text="Confirm Add", command=add_permission_confirm).grid(row=1, column=0, pady=5, padx=(0, 5))
        ttk.Button(add_frame, text="Cancel", command=cancel_add).grid(row=1, column=1, pady=5, padx=(5, 0))

    
    def update_permission(self):
        if PermissionManagement.update_window_open:
            messagebox.showerror("Error", "Update Permission window is already open.")
            return

        PermissionManagement.update_window_open = True

        if self.selected_permission_id:
            update_frame = ttk.Frame(self.permission_frame)
            update_frame.pack(pady=10)

            permission = self.permission_service.get_permission_by_id(self.selected_permission_id)

            tk.Label(update_frame, text="Permission Name:").grid(row=0, column=0)
            self.name_entry = ttk.Entry(update_frame)
            self.name_entry.insert(0, permission.name)
            self.name_entry.grid(row=0, column=1)

            def update_permission_confirm():
                name = self.name_entry.get()

                if not self.is_valid_permission_name(name):
                    messagebox.showerror("Error", "Invalid Permission Name. Please enter a valid name.")
                    return

                try:
                    self.permission_service.update_permission(self.selected_permission_id, name)
                    PermissionManagement.update_window_open = False
                    self.manage_permissions()
                    update_frame.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            def cancel_update():
                PermissionManagement.update_window_open = False
                update_frame.destroy()

            ttk.Button(update_frame, text="Confirm Update", command=update_permission_confirm).grid(row=1, column=0, pady=5, padx=(0, 5))
            ttk.Button(update_frame, text="Cancel", command=cancel_update).grid(row=1, column=1, pady=5, padx=(5, 0))

        else:
            messagebox.showerror("Error", "Select a permission to update.")
            PermissionManagement.update_window_open = False


    def remove_permission(self):
        if self.selected_permission_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this permission?"):
                self.permission_service.delete_permission(self.selected_permission_id)
                self.manage_permissions()
        else:
            messagebox.showerror("Error", "Select a permission to remove.")

    def browse_permission(self):
        browse_window = tk.Toplevel(self)
        browse_window.title("Browse Permission")

        tk.Label(browse_window, text="Permission ID (Optional):").grid(row=0, column=0)
        permission_id_entry = ttk.Entry(browse_window)
        permission_id_entry.grid(row=0, column=1)

        tk.Label(browse_window, text="Permission Name (Optional):").grid(row=1, column=0)
        permission_name_entry = ttk.Entry(browse_window)
        permission_name_entry.grid(row=1, column=1)

        def find_permission():
            permission_id = permission_id_entry.get()
            permission_name = permission_name_entry.get()
            found = False

            if permission_id:
                for item in self.permission_list.get_children():
                    values = self.permission_list.item(item, 'values')
                    if values and len(values) > 0 and str(values[0]) == permission_id:
                        self.permission_list.see(item)
                        self.permission_list.selection_set(item)
                        self.permission_list.focus(item)
                        self.selected_permission_id = permission_id
                        browse_window.destroy()
                        found = True
                        return
            elif permission_name:
                for item in self.permission_list.get_children():
                    values = self.permission_list.item(item, 'values')
                    if values and len(values) > 1 and values[1] == permission_name:
                        self.permission_list.see(item)
                        self.permission_list.selection_set(item)
                        self.permission_list.focus(item)
                        self.selected_permission_id = values[0]
                        browse_window.destroy()
                        found = True
                        return
            if not found:
                messagebox.showerror("Error", "No matching permission found.")

        ttk.Button(browse_window, text="Find Permission", command=find_permission).grid(row=2, column=0, columnspan=2, pady=10)

    def clear_permission_frame(self):
        for widget in self.permission_frame.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.callback:
            self.callback("back")
