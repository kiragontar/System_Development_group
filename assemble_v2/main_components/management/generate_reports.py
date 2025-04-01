import tkinter as tk
from tkinter import ttk
import json
import os

def display_json_report(filepath):
    """Displays the top-level content of a JSON file in a Tkinter Treeview with separators."""

    if not os.path.exists(filepath):
        tk.messagebox.showerror("Error", f"File not found: {filepath}")
        return

    try:
        with open(filepath, 'r') as file:
            data = json.load(file)

        report_window = tk.Toplevel()
        report_window.title("JSON Report")

        tree = ttk.Treeview(report_window, columns=("Key", "Value"), show="headings")
        tree.heading("Key", text="Key")
        tree.heading("Value", text="Value")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if isinstance(data, list):
            for item in data:
                for key, value in item.items():
                    tree.insert("", tk.END, values=(key, str(value)))
                tree.insert("", tk.END, values=("-" * 20, ""))  # Separator line
        elif isinstance(data, dict):
            for key, value in data.items():
                tree.insert("", tk.END, values=(key, str(value)))
        else:
            tree.insert("", tk.END, values=("Data", str(data)))

    except json.JSONDecodeError:
        tk.messagebox.showerror("Error", f"Invalid JSON file: {filepath}")
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() #hide the root window.
    json_file_path = "booking_events.json"
    display_json_report(json_file_path)
    root.mainloop()