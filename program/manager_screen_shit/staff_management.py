import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re
from datetime import datetime

# Color scheme for consistency with other screens
COLORS = {
    'background': '#f0f0f0',
    'header': '#3a7ca5',
    'header_text': 'white',
    'button': '#2c3e50',
    'button_text': 'white',
    'card_bg': '#ffffff',
    'card_border': '#d9d9d9',
    'footer': '#3a7ca5',
    'delete_button': '#e74c3c',
    'add_button': '#27ae60',
    'edit_button': '#f39c12'
}

# Staff data file
STAFF_DATA_DIR = os.path.join("program", "manager_screen_shit", "data")
STAFF_DATA_FILE = os.path.join(STAFF_DATA_DIR, "staff.json")

# Ensure data directory exists
if not os.path.exists(STAFF_DATA_DIR):
    os.makedirs(STAFF_DATA_DIR)

# Staff roles
ROLES = ["Manager", "Ticket Seller", "Usher", "Concession Worker", "Projectionist", "Cleaner"]

class StaffManagementScreen:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_header()
        self.create_main_content()
        self.create_footer()
        self.load_staff_data()
        self.populate_staff_table()
    
    def setup_window(self):
        self.root.title("Cinema Management System - Staff Management")
        self.root.state('zoomed')  # Full window mode
        self.root.configure(bg=COLORS['background'])
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Set minimum size
        self.root.minsize(1024, 768)
    
    def create_header(self):
        # Create a header frame
        self.header_frame = tk.Frame(self.root, bg=COLORS['header'], height=60)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Add title
        tk.Label(
            self.header_frame, 
            text="Staff Management", 
            font=("Arial", 20, "bold"), 
            bg=COLORS['header'], 
            fg=COLORS['header_text']
        ).pack(side=tk.LEFT, padx=20, pady=10)
    
    def create_main_content(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg=COLORS['background'])
        self.main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Split into two frames: controls and table
        self.controls_frame = tk.Frame(self.main_container, bg=COLORS['background'], width=300)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.controls_frame.pack_propagate(False)  # Maintain width
        
        self.table_frame = tk.Frame(self.main_container, bg=COLORS['card_bg'], borderwidth=1, relief="solid")
        self.table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create the controls
        self.create_controls()
        
        # Create the staff table
        self.create_staff_table()
    
    def create_controls(self):
        # Title for the control panel
        tk.Label(
            self.controls_frame,
            text="Staff Controls",
            font=("Arial", 14, "bold"),
            bg=COLORS['background']
        ).pack(anchor="w", pady=(0, 20))
        
        # Add staff button
        add_button = tk.Button(
            self.controls_frame,
            text="Add New Staff",
            command=self.show_add_staff_dialog,
            bg=COLORS['add_button'],
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            width=20
        )
        add_button.pack(pady=10)
        
        # Edit staff button
        edit_button = tk.Button(
            self.controls_frame,
            text="Edit Selected Staff",
            command=self.show_edit_staff_dialog,
            bg=COLORS['edit_button'],
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            width=20
        )
        edit_button.pack(pady=10)
        
        # Delete staff button
        delete_button = tk.Button(
            self.controls_frame,
            text="Delete Selected Staff",
            command=self.delete_staff,
            bg=COLORS['delete_button'],
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            width=20
        )
        delete_button.pack(pady=10)
        
        # Search frame
        search_frame = tk.LabelFrame(self.controls_frame, text="Search Staff", bg=COLORS['background'], padx=10, pady=10)
        search_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(search_frame, text="Name:", bg=COLORS['background']).grid(row=0, column=0, sticky="w", pady=5)
        self.search_name = tk.Entry(search_frame, width=25)
        self.search_name.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(search_frame, text="Role:", bg=COLORS['background']).grid(row=1, column=0, sticky="w", pady=5)
        self.search_role = ttk.Combobox(search_frame, values=["All"] + ROLES, state="readonly", width=22)
        self.search_role.current(0)
        self.search_role.grid(row=1, column=1, sticky="w", pady=5)
        
        search_button = tk.Button(
            search_frame,
            text="Search",
            command=self.search_staff,
            bg=COLORS['button'],
            fg=COLORS['button_text'],
            font=("Arial", 10),
            relief="flat",
            width=10
        )
        search_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Reset search button
        reset_button = tk.Button(
            search_frame,
            text="Reset",
            command=self.reset_search,
            bg="#7f8c8d",
            fg=COLORS['button_text'],
            font=("Arial", 10),
            relief="flat",
            width=10
        )
        reset_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Add a separator
        separator = tk.Frame(self.controls_frame, height=2, bg=COLORS['card_border'])
        separator.pack(fill=tk.X, pady=20)
        
        # Back button
        back_button = tk.Button(
            self.controls_frame,
            text="Back to Manager",
            command=self.root.destroy,
            bg=COLORS['delete_button'],
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            width=20
        )
        back_button.pack(pady=10)
    
    def create_staff_table(self):
        # Create a frame for the table header
        table_header = tk.Frame(self.table_frame, bg=COLORS['header'])
        table_header.pack(fill=tk.X)
        
        # Add header labels
        columns = [
            {"name": "ID", "width": 5},
            {"name": "Name", "width": 20},
            {"name": "Email", "width": 25},
            {"name": "Phone", "width": 15},
            {"name": "Role", "width": 15},
            {"name": "Hire Date", "width": 15},
        ]
        
        for i, col in enumerate(columns):
            tk.Label(
                table_header,
                text=col["name"],
                font=("Arial", 12, "bold"),
                bg=COLORS['header'],
                fg=COLORS['header_text'],
                width=col["width"]
            ).grid(row=0, column=i, padx=2, pady=8, sticky="w")
        
        # Create table contents area with scrollbar
        table_container = tk.Frame(self.table_frame)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(table_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas for scrolling
        self.table_canvas = tk.Canvas(table_container, bg=COLORS['card_bg'], yscrollcommand=scrollbar.set)
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.table_canvas.yview)
        
        # Create frame inside canvas for table rows
        self.table_content = tk.Frame(self.table_canvas, bg=COLORS['card_bg'])
        self.table_canvas.create_window((0, 0), window=self.table_content, anchor="nw")
        
        # Configure canvas scrolling
        self.table_content.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))
        
        # Status bar below table
        self.status_bar = tk.Label(
            self.table_frame,
            text="0 staff members found",
            anchor="w",
            font=("Arial", 10),
            bg=COLORS['background'],
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_footer(self):
        # Create footer
        self.footer_frame = tk.Frame(self.root, bg=COLORS['footer'], height=30)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add footer text
        tk.Label(
            self.footer_frame,
            text="Cinema Management System © 2025",
            font=("Arial", 10),
            bg=COLORS['footer'],
            fg=COLORS['header_text']
        ).pack(side=tk.LEFT, padx=20, pady=5)
    
    def load_staff_data(self):
        """Load staff data from JSON file"""
        try:
            if os.path.exists(STAFF_DATA_FILE):
                with open(STAFF_DATA_FILE, 'r') as file:
                    self.staff_data = json.load(file)
            else:
                # Create a sample staff list if file doesn't exist
                self.staff_data = [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john.doe@cinema.com",
                        "phone": "555-123-4567",
                        "role": "Manager",
                        "hire_date": "2023-01-15"
                    },
                    {
                        "id": 2,
                        "name": "Jane Smith",
                        "email": "jane.smith@cinema.com",
                        "phone": "555-765-4321",
                        "role": "Ticket Seller",
                        "hire_date": "2023-02-20"
                    }
                ]
                self.save_staff_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load staff data: {str(e)}")
            self.staff_data = []
    
    def save_staff_data(self):
        """Save staff data to JSON file"""
        try:
            with open(STAFF_DATA_FILE, 'w') as file:
                json.dump(self.staff_data, file, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save staff data: {str(e)}")
    
    def populate_staff_table(self, data=None):
        """Populate the staff table with data"""
        # Clear existing rows
        for widget in self.table_content.winfo_children():
            widget.destroy()
        
        # Use provided data or all staff data
        staff_to_display = data if data is not None else self.staff_data
        
        # Create row for each staff member
        for i, staff in enumerate(staff_to_display):
            row_color = "#ffffff" if i % 2 == 0 else "#f5f5f5"  # Alternate row colors
            row_frame = tk.Frame(self.table_content, bg=row_color)
            row_frame.pack(fill=tk.X)
            
            # Create selectable row effect
            row_frame.bind("<Button-1>", lambda e, s=staff: self.select_staff(s["id"]))
            row_frame.bind("<Enter>", lambda e, f=row_frame: f.configure(bg="#e0e0e0"))
            row_frame.bind("<Leave>", lambda e, f=row_frame, c=row_color: f.configure(bg=c))
            
            # Add staff details to row
            tk.Label(row_frame, text=staff["id"], bg=row_color, width=5).grid(row=0, column=0, padx=2, pady=8, sticky="w")
            tk.Label(row_frame, text=staff["name"], bg=row_color, width=20).grid(row=0, column=1, padx=2, pady=8, sticky="w")
            tk.Label(row_frame, text=staff["email"], bg=row_color, width=25).grid(row=0, column=2, padx=2, pady=8, sticky="w")
            tk.Label(row_frame, text=staff["phone"], bg=row_color, width=15).grid(row=0, column=3, padx=2, pady=8, sticky="w")
            tk.Label(row_frame, text=staff["role"], bg=row_color, width=15).grid(row=0, column=4, padx=2, pady=8, sticky="w")
            tk.Label(row_frame, text=staff["hire_date"], bg=row_color, width=15).grid(row=0, column=5, padx=2, pady=8, sticky="w")
        
        # Update status bar
        self.status_bar.config(text=f"{len(staff_to_display)} staff members found")
        
        # Initialize selected staff
        self.selected_staff_id = None
    
    def select_staff(self, staff_id):
        """Handle staff selection"""
        self.selected_staff_id = staff_id
        # Highlight the selected row
        for widget in self.table_content.winfo_children():
            for label in widget.winfo_children():
                if label.cget("text") == staff_id:
                    widget.configure(bg="#bde0ff")  # Highlight color
                    for child in widget.winfo_children():
                        child.configure(bg="#bde0ff")
                    break
    
    def show_add_staff_dialog(self):
        """Show dialog to add a new staff member"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Staff Member")
        dialog.configure(bg=COLORS['background'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the window
        window_width = 400
        window_height = 450
        x = (self.screen_width - window_width) // 2
        y = (self.screen_height - window_height) // 2
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Form title
        tk.Label(
            dialog, 
            text="Add New Staff Member",
            font=("Arial", 14, "bold"),
            bg=COLORS['background']
        ).pack(pady=20)
        
        # Create a form frame
        form_frame = tk.Frame(dialog, bg=COLORS['background'], padx=20, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name field
        tk.Label(form_frame, text="Name:", bg=COLORS['background'], anchor="w").grid(row=0, column=0, sticky="w", pady=10)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, sticky="w", pady=10)
        
        # Email field
        tk.Label(form_frame, text="Email:", bg=COLORS['background'], anchor="w").grid(row=1, column=0, sticky="w", pady=10)
        email_entry = tk.Entry(form_frame, width=30)
        email_entry.grid(row=1, column=1, sticky="w", pady=10)
        
        # Phone field
        tk.Label(form_frame, text="Phone:", bg=COLORS['background'], anchor="w").grid(row=2, column=0, sticky="w", pady=10)
        phone_entry = tk.Entry(form_frame, width=30)
        phone_entry.grid(row=2, column=1, sticky="w", pady=10)
        
        # Role field
        tk.Label(form_frame, text="Role:", bg=COLORS['background'], anchor="w").grid(row=3, column=0, sticky="w", pady=10)
        role_combo = ttk.Combobox(form_frame, values=ROLES, state="readonly", width=28)
        role_combo.current(0)
        role_combo.grid(row=3, column=1, sticky="w", pady=10)
        
        # Hire date field
        tk.Label(form_frame, text="Hire Date:", bg=COLORS['background'], anchor="w").grid(row=4, column=0, sticky="w", pady=10)
        hire_date_entry = tk.Entry(form_frame, width=30)
        hire_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today's date
        hire_date_entry.grid(row=4, column=1, sticky="w", pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(dialog, bg=COLORS['background'])
        buttons_frame.pack(pady=20)
        
        def validate_and_add():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            role = role_combo.get()
            hire_date = hire_date_entry.get().strip()
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
            
            if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Error", "Valid email is required")
                return
            
            if not phone:
                messagebox.showerror("Error", "Phone number is required")
                return
            
            if not role:
                messagebox.showerror("Error", "Role must be selected")
                return
            
            # Validate date format
            try:
                datetime.strptime(hire_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Date must be in format YYYY-MM-DD")
                return
            
            # Generate new ID
            new_id = max([staff["id"] for staff in self.staff_data], default=0) + 1
            
            # Create new staff member
            new_staff = {
                "id": new_id,
                "name": name,
                "email": email,
                "phone": phone,
                "role": role,
                "hire_date": hire_date
            }
            
            # Add to staff data and save
            self.staff_data.append(new_staff)
            self.save_staff_data()
            
            # Refresh the table
            self.populate_staff_table()
            
            # Close dialog
            dialog.destroy()
            
            # Show success message
            messagebox.showinfo("Success", f"Staff member {name} added successfully")
        
        # Add and Cancel buttons
        tk.Button(
            buttons_frame,
            text="Add Staff",
            command=validate_and_add,
            bg=COLORS['add_button'],
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            width=10
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#7f8c8d",
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            width=10
        ).grid(row=0, column=1, padx=10)
    
    def show_edit_staff_dialog(self):
        """Show dialog to edit a selected staff member"""
        if self.selected_staff_id is None:
            messagebox.showinfo("Select Staff", "Please select a staff member to edit")
            return
        
        # Find the selected staff member
        selected_staff = next((s for s in self.staff_data if s["id"] == self.selected_staff_id), None)
        if not selected_staff:
            messagebox.showerror("Error", "Selected staff member not found")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Staff Member")
        dialog.configure(bg=COLORS['background'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the window
        window_width = 400
        window_height = 450
        x = (self.screen_width - window_width) // 2
        y = (self.screen_height - window_height) // 2
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Form title
        tk.Label(
            dialog, 
            text=f"Edit Staff: {selected_staff['name']}",
            font=("Arial", 14, "bold"),
            bg=COLORS['background']
        ).pack(pady=20)
        
        # Create a form frame
        form_frame = tk.Frame(dialog, bg=COLORS['background'], padx=20, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # ID field (disabled)
        tk.Label(form_frame, text="ID:", bg=COLORS['background'], anchor="w").grid(row=0, column=0, sticky="w", pady=10)
        id_entry = tk.Entry(form_frame, width=30)
        id_entry.insert(0, str(selected_staff["id"]))
        id_entry.config(state="disabled")
        id_entry.grid(row=0, column=1, sticky="w", pady=10)
        
        # Name field
        tk.Label(form_frame, text="Name:", bg=COLORS['background'], anchor="w").grid(row=1, column=0, sticky="w", pady=10)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.insert(0, selected_staff["name"])
        name_entry.grid(row=1, column=1, sticky="w", pady=10)
        
        # Email field
        tk.Label(form_frame, text="Email:", bg=COLORS['background'], anchor="w").grid(row=2, column=0, sticky="w", pady=10)
        email_entry = tk.Entry(form_frame, width=30)
        email_entry.insert(0, selected_staff["email"])
        email_entry.grid(row=2, column=1, sticky="w", pady=10)
        
        # Phone field
        tk.Label(form_frame, text="Phone:", bg=COLORS['background'], anchor="w").grid(row=3, column=0, sticky="w", pady=10)
        phone_entry = tk.Entry(form_frame, width=30)
        phone_entry.insert(0, selected_staff["phone"])
        phone_entry.grid(row=3, column=1, sticky="w", pady=10)
        
        # Role field
        tk.Label(form_frame, text="Role:", bg=COLORS['background'], anchor="w").grid(row=4, column=0, sticky="w", pady=10)
        role_combo = ttk.Combobox(form_frame, values=ROLES, state="readonly", width=28)
        role_combo.set(selected_staff["role"])
        role_combo.grid(row=4, column=1, sticky="w", pady=10)
        
        # Hire date field
        tk.Label(form_frame, text="Hire Date:", bg=COLORS['background'], anchor="w").grid(row=5, column=0, sticky="w", pady=10)
        hire_date_entry = tk.Entry(form_frame, width=30)
        hire_date_entry.insert(0, selected_staff["hire_date"])
        hire_date_entry.grid(row=5, column=1, sticky="w", pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(dialog, bg=COLORS['background'])
        buttons_frame.pack(pady=20)
        
        def validate_and_update():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            role = role_combo.get()
            hire_date = hire_date_entry.get().strip()
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
            
            if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Error", "Valid email is required")
                return
            
            if not phone:
                messagebox.showerror("Error", "Phone number is required")
                return
            
            if not role:
                messagebox.showerror("Error", "Role must be selected")
                return
            
            # Validate date format
            try:
                datetime.strptime(hire_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Date must be in format YYYY-MM-DD")
                return
            
            # Update staff member
            for staff in self.staff_data:
                if staff["id"] == self.selected_staff_id:
                    staff["name"] = name
                    staff["email"] = email
                    staff["phone"] = phone
                    staff["role"] = role
                    staff["hire_date"] = hire_date
                    break
            
            # Save changes
            self.save_staff_data()
            
            # Refresh the table
            self.populate_staff_table()
            
            # Close dialog
            dialog.destroy()
            
            # Show success message
            messagebox.showinfo("Success", f"Staff member {name} updated successfully")
        
        # Update and Cancel buttons
        tk.Button(
            buttons_frame,
            text="Update",
            command=validate_and_update,
            bg=COLORS['edit_button'],
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            width=10
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#7f8c8d",
            fg=COLORS['button_text'],
            font=("Arial", 12),
            relief="flat",
            width=10
        ).grid(row=0, column=1, padx=10)
    
    def delete_staff(self):
        """Delete a selected staff member"""
        if self.selected_staff_id is None:
            messagebox.showinfo("Select Staff", "Please select a staff member to delete")
            return
        
        # Find the selected staff member
        selected_staff = next((s for s in self.staff_data if s["id"] == self.selected_staff_id), None)
        if not selected_staff:
            messagebox.showerror("Error", "Selected staff member not found")
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete staff member {selected_staff['name']}?"
        )
        
        if confirm:
            # Remove from staff data
            self.staff_data = [s for s in self.staff_data if s["id"] != self.selected_staff_id]
            
            # Save changes
            self.save_staff_data()
            
            # Reset selection
            self.selected_staff_id = None
            
            # Refresh the table
            self.populate_staff_table()
            
            # Show success message
            messagebox.showinfo("Success", f"Staff member {selected_staff['name']} deleted successfully")
    
    def search_staff(self):
        """Search staff based on criteria"""
        name_query = self.search_name.get().strip().lower()
        role_query = self.search_role.get()
        
        # Apply filters
        filtered_staff = self.staff_data.copy()
        
        if name_query:
            filtered_staff = [s for s in filtered_staff if name_query in s["name"].lower()]
        
        if role_query != "All":
            filtered_staff = [s for s in filtered_staff if s["role"] == role_query]
        
        # Display filtered results
        self.populate_staff_table(filtered_staff)
    
    def reset_search(self):
        """Reset search fields and show all staff"""
        self.search_name.delete(0, tk.END)
        self.search_role.current(0)
        self.populate_staff_table()

def main():
    root = tk.Tk()
    app = StaffManagementScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()