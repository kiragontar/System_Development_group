import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from tkinter import ttk  # For dropdown menu (combobox)

# Seat symbols
SEAT_SYMBOLS = {'low': '○', 'upper': '■', 'VIP': '▲'}

# Save and load functions
def save_layout():
    if layout_name:
        with open(f'{layout_name}.json', 'w') as file:
            json.dump(seats, file)
        messagebox.showinfo("Save", f"Seat layout '{layout_name}' saved successfully!")
    else:
        messagebox.showerror("Error", "No layout name specified!")


def load_layout():
    global seats, layout_name
    layouts = [f[:-5] for f in os.listdir() if f.endswith('.json')]  # List available layouts (remove '.json')
    if not layouts:
        messagebox.showwarning("Load", "No saved layouts found!")
        return

    # Create a new popup window for selecting layout
    load_window = tk.Toplevel(root)
    load_window.title("Select Layout")
    load_window.geometry("300x100")

    tk.Label(load_window, text="Select a layout to load:").pack(pady=5)
    selected_layout = tk.StringVar()
    dropdown = ttk.Combobox(load_window, textvariable=selected_layout, values=layouts, state="readonly")
    dropdown.pack(pady=5)
    dropdown.set("Choose a layout")  # Set default dropdown text

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


def add_seat(event):
    row = event.widget.grid_info()["row"] - 1
    col = event.widget.grid_info()["column"] - 1

    if 0 <= row < len(seats) and 0 <= col < len(seats[row]):
        # Create a popup window near the clicked cell
        button_window = tk.Toplevel(root)
        button_window.geometry(f"+{event.x_root + 50}+{event.y_root}")  # Position near the cursor
        button_window.title("Choose Seat Class")

        def select_class(seat_class):
            seats[row][col] = seat_class
            refresh_layout()
            button_window.destroy()

        # Add buttons for each seat class
        tk.Button(button_window, text="Low (○)", command=lambda: select_class('low')).pack(pady=5)
        tk.Button(button_window, text="Upper (■)", command=lambda: select_class('upper')).pack(pady=5)
        tk.Button(button_window, text="VIP (▲)", command=lambda: select_class('VIP')).pack(pady=5)

        # Close the popup if the user clicks outside
        button_window.transient(root)
        button_window.grab_set()

def delete_seat(event):
    row = event.widget.grid_info()["row"] - 1
    col = event.widget.grid_info()["column"] - 1
    if 0 <= row < len(seats) and 0 <= col < len(seats[row]):
        seats[row][col] = None
        refresh_layout()


def refresh_layout():
    for widget in layout_frame.winfo_children():
        widget.destroy()
    for r, row in enumerate(seats):
        for c, seat_class in enumerate(row):
            if seat_class:
                symbol = SEAT_SYMBOLS[seat_class]
                label = tk.Label(layout_frame, text=symbol, font=("Arial", 16), borderwidth=1, relief="solid")
                label.grid(row=r + 1, column=c + 1, padx=5, pady=5)
                label.bind("<Button-1>", add_seat)  # Left-click to add/edit seat
                label.bind("<Button-3>", delete_seat)  # Right-click to delete seat
            else:
                empty_label = tk.Label(layout_frame, text=" ", font=("Arial", 16), borderwidth=1, relief="solid", bg="lightgray")
                empty_label.grid(row=r + 1, column=c + 1, padx=5, pady=5)
                empty_label.bind("<Button-1>", add_seat)
                empty_label.bind("<Button-3>", delete_seat)
    for r in range(len(seats)):
        tk.Label(layout_frame, text=f"R{r}", font=("Arial", 12)).grid(row=r + 1, column=0)
    for c in range(len(seats[0]) if seats else 0):
        tk.Label(layout_frame, text=f"C{c}", font=("Arial", 12)).grid(row=0, column=c + 1)


def initialize_layout():
    global seats, layout_name

    # Create a new popup window for layout creation
    new_layout_window = tk.Toplevel(root)
    new_layout_window.title("New Layout")
    new_layout_window.geometry("300x200")

    # Layout name input
    tk.Label(new_layout_window, text="Enter layout name:").pack(pady=5)
    name_entry = tk.Entry(new_layout_window)
    name_entry.pack(pady=5)

    # Row slider
    tk.Label(new_layout_window, text="Select number of rows:").pack(pady=5)
    rows_slider = tk.Scale(new_layout_window, from_=1, to=20, orient=tk.HORIZONTAL)
    rows_slider.pack()

    # Column slider
    tk.Label(new_layout_window, text="Select number of columns:").pack(pady=5)
    cols_slider = tk.Scale(new_layout_window, from_=1, to=20, orient=tk.HORIZONTAL)
    cols_slider.pack()

    def confirm_new_layout():
        global seats, layout_name
        layout_name = name_entry.get()
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

# Frames
layout_frame = tk.Frame(root)
layout_frame.pack()

buttons_frame = tk.Frame(root)
buttons_frame.pack()

tk.Button(buttons_frame, text="New Layout", command=initialize_layout).pack(side=tk.LEFT, padx=5)
tk.Button(buttons_frame, text="Save Layout", command=save_layout).pack(side=tk.LEFT, padx=5)
tk.Button(buttons_frame, text="Load Layout", command=load_layout).pack(side=tk.LEFT, padx=5)

seats = []
layout_name = None

root.mainloop()
