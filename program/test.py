import tkinter as tk

def on_click(event): 
    """Handle square click."""
    print(f"Square at ({event.x}, {event.y}) clicked!")

screen_seat_plan = [0,1,1,1,1,2,3,2,1,3,1,0,1,4,2,1,2,3,3,3,3,3,3,3,3,4,3,2,2]
# Create the main window
root = tk.Tk()
root.title("creating layout")

# Set the window to fullscreen
root.attributes("-fullscreen", True)

# Add a canvas (for demonstration)
canvas = tk.Canvas(root, bg="grey")
canvas.pack(expand=True, fill="both")
# Draw squares
square1 = canvas.create_rectangle(50, 50, 150, 150, fill="blue", outline="")
square2 = canvas.create_rectangle(200, 50, 300, 150, fill="lightgreen", outline="")
# Draw a circle
circle = canvas.create_oval(100, 100, 200, 200, fill="yellow", outline="black")
canvas.create_text(200, 350, text="Click the Shapes!", font=("Comic Sans MS", 24, "bold"), fill="purple")

# Draw a triangle (fixed)
circle_1 = canvas.create_polygon(200, 200, 300, 400, 100, 400, fill="green", outline="black")

# Bind click events directly to the squares
canvas.tag_bind(square1, "<Button-1>", lambda event: on_click(event))
canvas.tag_bind(square2, "<Button-1>", lambda event: on_click(event))
canvas.tag_bind(circle_1, "<Button-1>", lambda event: on_click(event))

# Quit fullscreen with the "Escape" key
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)  # Bind "Escape" to exit fullscreen

# Start the Tkinter main event loop
root.mainloop()




seats = [] 
def delete_a_seat():
    return
def add_a_seat():
    return
def create_screen_seat_layout():
    return
def add_a_row():

    return

def creationg_layout():
    return