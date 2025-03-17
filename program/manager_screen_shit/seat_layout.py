import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Seat symbols
SEAT_SYMBOLS = {'low': '○', 'upper': '■', 'VIP': '▲'}

# Color scheme for a more professional look
COLORS = {
    'background': '#f0f0f0',
    'header': '#3a7ca5',
    'header_text': 'white',
    'button': '#2c3e50',
    'button_text': 'white',
    'empty_seat': '#d9d9d9',
    'seat_border': '#a3a3a3',
    'low_seat': '#81c784',
    'upper_seat': '#64b5f6',
    'vip_seat': '#ba68c8'
}

# Create layouts directory if it doesn't exist
layouts_dir = os.path.join("program", "manager_screen_shit", "layouts")
if not os.path.exists(layouts_dir):
    os.makedirs(layouts_dir)

# Save layout with user-entered name
def save_layout():
    global layout_name, seats
    
    # Check if seats is initialized (basic check to prevent errors)
    if not seats or len(seats) == 0:
        messagebox.showerror("Error", "No layout to save! Please create a layout first.")
        return
    
    save_window = tk.Toplevel(root)
    save_window.title("Save Layout")
    save_window.geometry("350x150")
    save_window.configure(bg=COLORS['background'])
    save_window.transient(root)  # Keep popup on top
    save_window.grab_set()

    # Center the window on the screen
    window_width = 350
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    save_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Prompt for layout name
    tk.Label(save_window, text="Enter layout name:", font=("Arial", 12), bg=COLORS['background']).pack(pady=10)
    name_entry = tk.Entry(save_window, font=("Arial", 12), width=25)
    name_entry.pack(pady=10)
    name_entry.focus_set()  # Automatically focus the entry field

    def confirm_save():
        global layout_name
        entered_name = name_entry.get().strip()
        if entered_name:
            layout_name = entered_name
            file_path = os.path.join(layouts_dir, f"{entered_name}.json")
            with open(file_path, 'w') as file:
                json.dump(seats, file)
            messagebox.showinfo("Save", f"Seat layout '{entered_name}' saved successfully!")
            save_window.destroy()
        else:
            messagebox.showerror("Error", "Layout name cannot be empty!")

    save_button = tk.Button(
        save_window, 
        text="Save", 
        command=confirm_save, 
        bg=COLORS['button'], 
        fg=COLORS['button_text'],
        font=("Arial", 12),
        relief="flat",
        padx=20
    )
    save_button.pack(pady=10)

