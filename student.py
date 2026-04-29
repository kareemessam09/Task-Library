from tkinter import *
from tkinter import messagebox, ttk
import backend
import os
import sys
import subprocess

class student:
    def __init__(self, window):
        self.window = window
        self.window.title("Library Management - Student Portal")
        self.window.geometry("1000x650")
        self.window.configure(bg="#f5f6fa") # Light Gray/White
        
        self.selected_tuple = None

        # --- Sidebar / Navigation ---
        self.sidebar = Frame(self.window, bg="#2f3640", width=200, height=650)
        self.sidebar.pack(side=LEFT, fill=Y)
        
        Label(self.sidebar, text="STUDENT", fg="#f5f6fa", bg="#2f3640", font=("Helvetica", 20, "bold")).pack(pady=30)
        
        # Navigation Buttons in Sidebar
        btn_style = {"font": ("Helvetica", 11, "bold"), "bg": "#487eb0", "fg": "white", "activebackground": "#40739e", "cursor": "hand2", "bd": 0, "pady": 12}
        
        Button(self.sidebar, text="Browse Catalog", **btn_style, command=self.view_command).pack(fill=X, padx=20, pady=5)
        Button(self.sidebar, text="Search Books", **btn_style, command=self.search_command).pack(fill=X, padx=20, pady=5)
        Button(self.sidebar, text="My Issued Books", **btn_style, command=self.view_issued_command).pack(fill=X, padx=20, pady=5)
        
        Frame(self.sidebar, height=30, bg="#2f3640").pack() # Spacer
        
        Button(self.sidebar, text="Clear Selection", font=("Helvetica", 10), bg="#7f8c8d", fg="white", bd=0, command=self.clear_command).pack(fill=X, padx=30, pady=5)
        
        # Logout at bottom
        Button(self.sidebar, text="LOGOUT", font=("Helvetica", 11, "bold"), bg="#c23616", fg="white", bd=0, command=self.logout_command).pack(side=BOTTOM, fill=X, padx=20, pady=20)

        # --- Main Content Area ---
        self.main_area = Frame(self.window, bg="#f5f6fa", padx=30, pady=20)
        self.main_area.pack(side=RIGHT, fill=BOTH, expand=True)

        # Welcome Section
        header_frame = Frame(self.main_area, bg="#f5f6fa")
        header_frame.pack(fill=X, pady=(0, 20))
        
        Label(header_frame, text="Student Library Access", font=("Helvetica", 24, "bold"), bg="#f5f6fa", fg="#2f3640").pack(side=LEFT)

        # --- Quick Info / Search Bar Section ---
        self.form_frame = Frame(self.main_area, bg="white", highlightbackground="#dcdde1", highlightthickness=1, padx=20, pady=20)
        self.form_frame.pack(fill=X)

        label_font = ("Helvetica", 9, "bold")
        entry_font = ("Helvetica", 10)
        
        # Row 1
        Label(self.form_frame, text="TITLE", font=label_font, bg="white", fg="#7f8c8d").grid(row=0, column=0, sticky=W, padx=5)
        self.title_text = StringVar()
        self.entry_title = Entry(self.form_frame, textvariable=self.title_text, font=entry_font, bd=1, relief=SOLID)
        self.entry_title.grid(row=0, column=1, sticky=EW, padx=10, pady=5)

        Label(self.form_frame, text="AUTHOR", font=label_font, bg="white", fg="#7f8c8d").grid(row=0, column=2, sticky=W, padx=5)
        self.author_text = StringVar()
        self.entry_author = Entry(self.form_frame, textvariable=self.author_text, font=entry_font, bd=1, relief=SOLID)
        self.entry_author.grid(row=0, column=3, sticky=EW, padx=10, pady=5)

        # Row 2
        Label(self.form_frame, text="YEAR", font=label_font, bg="white", fg="#7f8c8d").grid(row=1, column=0, sticky=W, padx=5)
        self.year_text = StringVar()
        self.entry_year = Entry(self.form_frame, textvariable=self.year_text, font=entry_font, bd=1, relief=SOLID)
        self.entry_year.grid(row=1, column=1, sticky=EW, padx=10, pady=5)

        Label(self.form_frame, text="ISBN", font=label_font, bg="white", fg="#7f8c8d").grid(row=1, column=2, sticky=W, padx=5)
        self.isbn_text = StringVar()
        self.entry_isbn = Entry(self.form_frame, textvariable=self.isbn_text, font=entry_font, bd=1, relief=SOLID)
        self.entry_isbn.grid(row=1, column=3, sticky=EW, padx=10, pady=5)

        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(3, weight=1)

        # Primary Action Buttons
        self.action_frame = Frame(self.main_area, bg="#f5f6fa", pady=15)
        self.action_frame.pack(fill=X)
        
        Button(self.action_frame, text="📖 Issue This Book", bg="#44bd32", fg="white", font=("Helvetica", 10, "bold"), padx=20, pady=8, bd=0, cursor="hand2", command=self.issue_command).pack(side=LEFT, padx=5)
        Button(self.action_frame, text="✉️ Request New Book", bg="#8c7ae6", fg="white", font=("Helvetica", 10, "bold"), padx=20, pady=8, bd=0, cursor="hand2", command=self.request_command).pack(side=LEFT, padx=5)

        # --- Book List Section (Styled Treeview) ---
        self.list_label = Label(self.main_area, text="Available Collection", font=("Helvetica", 14, "bold"), bg="#f5f6fa", fg="#353b48")
        self.list_label.pack(anchor=W, pady=(10, 5))

        self.list_frame = Frame(self.main_area, bg="white")
        self.list_frame.pack(fill=BOTH, expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ffffff", foreground="#2f3640", rowheight=35, fieldbackground="#ffffff", font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#dcdde1")
        style.map("Treeview", background=[('selected', '#487eb0')])

        self.tree = ttk.Treeview(self.list_frame, columns=("ID", "Title", "Author", "Year", "ISBN"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("ISBN", text="ISBN")
        
        self.tree.column("ID", width=40, anchor=CENTER)
        self.tree.column("Title", width=300)
        self.tree.column("Author", width=200)
        self.tree.column("Year", width=80, anchor=CENTER)
        self.tree.column("ISBN", width=120)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.list_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind('<<TreeviewSelect>>', self.get_selected_row)

    def logout_command(self):
        self.window.destroy()
        subprocess.Popen([sys.executable, "login_register.py"])

    def get_selected_row(self, event):
        try:
            selection = self.tree.selection()
            if not selection: return
            item = self.tree.item(selection[0])
            self.selected_tuple = item['values']
            
            # Fill entries
            self.title_text.set(self.selected_tuple[1])
            self.author_text.set(self.selected_tuple[2])
            self.year_text.set(self.selected_tuple[3])
            self.isbn_text.set(self.selected_tuple[4])
        except Exception:
            pass

    def clear_command(self):
        self.title_text.set("")
        self.author_text.set("")
        self.year_text.set("")
        self.isbn_text.set("")
        self.selected_tuple = None

    def view_command(self):
        self.list_label.config(text="Available Collection")
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in backend.view():
            self.tree.insert("", END, values=row)

    def view_issued_command(self):
        self.list_label.config(text="My Currently Issued Books")
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in backend.issue_view():
            self.tree.insert("", END, values=row)

    def search_command(self):
        self.list_label.config(text="Search Results")
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in backend.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.tree.insert("", END, values=row)

    def issue_command(self):
        if self.selected_tuple:
            success = backend.issue_insert(self.selected_tuple[0])
            if success:
                messagebox.showinfo("Success", f"'{self.selected_tuple[1]}' has been issued to your account.")
            else:
                messagebox.showerror("Error", "This book is already issued!")
        else:
            messagebox.showwarning("Selection Required", "Please select a book from the list to issue.")

    def request_command(self):
        if self.title_text.get() == "":
            messagebox.showerror("Required Information", "Please enter at least the Book Title to submit a request.")
            return
        backend.request_insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        messagebox.showinfo("Request Sent", "Your request has been submitted to the admin for review.")
        self.clear_command()
