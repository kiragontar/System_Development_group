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

# Save layout with user-entered name
def save_layout():
    global layout_name
    save_window = tk.Toplevel(root)
    save_window.title("Save Layout")
    save_window.geometry("300x100")
    save_window.transient(root)  # Keep popup on top
    save_window.grab_set()

    # Prompt for layout name
    tk.Label(save_window, text="Enter layout name:").pack(pady=5)
    name_entry = tk.Entry(save_window)
    name_entry.pack(pady=5)

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

    tk.Button(save_window, text="Save", command=confirm_save).pack(pady=5)

# Load a layout from a file
def load_layout():
    global seats, layout_name
    layouts = [f[:-5] for f in os.listdir() if f.endswith('.json')]
    if not layouts:
        messagebox.showwarning("Load", "No saved layouts found!")
        return

    load_window = tk.Toplevel(root)
    load_window.title("Load Layout")
    load_window.geometry("300x100")
    load_window.transient(root)
    load_window.grab_set()

    tk.Label(load_window, text="Select a layout to load:").pack(pady=5)
    selected_layout = tk.StringVar()
    dropdown = ttk.Combobox(load_window, textvariable=selected_layout, values=layouts, state="readonly")
    dropdown.pack(pady=5)
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

    tk.Button(load_window, text="Load", command=confirm_selection).pack(pady=5)

# Quick seat adding (hold and drag)
def quick_add_seat(event):
    global is_dragging
    is_dragging = True
    hover_add_seat(event)

def hover_add_seat(event):
    global quick_seat_class
    if is_dragging and quick_seat_class:
        row = event.widget.grid_info()["row"] - 1
        col = event.widget.grid_info()["column"] - 1
        if 0 <= row < len(seats) and 0 <= col < len(seats[row]):
            seats[row][col] = quick_seat_class
            refresh_layout()

def stop_quick_add(event):
    global is_dragging
    is_dragging = False

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

    tk.Label(quick_window, text="Select a seat class for quick add:").pack(pady=5)
    tk.Button(quick_window, text="Low (○)", command=lambda: set_class('low')).pack(pady=5)
    tk.Button(quick_window, text="Upper (■)", command=lambda: set_class('upper')).pack(pady=5)
    tk.Button(quick_window, text="VIP (▲)", command=lambda: set_class('VIP')).pack(pady=5)

# Refresh the grid layout
def refresh_layout():
    for widget in layout_frame.winfo_children():
        widget.destroy()
    for r, row in enumerate(seats):
        for c, seat_class in enumerate(row):
            if seat_class:
                symbol = SEAT_SYMBOLS[seat_class]
                label = tk.Label(layout_frame, text=symbol, font=("Arial", 20), borderwidth=1, relief="solid", width=4, height=2)
                label.grid(row=r + 1, column=c + 1, padx=5, pady=5)
                label.bind("<Button-1>", quick_add_seat)  # Start quick add on left-click
                label.bind("<B1-Motion>", hover_add_seat)  # Dragging
                label.bind("<ButtonRelease-1>", stop_quick_add)  # Stop quick add
            else:
                empty_label = tk.Label(layout_frame, text="", font=("Arial", 20), borderwidth=1, relief="solid", bg="lightgray", width=4, height=2)
                empty_label.grid(row=r + 1, column=c + 1, padx=5, pady=5)
                empty_label.bind("<Button-1>", quick_add_seat)
                empty_label.bind("<B1-Motion>", hover_add_seat)
                empty_label.bind("<ButtonRelease-1>", stop_quick_add)
    for r in range(len(seats)):
        tk.Label(layout_frame, text=f"R{r}", font=("Arial", 12)).grid(row=r + 1, column=0)
    for c in range(len(seats[0]) if seats else 0):
        tk.Label(layout_frame, text=f"C{c}", font=("Arial", 12)).grid(row=0, column=c + 1)

# Initialize layout creation
def initialize_layout():
    global seats, layout_name

    new_layout_window = tk.Toplevel(root)
    new_layout_window.title("New Layout")
    new_layout_window.geometry("300x200")
    new_layout_window.transient(root)
    new_layout_window.grab_set()

    tk.Label(new_layout_window, text="Enter layout name:").pack(pady=5)
    name_entry = tk.Entry(new_layout_window)
    name_entry.pack(pady=5)

    tk.Label(new_layout_window, text="Select rows:").pack(pady=5)
    rows_slider = tk.Scale(new_layout_window, from_=1, to=20, orient=tk.HORIZONTAL)
    rows_slider.pack()

    tk.Label(new_layout_window, text="Select columns:").pack(pady=5)
    cols_slider = tk.Scale(new_layout_window, from_=1, to=20, orient=tk.HORIZONTAL)
    cols_slider.pack()

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

    tk.Button(new_layout_window, text="Create Layout", command=confirm_new_layout).pack(pady=10)

# Initialize tkinter
root = tk.Tk()
root.title("Cinema Seat Layout")
root.state('zoomed')  # Full window mode

layout_frame = tk.Frame(root)
layout_frame.pack(expand=True)

buttons_frame = tk.Frame(root)
buttons_frame.pack()

tk.Button(buttons_frame, text="New Layout", command=initialize_layout, font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Save Layout", command=save_layout, font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Load Layout", command=load_layout, font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Quick Add Seat", command=select_quick_seat_class, font=("Arial", 14)).pack(side=tk.LEFT, padx=10)

seats = []
layout_name = None

root.mainloop()