# Update load_layout to use the layouts directory
def load_layout():
    global seats, layout_name
    
    # Check if layouts directory exists, create if not
    if not os.path.exists(layouts_dir):
        os.makedirs(layouts_dir)
        
    layouts = [f[:-5] for f in os.listdir(layouts_dir) if f.endswith('.json')]
    if not layouts:
        messagebox.showwarning("Load", "No saved layouts found!")
        return

    load_window = tk.Toplevel(root)
    load_window.title("Load Layout")
    load_window.geometry("450x300")
    load_window.configure(bg=COLORS['background'])
    load_window.transient(root)
    load_window.grab_set()
    
    # Center the window on the screen
    window_width = 450
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position coordinates
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # Set the position
    load_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(load_window, text="Select a layout to load or delete:", font=("Arial", 12, "bold"), bg=COLORS['background']).pack(pady=10)
    
    # Create a frame to contain the list of layouts
    list_frame = tk.Frame(load_window, bg=COLORS['background'])
    list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
    
    # Create a listbox to display layouts instead of dropdown
    layout_listbox = tk.Listbox(list_frame, font=("Arial", 12), width=25, height=8, selectmode=tk.SINGLE)
    layout_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Add scrollbar to the listbox
    scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=layout_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    layout_listbox.config(yscrollcommand=scrollbar.set)
    
    # Populate the listbox with layout names
    for layout in layouts:
        layout_listbox.insert(tk.END, layout)
    
    button_frame = tk.Frame(load_window, bg=COLORS['background'])
    button_frame.pack(fill=tk.X, pady=10)
    
    def delete_selected_layout():
        if layout_listbox.curselection():
            selected_index = layout_listbox.curselection()[0]
            selected_layout = layout_listbox.get(selected_index)
            
            # Confirm deletion
            if messagebox.askyesno("Delete Layout", f"Are you sure you want to delete '{selected_layout}' layout?"):
                # Delete the file from layouts directory
                file_to_delete = os.path.join(layouts_dir, f"{selected_layout}.json")
                try:
                    os.remove(file_to_delete)
                    layouts.remove(selected_layout)
                    layout_listbox.delete(selected_index)
                    status_label.config(text=f"Status: Layout '{selected_layout}' deleted")
                    
                    # If no layouts left, close the window
                    if not layouts:
                        messagebox.showinfo("Delete Layout", "No more layouts available.")
                        load_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete layout: {str(e)}")
    
    def confirm_selection():
        global seats, layout_name
        if layout_listbox.curselection():
            selected_index = layout_listbox.curselection()[0]
            layout_name = layout_listbox.get(selected_index)
            
            file_path = os.path.join(layouts_dir, f"{layout_name}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    seats = json.load(file)
                refresh_layout()
                # Update the layout label at the top
                loaded_layout_label.config(text=f"Layout: {layout_name}")
                status_label.config(text=f"Status: Layout '{layout_name}' loaded")
                load_window.destroy()
            else:
                messagebox.showerror("Error", "Please select a valid layout!")
        else:
            messagebox.showinfo("Select", "Please select a layout first.")

    # Add buttons for loading and deleting layouts
    load_button = tk.Button(
        button_frame, 
        text="Load Selected", 
        command=confirm_selection, 
        bg=COLORS['button'], 
        fg=COLORS['button_text'],
        font=("Arial", 12),
        relief="flat",
        padx=20
    )
    load_button.pack(side=tk.LEFT, padx=10, expand=True)
    
    delete_button = tk.Button(
        button_frame, 
        text="Delete Selected", 
        command=delete_selected_layout, 
        bg="#c0392b", 
        fg="white",
        font=("Arial", 12),
        relief="flat",
        padx=20
    )
    delete_button.pack(side=tk.RIGHT, padx=10, expand=True)

def add_seat(event):
    row = event.widget.grid_info()["row"] - 1
    col = event.widget.grid_info()["column"] - 1

    if 0 <= row < len(seats) and 0 <= col < len(seats[row]):
        # Create a popup window near the clicked cell
        button_window = tk.Toplevel(root)
        button_window.geometry(f"+{event.x_root + 50}+{event.y_root}")  # Position near the cursor
        button_window.title("Choose Seat Class")
        button_window.configure(bg=COLORS['background'])
        button_window.transient(root)
        button_window.grab_set()

        def select_class(seat_class):
            seats[row][col] = seat_class
            refresh_layout()
            status_label.config(text=f"Status: Added a {seat_class} seat at row {row+1}, column {col+1}")
            button_window.destroy()

        # Add buttons for each seat class with better styling
        tk.Button(
            button_window, 
            text="Low (○)", 
            command=lambda: select_class('low'),
            bg=COLORS['low_seat'],
            font=("Arial", 11),
            width=12,
            relief="flat"
        ).pack(pady=5)
        
        tk.Button(
            button_window, 
            text="Upper (■)", 
            command=lambda: select_class('upper'),
            bg=COLORS['upper_seat'],
            font=("Arial", 11),
            width=12,
            relief="flat"
        ).pack(pady=5)
        
        tk.Button(
            button_window, 
            text="VIP (▲)", 
            command=lambda: select_class('VIP'),
            bg=COLORS['vip_seat'],
            font=("Arial", 11),
            width=12,
            relief="flat"
        ).pack(pady=5)

def delete_seat(event):
    row = event.widget.grid_info()["row"] - 1
    col = event.widget.grid_info()["column"] - 1
    if 0 <= row < len(seats) and 0 <= col < len(seats[row]):
        seats[row][col] = None
        refresh_layout()
        status_label.config(text=f"Status: Removed seat at row {row+1}, column {col+1}")

def refresh_layout():
    # Store the current seat_frame if it exists to avoid recreating everything
    existing_frame = None
    for widget in inner_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            existing_frame = widget
            break
    
    if not seats or len(seats) == 0:
        if existing_frame:
            existing_frame.destroy()
        return
    
    # Get current dimensions of the canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    # Calculate the number of rows and columns
    rows = len(seats)
    cols = len(seats[0]) if rows > 0 else 0
    
    # Calculate the best seat size to use all available space
    # Leave some margin and account for row/column labels
    available_width = canvas_width * 0.9
    available_height = canvas_height * 0.9
    
    # Calculate the max size each seat can be while maintaining square shape
    max_seat_width = available_width / (cols + 1)  # +1 for row labels
    max_seat_height = available_height / (rows + 1)  # +1 for column labels
    
    # Use the smaller dimension to maintain square seats
    seat_size = min(max_seat_width, max_seat_height)
    
    # Scale padding and font based on the seat size
    padding = max(3, int(seat_size * 0.1))
    font_size = max(9, min(16, int(seat_size * 0.35)))  # Keep font size reasonable
    
    # Create a frame with fixed size to hold all seats if not already created
    if not existing_frame:
        seat_frame = tk.Frame(inner_frame, bg=COLORS['background'])
        seat_frame.pack(expand=True, padx=20, pady=20)
    else:
        seat_frame = existing_frame
    
    # Update seats instead of recreating everything
    for r in range(len(seats)):
        for c, seat_class in enumerate(seats[r]):
            # Find if this position already has a widget
            existing_widget = None
            for widget in seat_frame.grid_slaves(row=r+1, column=c+1):
                existing_widget = widget
                break
                
            if seat_class:
                symbol = SEAT_SYMBOLS[seat_class]
                bg_color = COLORS['low_seat'] if seat_class == 'low' else COLORS['upper_seat'] if seat_class == 'upper' else COLORS['vip_seat']
                
                # Create the widget dimensions based on calculated seat size
                width = int(seat_size / 20)  # Convert pixels to character width approximation
                height = int(seat_size / 30)  # Convert pixels to character height approximation
                
                # Ensure minimum size
                width = max(2, width)
                height = max(1, height)
                
                # Update existing widget if possible
                if existing_widget:
                    existing_widget.config(text=symbol, bg=bg_color, width=width, height=height, 
                                          font=("Arial Bold", font_size))
                else:
                    label = tk.Label(
                        seat_frame, 
                        text=symbol, 
                        font=("Arial Bold", font_size), 
                        width=width, 
                        height=height,
                        borderwidth=1, 
                        relief="solid",
                        bg=bg_color
                    )
                    label.grid(row=r+1, column=c+1, padx=padding, pady=padding)
                    label.bind("<Button-1>", add_seat)
                    label.bind("<Button-3>", delete_seat)
                    
                    # Add tooltips
                    tooltip_text = f"Left click to change, Right click to delete\nR{r+1}C{c+1}: {seat_class.upper()} seat"
                    tooltip = ToolTip(label, tooltip_text)
            else:
                # Create the widget dimensions based on calculated seat size
                width = int(seat_size / 20)  # Convert pixels to character width approximation
                height = int(seat_size / 30)  # Convert pixels to character height approximation
                
                # Ensure minimum size
                width = max(2, width)
                height = max(1, height)
                
                # Update existing widget if possible
                if existing_widget:
                    existing_widget.config(text=" ", bg=COLORS['empty_seat'], width=width, height=height,
                                          font=("Arial", font_size))
                else:
                    label = tk.Label(
                        seat_frame, 
                        text=" ", 
                        font=("Arial", font_size), 
                        width=width, 
                        height=height,
                        borderwidth=1, 
                        relief="solid", 
                        bg=COLORS['empty_seat']
                    )
                    label.grid(row=r+1, column=c+1, padx=padding, pady=padding)
                    label.bind("<Button-1>", add_seat)
                    label.bind("<Button-3>", delete_seat)
                    
                    # Add tooltips
                    tooltip_text = f"Left click to add a seat\nR{r+1}C{c+1}: Empty"
                    tooltip = ToolTip(label, tooltip_text)
    
    # Ensure row labels exist with consistent sizing
    for r in range(len(seats)):
        existing_label = None
        for widget in seat_frame.grid_slaves(row=r+1, column=0):
            existing_label = widget
            break
            
        if not existing_label:
            width = max(2, int(seat_size / 20))
            row_label = tk.Label(
                seat_frame, 
                text=f"R{r+1}", 
                font=("Arial Bold", font_size), 
                width=width, 
                anchor="center",
                bg=COLORS['header'],
                fg=COLORS['header_text']
            )
            row_label.grid(row=r+1, column=0, padx=padding, pady=padding)
        else:
            # Update existing label
            width = max(2, int(seat_size / 20))
            existing_label.config(font=("Arial Bold", font_size), width=width)
    
    # Ensure column labels exist with consistent sizing
    for c in range(len(seats[0]) if seats else 0):
        existing_label = None
        for widget in seat_frame.grid_slaves(row=0, column=c+1):
            existing_label = widget
            break
            
        if not existing_label:
            width = max(2, int(seat_size / 20))
            col_label = tk.Label(
                seat_frame, 
                text=f"C{c+1}", 
                font=("Arial Bold", font_size), 
                width=width, 
                anchor="center",
                bg=COLORS['header'],
                fg=COLORS['header_text']
            )
            col_label.grid(row=0, column=c+1, padx=padding, pady=padding)
        else:
            # Update existing label
            width = max(2, int(seat_size / 20))
            existing_label.config(font=("Arial Bold", font_size), width=width)
    
    # Add corner label for completeness with consistent sizing
    corner_exists = False
    for widget in seat_frame.grid_slaves(row=0, column=0):
        corner_exists = True
        corner_widget = widget
        break
        
    if not corner_exists:
        width = max(2, int(seat_size / 20))
        height = max(1, int(seat_size / 30))
        corner_label = tk.Label(
            seat_frame, 
            text="", 
            font=("Arial", font_size), 
            width=width, 
            height=height,
            bg=COLORS['header']
        )
        corner_label.grid(row=0, column=0, padx=padding, pady=padding)
    else:
        # Update existing corner label
        width = max(2, int(seat_size / 20))
        height = max(1, int(seat_size / 30))
        corner_widget.config(width=width, height=height, font=("Arial", font_size))
    
    # Make sure the layout is centered
    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Center the view to the middle of the canvas
    canvas.xview_moveto(0.5 - (inner_frame.winfo_width() / 2 / canvas.winfo_width()))
    canvas.yview_moveto(0.5 - (inner_frame.winfo_height() / 2 / canvas.winfo_height()))

# Initialize layout creation
def initialize_layout():
    global seats, layout_name

    new_layout_window = tk.Toplevel(root)
    new_layout_window.title("New Layout")
    new_layout_window.geometry("400x300")
    new_layout_window.configure(bg=COLORS['background'])
    new_layout_window.transient(root)
    new_layout_window.grab_set()

    # Center the window on the screen
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    new_layout_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(new_layout_window, text="Select rows:", font=("Arial", 12), bg=COLORS['background']).pack(pady=10)
    rows_slider = tk.Scale(
        new_layout_window, 
        from_=1, 
        to=20, 
        orient=tk.HORIZONTAL, 
        length=300, 
        bg=COLORS['background'],
        troughcolor=COLORS['empty_seat'],
        font=("Arial", 10)
    )
    rows_slider.pack()

    tk.Label(new_layout_window, text="Select columns:", font=("Arial", 12), bg=COLORS['background']).pack(pady=10)
    cols_slider = tk.Scale(
        new_layout_window, 
        from_=1, 
        to=20, 
        orient=tk.HORIZONTAL, 
        length=300,
        bg=COLORS['background'],
        troughcolor=COLORS['empty_seat'],
        font=("Arial", 10)
    )
    cols_slider.pack()

    seat_count_label = tk.Label(
        new_layout_window, 
        text="Total Seats: 0", 
        font=("Arial", 12, "bold"),
        bg=COLORS['background']
    )
    seat_count_label.pack(pady=10)

    def update_seat_count(event):
        rows = rows_slider.get()
        cols = cols_slider.get()
        total_seats = rows * cols
        seat_count_label.config(text=f"Total Seats: {total_seats}")

    rows_slider.bind("<Motion>", update_seat_count)
    cols_slider.bind("<Motion>", update_seat_count)

    def confirm_new_layout():
        global seats
        rows = rows_slider.get()
        cols = cols_slider.get()
        if rows > 0 and cols > 0:
            seats = [[None for _ in range(cols)] for _ in range(rows)]
            refresh_layout()
            loaded_layout_label.config(text="New Layout")
            status_label.config(text=f"Status: Created new layout with {rows} rows and {cols} columns")
            new_layout_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid layout dimensions!")

    create_button = tk.Button(
        new_layout_window, 
        text="Create Layout", 
        command=confirm_new_layout,
        bg=COLORS['button'],
        fg=COLORS['button_text'],
        font=("Arial", 12),
        relief="flat",
        padx=20
    )
    create_button.pack(pady=15)

# Simple tooltip implementation
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip, 
            text=self.text, 
            bg="#ffffcc", 
            relief="solid", 
            borderwidth=1,
            font=("Arial", 9),
            padx=5,
            pady=2
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# Initialize tkinter
root = tk.Tk()
root.title("Cinema Seat Layout Manager")
root.state('zoomed')  # Full window mode
root.configure(bg=COLORS['background'])

# Create a header frame
header_frame = tk.Frame(root, bg=COLORS['header'], height=60)
header_frame.pack(side=tk.TOP, fill=tk.X)

# Add title
tk.Label(
    header_frame, 
    text="Cinema Seat Layout Designer", 
    font=("Arial", 18, "bold"), 
    bg=COLORS['header'], 
    fg=COLORS['header_text']
).pack(side=tk.LEFT, padx=20, pady=10)

# Create a container frame for the main content
main_container = tk.Frame(root, bg=COLORS['background'])
main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)

