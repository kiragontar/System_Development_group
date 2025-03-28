# frontend/role_management.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.role_service import RoleService
from backend.permission_service import PermissionService

def run_role_management(parent, session):
    window = tk.Toplevel(parent)
    window.title("Role Management")
    window.geometry("1000x600")
    window.configure(bg="#6e7c91")
    
    role_service = RoleService(session)
    perm_service = PermissionService(session)
    
    # ====== Role List ======
    tree_frame = ttk.Frame(window)
    tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Permissions"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Role Name")
    tree.heading("Permissions", text="Permissions")
    tree.column("ID", width=50, anchor='center')
    tree.column("Name", width=150)
    tree.column("Permissions", width=300)
    tree.pack(side='left', fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)
    
    # ====== Role Form ======
    form_frame = ttk.Frame(window)
    form_frame.pack(pady=10, fill='x', padx=20)
    
    ttk.Label(form_frame, text="Role Name:").pack(side='left')
    name_entry = ttk.Entry(form_frame, width=30)
    name_entry.pack(side='left', padx=10)
    
    # ====== Action Buttons ======
    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)
    
    def clear_form():
        name_entry.delete(0, tk.END)
        tree.selection_remove(tree.selection())
    
    def refresh_roles():
        tree.delete(*tree.get_children())
        for role in role_service.get_all_roles():
            perms = ", ".join([p.name for p in role.permissions])
            tree.insert("", "end", values=(role.role_id, role.name, perms))
    
    def create_role():
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Error", "Role name required")
            return
        if role_service.create_role(name):
            refresh_roles()
            clear_form()
        else:
            messagebox.showerror("Error", "Role already exists")
    
    def update_role():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Error", "No role selected")
            return
            
        role_id = tree.item(selected[0])['values'][0]
        new_name = name_entry.get().strip()
        
        if not new_name:
            messagebox.showwarning("Error", "New name required")
            return
            
        if role_service.update_role(role_id, new_name):
            refresh_roles()
            clear_form()
        else:
            messagebox.showerror("Error", "Update failed")
    
    def delete_role():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Error", "No role selected")
            return
            
        role_id = tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this role permanently?"):
            if role_service.delete_role(role_id):
                refresh_roles()
                clear_form()
            else:
                messagebox.showerror("Error", "Delete failed (users assigned or permissions exist)")
    
    def manage_role_permissions():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Select a role first")
            return
        
        role_id = tree.item(selected[0])['values'][0]
        role = role_service.get_role_by_id(role_id)
        
        perm_dialog = tk.Toplevel(window)
        perm_dialog.title(f"Manage Permissions for {role.name}")
        perm_dialog.geometry("500x400")
        
        # --- Create a container frame to hold all three columns ---
        container = ttk.Frame(perm_dialog)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ====== Available Permissions ======
        available_frame = ttk.Frame(container)
        available_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(available_frame, text="Available Permissions").pack()
        available_list = tk.Listbox(available_frame)
        available_list.pack(fill='both', expand=True)
        
        # ====== Buttons Frame in the center ======
        btn_frame = ttk.Frame(container)
        btn_frame.pack(side='left', fill='y', padx=10)
        
        def add_permission():
            selected_idx = available_list.curselection()
            if not selected_idx:
                return
            perm_str = available_list.get(selected_idx[0])
            perm_id = int(perm_str.split("ID: ")[1].rstrip(")"))
            
            if role_service.add_permission_to_role(role.role_id, perm_id):
                current_list.insert(tk.END, perm_str)
                available_list.delete(selected_idx[0])
                refresh_roles()
        
        def remove_permission():
            selected_idx = current_list.curselection()
            if not selected_idx:
                return
            perm_str = current_list.get(selected_idx[0])
            perm_id = int(perm_str.split("ID: ")[1].rstrip(")"))
            
            if role_service.remove_permission_from_role(role.role_id, perm_id):
                available_list.insert(tk.END, perm_str)
                current_list.delete(selected_idx[0])
                refresh_roles()
        
        ttk.Button(btn_frame, text="<< Add", command=add_permission).pack(pady=5)
        ttk.Button(btn_frame, text="Remove >>", command=remove_permission).pack(pady=5)
        
        # ====== Current Permissions ======
        current_frame = ttk.Frame(container)
        current_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(current_frame, text="Current Permissions").pack()
        current_list = tk.Listbox(current_frame)
        current_list.pack(fill='both', expand=True)
        
        # ====== Load Data ======
        all_perms = perm_service.get_all_permissions()
        current_perms = role.permissions
        
        for perm in all_perms:
            if perm not in current_perms:
                available_list.insert(tk.END, f"{perm.name} (ID: {perm.permission_id})")
        
        for perm in current_perms:
            current_list.insert(tk.END, f"{perm.name} (ID: {perm.permission_id})")
    
    def on_select(event):
        selected = tree.selection()
        if selected:
            role_name = tree.item(selected[0])['values'][1]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, role_name)
    
    # ====== Main Buttons ======
    ttk.Button(button_frame, text="Create", command=create_role).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Update", command=update_role).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Delete", command=delete_role).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Clear", command=clear_form).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Manage Permissions", command=manage_role_permissions).pack(side='left', padx=5)
    
    tree.bind("<<TreeviewSelect>>", on_select)
    refresh_roles()
    window.mainloop()
