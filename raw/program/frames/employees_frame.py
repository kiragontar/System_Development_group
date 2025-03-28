import tkinter as tk

class EmployeesFrame(tk.Frame):
    """The employee list screen."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Employee List", font=("Arial", 14, "bold"))
        label.pack(pady=5)

        # Frame to hold the employee list labels
        self.employees_container = tk.Frame(self)
        self.employees_container.pack()

        # Back button
        btn_back = tk.Button(
            self,
            text="Back to Main",
            command=lambda: controller.show_frame("MainMenu")
        )
        btn_back.pack(pady=10)

        self.pack(fill="both", expand=True)  # Ensure the frame gets packed into the container

    def refresh_employee_list(self):
        # Fetch employee data
        employees = self.controller.user_service.get_all()

        # Clear the previous employee labels from the container
        for widget in self.employees_container.winfo_children():
            widget.pack_forget()

        # Display each employee in a Label
        for i in range(len(employees)):
            tk.Label(self.employees_container, text=f"{employees[i].username} {employees[i].firstname} {employees[i].lastname} (ID: {employees[i].user_id})").pack()

        
       