# Create a frame for the top label (to display layout name)
top_frame = tk.Frame(main_container, bg=COLORS['background'])
top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

# Center-align the label within the frame
loaded_layout_label = tk.Label(
    top_frame, 
    text="No Layout Loaded", 
    font=("Arial", 14, "bold"), 
    bg=COLORS['background']
)
loaded_layout_label.pack()

# Create a central area frame
central_area = tk.Frame(main_container, bg=COLORS['background'])
central_area.pack(fill=tk.BOTH, expand=True)

# Create a frame for the grid layout - positioned in center
layout_frame = tk.Frame(central_area, bg=COLORS['background'])
layout_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

# Create a canvas to hold the layout
canvas = tk.Canvas(layout_frame, highlightthickness=0, bg=COLORS['background'])
canvas.pack(side="left", expand=True, fill="both")

# Create a frame inside the canvas to hold the seat layout
inner_frame = tk.Frame(canvas, bg=COLORS['background'])
canvas_window = canvas.create_window((canvas.winfo_reqwidth()/2, canvas.winfo_reqheight()/2), 
                                   window=inner_frame, anchor="center")

# Update window size when canvas size changes
def on_canvas_configure(event):
    # Update the inner frame position to center it
    canvas.coords(canvas_window, event.width/2, event.height/2)
    # If seats are loaded, refresh the layout to adapt to new size
    if seats and len(seats) > 0:
        refresh_layout()

