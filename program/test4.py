import tkinter as tk
from tkinter import messagebox
import json
import os
from tkinter import ttk

# Seat symbols
SEAT_SYMBOLS = {'low': '○', 'upper': '■', 'VIP': '▲'}

# Globals for quick seat adding
quick_seat_class = None
is_dragging = False
delete_mode = False

# Save layout with user-entered name
def save_layout():
    global layout_name
    save_window = tk.Toplevel(root)
    save_window.title("Save Layout")
    save_window.geometry("300x150+500+300")  # Center popup
    save_window.transient(root)
    save_window.grab_set()

    tk.Label(save_window, text="Enter layout name:", font=("Arial", 12)).pack(pady=10)
    name_entry = tk.Entry(save_window, font=("Arial", 12))
    name_entry.pack(pady=10)

    def confirm_save():
        global layout_name
        entered_name = name_entry.get().strip()
        if entered_name:
            layout_name = f"{entered_name}.json"
            with open(layout_name, 'w') as file:
                json.dump(seats, file)
            messagebox.showinfo("Save", f"Seat layout '{entered_name}' saved successfully!")
            save_window.destroy()
        else:
            messagebox.showerror("Error", "Layout name cannot be empty!")

    tk.Button(save_window, text="Save", command=confirm_save, font=("Arial", 12)).pack(pady=10)

# Load a layout from a file
def load_layout():
    global seats, layout_name
    layouts = [f[:-5] for f in os.listdir() if f.endswith('.json')]
    if not layouts:
        messagebox.showwarning("Load", "No saved layouts found!")
        return

    load_window = tk.Toplevel(root)
    load_window.title("Load Layout")
    load_window.geometry("300x150")
    load_window.transient(root)
    load_window.grab_set()

    tk.Label(load_window, text="Select a layout to load:", font=("Arial", 12)).pack(pady=10)
    selected_layout = tk.StringVar()
    dropdown = ttk.Combobox(load_window, textvariable=selected_layout, values=layouts, state="readonly", font=("Arial", 12))
    dropdown.pack(pady=10)
    dropdown.set("Choose a layout")

    def confirm_selection():
        global seats, layout_name
        layout_name = selected_layout.get()
        if layout_name and f'{layout_name}.json' in os.listdir():
            with open(f'{layout_name}.json', 'r') as file:
                seats = json.load(file)
            refresh_layout()
            messagebox.showinfo("Load", f"Layout '{layout_name}' loaded successfully!")
            load_window.destroy()
        else:
            messagebox.showerror("Error", "Please select a valid layout!")

    tk.Button(load_window, text="Load", command=confirm_selection, font=("Arial", 12)).pack(pady=10)

# Enable quick add mode
def quick_add_seat(event):
    global is_dragging, delete_mode
    if delete_mode: return  # Ignore if delete mode is enabled
    is_dragging = True
    hover_add_seat(event)

# Add seat while dragging
def hover_add_seat(event):
    global quick_seat_class
    if is_dragging and quick_seat_class:
        row = event.widget.grid_info()["row"] - 1
        col = event.widget.grid_info()["column"] - 1
        if 0 <= row < len(seats) and 0 <= col < len(seats[row]):
            seats[row][col] = quick_seat_class
            refresh_layout()

# Disable quick add mode
def stop_quick_add():
    global is_dragging
    is_dragging = False

# Enable delete mode
def delete_seat(event):
    global delete_mode
    delete_mode = True
    hover_delete_seat(event)

# Delete seat while dragging
def hover_delete_seat(event):
    global delete_mode
    if delete_mode:
        row = event.widget.grid_info()["row"] - 1
        col = event.widget.grid_info()["column"] - 1
        if 0 <= row < len(seats) and 0 <= col < len(seats[row]):
            seats[row][col] = None
            refresh_layout()

# Disable delete mode
def stop_delete_seat(event):
    global delete_mode
    delete_mode = False

# Popup to select quick seat class
def select_quick_seat_class():
    quick_window = tk.Toplevel(root)
    quick_window.geometry("300x150")
    quick_window.transient(root)
    quick_window.grab_set()
    quick_window.title("Select Seat Class")

    def set_class(seat_class):
        global quick_seat_class
        quick_seat_class = seat_class
        quick_window.destroy()

    tk.Label(quick_window, text="Select a seat class for quick add:", font=("Arial", 12)).pack(pady=10)
    tk.Button(quick_window, text="Low (○)", command=lambda: set_class('low'), font=("Arial", 12)).pack(pady=5)
    tk.Button(quick_window, text="Upper (■)", command=lambda: set_class('upper'), font=("Arial", 12)).pack(pady=5)
    tk.Button(quick_window, text="VIP (▲)", command=lambda: set_class('VIP'), font=("Arial", 12)).pack(pady=5)

