# frontend/permission_management.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.permission_service import PermissionService

def run_permission_management(parent, session):
    window = tk.Toplevel(parent)
    window.title("Permission Management")
    window.geometry("800x400")
    window.configure(bg="#6e7c91")

    perm_service = PermissionService(session)
    
    # Treeview
    tree_frame = ttk.Frame(window)
    tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    tree = ttk.Treeview(tree_frame, columns=("ID", "Name"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Permission Name")
    tree.column("ID", width=50, anchor='center')
    tree.column("Name", width=200)
    tree.pack(side='left', fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Entry Form
    form_frame = ttk.Frame(window)
    form_frame.pack(pady=10, fill='x', padx=20)
    
    ttk.Label(form_frame, text="Permission Name:").pack(side='left')
    name_entry = ttk.Entry(form_frame, width=30)
    name_entry.pack(side='left', padx=10)
    
    # Buttons
    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)
    
    def refresh_permissions():
        tree.delete(*tree.get_children())
        # Sort permissions by ID (FIXED)
        sorted_perms = sorted(perm_service.get_all_permissions(), key=lambda x: x.permission_id)
        for perm in sorted_perms:
            tree.insert("", "end", values=(perm.permission_id, perm.name))
    
    def create_permission():
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Error", "Name required")
            return
        
        if perm_service.create_permission(name):
            refresh_permissions()
            name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Permission already exists")
    
    def update_permission():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Select a permission first")
            return
            
        perm_id = tree.item(selected[0])['values'][0]
        new_name = name_entry.get().strip()
        
        if not new_name:
            messagebox.showwarning("Error", "New name required")
            return
        
        existing = perm_service.get_permission_by_name(new_name)
        if existing and existing.permission_id != perm_id:
            messagebox.showerror("Error", "Permission name already exists")
            return
            
        if perm_service.update_permission(perm_id, new_name):
            refresh_permissions()
            name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Update failed")
    
    def delete_permission():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Select a permission first")
            return
        
        perm_id = tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this permission permanently?"):
            if perm_service.delete_permission(perm_id):
                refresh_permissions()
            else:
                messagebox.showerror("Error", "Delete failed - check if in use")

    def on_select(event):
        selected = tree.selection()
        if selected:
            perm_name = tree.item(selected[0])['values'][1]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, perm_name)

    # Button layout
    ttk.Button(button_frame, text="Create", command=create_permission).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Update", command=update_permission).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Refresh", command=refresh_permissions).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Delete", command=delete_permission).pack(side=tk.LEFT, padx=5)
    
    # Event binding
    tree.bind("<<TreeviewSelect>>", on_select)
    
    # Initial load
    refresh_permissions()
    window.mainloop()