canvas.bind("<Configure>", on_canvas_configure)

# Create a frame for the buttons
buttons_frame = tk.Frame(central_area, bg=COLORS['background'], width=200)
buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=10)

# Add a legend for seat types
legend_frame = tk.LabelFrame(buttons_frame, text="Seat Legend", bg=COLORS['background'], font=("Arial", 12))
legend_frame.pack(fill=tk.X, pady=10)

# Add legend items
low_frame = tk.Frame(legend_frame, bg=COLORS['background'])
low_frame.pack(anchor="w", pady=5)
tk.Label(low_frame, text="○", font=("Arial", 12, "bold"), bg=COLORS['low_seat'], width=2, relief="solid").pack(side=tk.LEFT, padx=5)
tk.Label(low_frame, text="Low", font=("Arial", 10), bg=COLORS['background']).pack(side=tk.LEFT, padx=5)

upper_frame = tk.Frame(legend_frame, bg=COLORS['background'])
upper_frame.pack(anchor="w", pady=5)
tk.Label(upper_frame, text="■", font=("Arial", 12, "bold"), bg=COLORS['upper_seat'], width=2, relief="solid").pack(side=tk.LEFT, padx=5)
tk.Label(upper_frame, text="Upper", font=("Arial", 10), bg=COLORS['background']).pack(side=tk.LEFT, padx=5)