# Refresh the grid layout and scale it to fit the window
# Refresh the grid layout and scale it to fit the window
def refresh_layout():
    for widget in layout_frame.winfo_children():
        widget.destroy()
    rows, cols = len(seats), len(seats[0]) if seats else 0

    # Dynamically calculate cell size based on available space
    max_width = root.winfo_width() // max(cols, 1) - 10
    max_height = root.winfo_height() // max(rows, 1) - 10
    cell_size = max(1, min(max_width, max_height, 10))  # Limit to reasonable size

    for r, row in enumerate(seats):
        for c, seat_class in enumerate(row):
            symbol = SEAT_SYMBOLS.get(seat_class, "")
            label = tk.Label(
                layout_frame,
                text=symbol,
                font=("Arial", cell_size),
                width=2,  # Fixed width to maintain proportions
                height=1,  # Fixed height for readability
                borderwidth=1,
                relief="solid",
                bg="lightgray" if not seat_class else "white"
            )
            label.grid(row=r + 1, column=c + 1, padx=2, pady=2)

            # Bind interactions for quick add and delete
            label.bind("<Button-1>", quick_add_seat)  # Start quick add
            label.bind("<B1-Motion>", hover_add_seat)  # Dragging to add
            label.bind("<ButtonRelease-1>", stop_quick_add)  # Stop quick add
            label.bind("<Button-3>", delete_seat)  # Start delete mode
            label.bind("<B3-Motion>", hover_delete_seat)  # Dragging to delete
            label.bind("<ButtonRelease-3>", stop_delete_seat)  # Stop delete mode

    # Add row and column labels
    for r in range(rows):
        tk.Label(layout_frame, text=f"R{r}", font=("Arial", 10)).grid(row=r + 1, column=0, padx=5, pady=5)
    for c in range(cols):
        tk.Label(layout_frame, text=f"C{c}", font=("Arial", 10)).grid(row=0, column=c + 1, padx=5, pady=5)
# Initialize layout creation
def initialize_layout():
    global seats, layout_name

    # Create a centered popup window for layout initialization
    new_layout_window = tk.Toplevel(root)
    new_layout_window.title("New Layout")
    new_layout_window.geometry("400x300+500+200")  # Position centrally on the screen
    new_layout_window.transient(root)
    new_layout_window.grab_set()

    # Layout name input
    tk.Label(new_layout_window, text="Enter layout name:", font=("Arial", 12)).pack(pady=10)
    name_entry = tk.Entry(new_layout_window, font=("Arial", 12))
    name_entry.pack(pady=10)

    # Row and column sliders
    tk.Label(new_layout_window, text="Select number of rows:", font=("Arial", 12)).pack(pady=10)
    rows_slider = tk.Scale(new_layout_window, from_=1, to=20, orient=tk.HORIZONTAL)
    rows_slider.pack(pady=10)

    tk.Label(new_layout_window, text="Select number of columns:", font=("Arial", 12)).pack(pady=10)
    cols_slider = tk.Scale(new_layout_window, from_=1, to=20, orient=tk.HORIZONTAL)
    cols_slider.pack(pady=10)

    # Confirm button to create the new layout
    def confirm_new_layout():
        global seats, layout_name
        layout_name = name_entry.get().strip()
        rows = rows_slider.get()
        cols = cols_slider.get()
        if layout_name and rows > 0 and cols > 0:
            seats = [[None for _ in range(cols)] for _ in range(rows)]
            refresh_layout()
            new_layout_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid layout name or dimensions!")

    tk.Button(new_layout_window, text="Create Layout", command=confirm_new_layout, font=("Arial", 12)).pack(pady=20)
# Initialize tkinter
root = tk.Tk()
root.title("Cinema Seat Layout")
root.state('zoomed')  # Set the window to start maximized

# Frames for layout and buttons
layout_frame = tk.Frame(root)
layout_frame.pack(expand=True, fill="both")

buttons_frame = tk.Frame(root)
buttons_frame.pack()

# Buttons for layout actions
tk.Button(buttons_frame, text="New Layout", command=initialize_layout, font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Save Layout", command=save_layout, font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Load Layout", command=load_layout, font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Quick Add Seat", command=select_quick_seat_class, font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Stop Quick Add", command=lambda: stop_quick_add(None), font=("Arial", 14)).pack(side=tk.LEFT, padx=10)

# Variables to store layout data
seats = []
layout_name = None

# Run the tkinter main loop
root.mainloop()
