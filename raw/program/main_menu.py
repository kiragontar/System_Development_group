import tkinter as tk

def show_frame(frame):
    """Raise the selected frame to the front."""
    frame.tkraise()

# Create the main window
root = tk.Tk()
root.title("Page Navigation Example")
root.geometry("400x300")  # Set the window size

# Configure the grid layout
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Create frames for two pages
frame1 = tk.Frame(root, bg="lightblue")
frame2 = tk.Frame(root, bg="lightgreen")

# Place both frames in the same grid
for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nsew")

# Add widgets to the first page
label1 = tk.Label(frame1, text="This is Page 1", bg="lightblue", font=("Arial", 16))
label1.pack(pady=50)
button1 = tk.Button(frame1, text="Go to Page 2", command=lambda: show_frame(frame2))
button1.pack()

# Add widgets to the second page
label2 = tk.Label(frame2, text="This is Page 2", bg="lightgreen", font=("Arial", 16))
label2.pack(pady=50)
button2 = tk.Button(frame2, text="Go to Page 1", command=lambda: show_frame(frame1))
button2.pack()

# Show the first page initially
show_frame(frame1)

# Start the Tkinter main event loop
root.mainloop()
