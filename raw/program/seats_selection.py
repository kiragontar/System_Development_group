import tkinter as tk
from tkinter import simpledialog

# Initial screen seat plan
screen_seat_plan = [0, 11, 11, 10, 10, 20, 30, 20, 11, 31, 10, 00, 10, 4, 21, 11, 21, 31, 31, 31, 31, 30, 30, 30, 30, 4, 30, 20, 20]

# Create the main window
root = tk.Tk()
root.title("Add Seats to Screen Plan")
root.geometry("800x600")

# Canvas for displaying seats
canvas = tk.Canvas(root, bg="lightgrey")
canvas.pack(expand=True, fill="both")

# Variables to control layout
shape_size = 40  # Size of each seat
padding = 10  # Space between seats
x_start = 50  # Starting x-coordinate
y_start = 50  # Starting y-coordinate

# Function to draw a triangle
def create_triangle(x1, y1, x2, y2, x3, y3, color):
    return canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline="black", tags=("seat",))

# Function to render the screen seat plan
def render_screen_seat_plan():
    canvas.delete("seat")  # Clear existing seats
    current_x = x_start
    current_y = y_start

    for seat in screen_seat_plan:
        if seat == 0:
            # Empty space
            current_x += shape_size + padding
        elif seat == 1:
            # Circle
            canvas.create_oval(
                current_x, current_y,
                current_x + shape_size, current_y + shape_size,
                fill="green", outline="black", tags=("seat",)
            )
            current_x += shape_size + padding
        elif seat == 2:
            # Square
            canvas.create_rectangle(
                current_x, current_y,
                current_x + shape_size, current_y + shape_size,
                fill="blue", outline="black", tags=("seat",)
            )
            current_x += shape_size + padding
        elif seat == 3:
            # Triangle
            create_triangle(
                current_x, current_y + shape_size,
                current_x + shape_size / 2, current_y,
                current_x + shape_size, current_y + shape_size,
                "yellow"
            )
            current_x += shape_size + padding
        elif seat == 4:
            # Move to next row
            current_x = x_start
            current_y += shape_size + padding

# Function to add a new seat
def add_seat():
    seat_type = simpledialog.askinteger("Input", "Enter seat type (0: Empty, 1: Circle, 2: Square, 3: Triangle, 4: New Row):")
    if seat_type not in [0, 1, 2, 3, 4]:
        print("Invalid seat type!")
        return

    # Append the seat to the screen_seat_plan list
    screen_seat_plan.append(seat_type)
    print(f"Added seat type {seat_type}. Current plan: {screen_seat_plan}")

    # Re-render the screen seat plan
    render_screen_seat_plan()

# Button to add a new seat
add_seat_button = tk.Button(root, text="Add New Seat", command=add_seat)
add_seat_button.pack(side="top", pady=10)

# Render the initial screen seat plan
render_screen_seat_plan()

# Start the Tkinter main loop
root.mainloop()
