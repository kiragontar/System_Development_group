
import tkinter as tk

def on_click(event):
    """Handle shape click and toggle its color between green and red."""
    clicked_shape = canvas.find_closest(event.x, event.y)  # Get the closest shape
    tags = canvas.gettags(clicked_shape)  # Retrieve tags associated with the shape
    if "shape" in tags:  # Ensure the clicked item is a shape
        current_color = canvas.itemcget(clicked_shape, "fill")  # Get current fill color
        new_color = "red" if current_color == "green" else "green"  # Toggle color
        canvas.itemconfig(clicked_shape, fill=new_color)

# Input: Number list (first digit = shape, second digit = color)
screen_seat_plan = [0, 11, 11, 10, 10, 20, 30, 20, 11, 31, 10, 00, 10, 4, 21, 11, 21, 31, 31, 31, 31, 30, 30, 30, 30, 4, 30, 20, 20]

# Create the main window
root = tk.Tk()
root.title("Dynamic Shapes with Empty Spaces")

# Set the window to fullscreen
root.attributes("-fullscreen", True)

# Add a canvas
canvas = tk.Canvas(root, bg="grey")
canvas.pack(expand=True, fill="both")

# Variables to control layout
shape_size = 40  # Size of each shape
padding = 10  # Space between shapes
x_start = 50  # Starting x-coordinate
y_start = 50  # Starting y-coordinate
current_x = x_start
current_y = y_start

# Function to draw a triangle
def create_triangle(x1, y1, x2, y2, x3, y3, color):
    return canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline="black", tags=("shape",))

# Loop through the number list and draw shapes
for num in screen_seat_plan:
    if num == 0:
        # Skip empty spaces
        current_x += shape_size + padding
    elif num == 4:
        # Move to the next line
        current_x = x_start
        current_y += shape_size + padding
    else:
        first_digit = num // 10  # Determine the shape
        second_digit = num % 10  # Determine the color

        # Assign color based on second digit
        color = "green" if second_digit == 0 else "red"

        if first_digit == 1:
            # Draw a circle
            shape = canvas.create_oval(
                current_x, current_y,
                current_x + shape_size, current_y + shape_size,
                fill=color, outline="black", tags=("shape",)
            )
        elif first_digit == 2:
            # Draw a square
            shape = canvas.create_rectangle(
                current_x, current_y,
                current_x + shape_size, current_y + shape_size,
                fill=color, outline="black", tags=("shape",)
            )
        elif first_digit == 3:
            # Draw a triangle
            shape = create_triangle(
                current_x, current_y + shape_size,
                current_x + shape_size / 2, current_y,
                current_x + shape_size, current_y + shape_size,
                color
            )
        else:
            # Unknown digit: Skip this entry
            continue

        # Bind click event to change color
        canvas.tag_bind(shape, "<Button-1>", on_click)

        # Update position
        current_x += shape_size + padding

# Quit fullscreen with the "Escape" key
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)  # Bind "Escape" to exit fullscreen

# Start the Tkinter main event loop
root.mainloop()