vip_frame = tk.Frame(legend_frame, bg=COLORS['background'])
vip_frame.pack(anchor="w", pady=5)
tk.Label(vip_frame, text="▲", font=("Arial", 12, "bold"), bg=COLORS['vip_seat'], width=2, relief="solid").pack(side=tk.LEFT, padx=5)
tk.Label(vip_frame, text="VIP", font=("Arial", 10), bg=COLORS['background']).pack(side=tk.LEFT, padx=5)

# Add control buttons with better styling
tk.Label(buttons_frame, text="Layout Controls", font=("Arial", 12, "bold"), bg=COLORS['background']).pack(pady=15)

new_button = tk.Button(
    buttons_frame, 
    text="New Layout", 
    command=initialize_layout, 
    font=("Arial", 12),
    bg=COLORS['button'],
    fg=COLORS['button_text'],
    relief="flat",
    width=15
)
new_button.pack(pady=10)

save_button = tk.Button(
    buttons_frame, 
    text="Save Layout", 
    command=save_layout, 
    font=("Arial", 12),
    bg=COLORS['button'],
    fg=COLORS['button_text'],
    relief="flat",
    width=15
)
save_button.pack(pady=10)

load_button = tk.Button(
    buttons_frame, 
    text="Load Layout", 
    command=load_layout, 
    font=("Arial", 12),
    bg=COLORS['button'],
    fg=COLORS['button_text'],
    relief="flat",
    width=15
)
load_button.pack(pady=10)

