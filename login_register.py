from tkinter import *
from tkinter import messagebox, ttk
import login_backend
import os
import sys
import subprocess

class LoginApp:
    def __init__(self, window):
        self.window = window
        self.window.title('Library Management - Portal Access')
        self.window.geometry('800x550')
        self.window.configure(bg="#f0f2f5") # Light grayish blue
        self.role = "Admin"

        # Center the window on screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (550 // 2)
        self.window.geometry(f'800x550+{x}+{y}')

        self.main_container = Frame(self.window, bg="#f0f2f5")
        self.main_container.pack(fill=BOTH, expand=True)

        self.show_login_ui()

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_login_ui(self):
        self.clear_container()
        
        # Left Side: Branding / Welcome
        self.left_panel = Frame(self.main_container, bg="#2c3e50", width=350)
        self.left_panel.pack(side=LEFT, fill=Y)
        
        Label(self.left_panel, text="WELCOME", fg="#ecf0f1", bg="#2c3e50", font=("Helvetica", 28, "bold")).place(relx=0.5, rely=0.3, anchor=CENTER)
        Label(self.left_panel, text="Library Management\nSystem", fg="#bdc3c7", bg="#2c3e50", font=("Helvetica", 14), justify=CENTER).place(relx=0.5, rely=0.45, anchor=CENTER)
        Label(self.left_panel, text="Access your portal to\nmanage books and records.", fg="#95a5a6", bg="#2c3e50", font=("Helvetica", 10)).place(relx=0.5, rely=0.8, anchor=CENTER)

        # Right Side: Login Form
        self.right_panel = Frame(self.main_container, bg="white", padx=50)
        self.right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

        # Role Selector
        role_frame = Frame(self.right_panel, bg="white", pady=20)
        role_frame.pack(fill=X)
        
        self.role_admin_btn = Button(role_frame, text="Admin", font=("Helvetica", 10, "bold"), bd=0, bg="#ecf0f1", fg="#7f8c8d", padx=20, pady=5, cursor="hand2", command=lambda: self.switch_role("Admin"))
        self.role_admin_btn.pack(side=LEFT, padx=(0, 5))
        
        self.role_student_btn = Button(role_frame, text="Student", font=("Helvetica", 10, "bold"), bd=0, bg="#ecf0f1", fg="#7f8c8d", padx=20, pady=5, cursor="hand2", command=lambda: self.switch_role("Student"))
        self.role_student_btn.pack(side=LEFT)

        Label(self.right_panel, text="Sign In", font=("Helvetica", 24, "bold"), bg="white", fg="#2c3e50").pack(anchor=W, pady=(10, 30))

        # Input Fields
        Label(self.right_panel, text="USERNAME", font=("Helvetica", 9, "bold"), bg="white", fg="#95a5a6").pack(anchor=W)
        self.username_var = StringVar()
        self.username_entry = Entry(self.right_panel, textvariable=self.username_var, font=("Helvetica", 12), bd=0, highlightthickness=1, highlightbackground="#dcdde1")
        self.username_entry.pack(fill=X, pady=(5, 20), ipady=8)

        Label(self.right_panel, text="PASSWORD", font=("Helvetica", 9, "bold"), bg="white", fg="#95a5a6").pack(anchor=W)
        self.password_var = StringVar()
        self.password_entry = Entry(self.right_panel, textvariable=self.password_var, font=("Helvetica", 12), bd=0, highlightthickness=1, highlightbackground="#dcdde1", show="•")
        self.password_entry.pack(fill=X, pady=(5, 30), ipady=8)

        # Submit Button
        self.login_btn = Button(self.right_panel, text="SIGN IN", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", bd=0, pady=10, cursor="hand2", command=self.handle_login)
        self.login_btn.pack(fill=X)

        # Sign Up Link (for students)
        self.signup_container = Frame(self.right_panel, bg="white", pady=20)
        self.signup_container.pack(fill=X)
        
        self.signup_label = Label(self.signup_container, text="Don't have an account?", font=("Helvetica", 10), bg="white", fg="#7f8c8d")
        self.signup_link = Button(self.signup_container, text="Register Now", font=("Helvetica", 10, "bold"), bd=0, bg="white", fg="#3498db", cursor="hand2", command=self.show_signup_ui)
        
        self.switch_role(self.role)

    def switch_role(self, role):
        self.role = role
        if role == "Admin":
            self.role_admin_btn.config(bg="#3498db", fg="white")
            self.role_student_btn.config(bg="#ecf0f1", fg="#7f8c8d")
            self.signup_label.pack_forget()
            self.signup_link.pack_forget()
        else:
            self.role_admin_btn.config(bg="#ecf0f1", fg="#7f8c8d")
            self.role_student_btn.config(bg="#3498db", fg="white")
            self.signup_label.pack(side=LEFT)
            self.signup_link.pack(side=LEFT, padx=5)

    def show_signup_ui(self):
        self.clear_container()
        
        self.left_panel = Frame(self.main_container, bg="#1abc9c", width=350)
        self.left_panel.pack(side=LEFT, fill=Y)
        Label(self.left_panel, text="JOIN US", fg="white", bg="#1abc9c", font=("Helvetica", 28, "bold")).place(relx=0.5, rely=0.3, anchor=CENTER)
        Label(self.left_panel, text="Create a student account\nto browse and issue books.", fg="#e8f8f5", bg="#1abc9c", font=("Helvetica", 12), justify=CENTER).place(relx=0.5, rely=0.45, anchor=CENTER)

        self.right_panel = Frame(self.main_container, bg="white", padx=50, pady=40)
        self.right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

        Label(self.right_panel, text="Register", font=("Helvetica", 24, "bold"), bg="white", fg="#2c3e50").pack(anchor=W, pady=(0, 20))

        # Form Fields
        fields = [("FULL NAME", "reg_name", False), ("ROLL NO / ID", "reg_id", False), ("PASSWORD", "reg_pass1", True), ("CONFIRM PASSWORD", "reg_pass2", True)]
        self.reg_vars = {}

        for label, var_name, is_pass in fields:
            Label(self.right_panel, text=label, font=("Helvetica", 8, "bold"), bg="white", fg="#95a5a6").pack(anchor=W)
            self.reg_vars[var_name] = StringVar()
            entry = Entry(self.right_panel, textvariable=self.reg_vars[var_name], font=("Helvetica", 11), bd=0, highlightthickness=1, highlightbackground="#dcdde1", show="•" if is_pass else "")
            entry.pack(fill=X, pady=(2, 12), ipady=5)

        Button(self.right_panel, text="CREATE ACCOUNT", font=("Helvetica", 12, "bold"), bg="#1abc9c", fg="white", bd=0, pady=10, cursor="hand2", command=self.handle_signup).pack(fill=X, pady=(10, 10))
        Button(self.right_panel, text="← BACK TO LOGIN", font=("Helvetica", 9, "bold"), bg="white", fg="#7f8c8d", bd=0, cursor="hand2", command=self.show_login_ui).pack()

    def handle_login(self):
        user = self.username_var.get()
        pwd = self.password_var.get()
        if not user or not pwd:
            messagebox.showerror("Error", "Please enter your credentials")
            return
        
        if self.role == "Admin":
            login_backend.check(user, pwd, self.window)
        else:
            login_backend.checks(user, pwd, self.window)

    def handle_signup(self):
        name = self.reg_vars["reg_name"].get()
        rid = self.reg_vars["reg_id"].get()
        p1 = self.reg_vars["reg_pass1"].get()
        p2 = self.reg_vars["reg_pass2"].get()

        if not all([name, rid, p1, p2]):
            messagebox.showerror("Error", "All fields are required")
            return
        if p1 != p2:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        try:
            login_backend.insert(rid, name, p1)
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login_ui()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

if __name__ == "__main__":
    window = Tk()
    app = LoginApp(window)
    window.mainloop()