# Add a separator line after the existing buttons
separator = tk.Frame(buttons_frame, height=2, bg=COLORS['seat_border'])
separator.pack(fill=tk.X, pady=15)

# Add back button
back_button = tk.Button(
    buttons_frame, 
    text="Back to Manager", 
    command=root.destroy,  # Simply close this window to return to manager
    font=("Arial", 12),
    bg="#e74c3c",  # Red color to distinguish it
    fg="white",
    relief="flat",
    width=15
)
back_button.pack(pady=10)

# Add instructions
instructions = tk.Label(
    buttons_frame,
    text="Instructions:\n\n• Left-click on a seat to add/change\n• Right-click to remove a seat\n• Save your layout when finished",
    justify=tk.LEFT,
    bg=COLORS['background'],
    font=("Arial", 10),
    anchor="w"
)
instructions.pack(side=tk.BOTTOM, pady=20, fill=tk.X)

# Add a status bar at the bottom
status_frame = tk.Frame(root, bg=COLORS['header'], height=30)
status_frame.pack(side=tk.BOTTOM, fill=tk.X)
status_label = tk.Label(
    status_frame, 
    text="Status: Ready", 
    font=("Arial", 10), 
    bg=COLORS['header'], 
    fg=COLORS['header_text'],
    anchor="w"
)
status_label.pack(side=tk.LEFT, padx=10, pady=5)

# Initialize variables
seats = []
layout_name = None

root.mainloop()
