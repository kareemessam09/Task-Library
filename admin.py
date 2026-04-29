from tkinter import *
from tkinter import messagebox, ttk
import backend
import os
import sys
import subprocess

class admin:
    def __init__(self, window):
        self.window = window
        self.window.title("Library Management - Admin Console")
        self.window.geometry("1000x650")
        self.window.configure(bg="#2c3e50")
        
        self.selected_tuple = None

        # --- Sidebar / Navigation ---
        self.sidebar = Frame(self.window, bg="#34495e", width=200, height=650)
        self.sidebar.pack(side=LEFT, fill=Y)
        
        Label(self.sidebar, text="ADMIN", fg="#ecf0f1", bg="#34495e", font=("Helvetica", 20, "bold")).pack(pady=30)
        
        btn_style = {"font": ("Helvetica", 11, "bold"), "bg": "#1abc9c", "fg": "white", "activebackground": "#16a085", "cursor": "hand2", "bd": 0, "pady": 10}
        
        Button(self.sidebar, text="View Catalog", **btn_style, command=self.view_command).pack(fill=X, padx=20, pady=5)
        Button(self.sidebar, text="Search Books", **btn_style, command=self.search_command).pack(fill=X, padx=20, pady=5)
        Button(self.sidebar, text="Clear Entry", **btn_style, command=self.clear_command).pack(fill=X, padx=20, pady=5)
        
        Frame(self.sidebar, height=30, bg="#34495e").pack()
        
        Button(self.sidebar, text="Pending Requests", **btn_style, command=self.request_view_command).pack(fill=X, padx=20, pady=5)
        Button(self.sidebar, text="Active Issues", **btn_style, command=self.issue_view_command).pack(fill=X, padx=20, pady=5)
        
        Button(self.sidebar, text="LOGOUT", font=("Helvetica", 11, "bold"), bg="#e74c3c", fg="white", bd=0, command=self.logout_command).pack(side=BOTTOM, fill=X, padx=20, pady=20)

        # --- Main Content Area ---
        self.main_area = Frame(self.window, bg="#ecf0f1", padx=30, pady=20)
        self.main_area.pack(side=RIGHT, fill=BOTH, expand=True)

        Label(self.main_area, text="Inventory Management", font=("Helvetica", 24, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(anchor=W, pady=(0, 20))

        # --- Entry Form Section ---
        self.form_frame = Frame(self.main_area, bg="white", highlightbackground="#bdc3c7", highlightthickness=1, padx=20, pady=20)
        self.form_frame.pack(fill=X)

        label_font = ("Helvetica", 10, "bold")
        entry_font = ("Helvetica", 11)
        
        # Grid for inputs
        Label(self.form_frame, text="Book Title", font=label_font, bg="white").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.title_text = StringVar()
        self.entry_title = Entry(self.form_frame, textvariable=self.title_text, font=entry_font, bd=1, relief=SOLID)
        self.entry_title.grid(row=0, column=1, sticky=EW, padx=20, pady=5)

        Label(self.form_frame, text="Author", font=label_font, bg="white").grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.author_text = StringVar()
        self.entry_author = Entry(self.form_frame, textvariable=self.author_text, font=entry_font, bd=1, relief=SOLID)
        self.entry_author.grid(row=0, column=3, sticky=EW, padx=20, pady=5)

        Label(self.form_frame, text="Year", font=label_font, bg="white").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.year_text = StringVar()
        self.entry_year = Entry(self.form_frame, textvariable=self.year_text, font=entry_font, bd=1, relief=SOLID)
        self.entry_year.grid(row=1, column=1, sticky=EW, padx=20, pady=5)

        Label(self.form_frame, text="ISBN", font=label_font, bg="white").grid(row=1, column=2, sticky=W, padx=5, pady=5)
        self.isbn_text = StringVar()
        self.entry_isbn = Entry(self.form_frame, textvariable=self.isbn_text, font=entry_font, bd=1, relief=SOLID)
        self.entry_isbn.grid(row=1, column=3, sticky=EW, padx=20, pady=5)

        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(3, weight=1)

        # Form Buttons
        self.action_frame = Frame(self.main_area, bg="#ecf0f1", pady=15)
        self.action_frame.pack(fill=X)
        
        Button(self.action_frame, text="+ Add New Book", bg="#2ecc71", fg="white", font=("Helvetica", 10, "bold"), padx=15, pady=5, bd=0, command=self.add_command).pack(side=LEFT, padx=5)
        Button(self.action_frame, text="💾 Update Selected", bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), padx=15, pady=5, bd=0, command=self.update_command).pack(side=LEFT, padx=5)
        Button(self.action_frame, text="🗑 Delete Selected", bg="#e67e22", fg="white", font=("Helvetica", 10, "bold"), padx=15, pady=5, bd=0, command=self.delete_command).pack(side=LEFT, padx=5)

        # --- Table Section ---
        self.list_frame = Frame(self.main_area, bg="white")
        self.list_frame.pack(fill=BOTH, expand=True, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ffffff", foreground="#333", rowheight=30, fieldbackground="#ffffff", font=("Helvetica", 10))
        style.map("Treeview", background=[('selected', '#3498db')])

        self.tree = ttk.Treeview(self.list_frame, columns=("ID", "Title", "Author", "Year", "ISBN"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Book Title")
        self.tree.heading("Author", text="Author Name")
        self.tree.heading("Year", text="Year")
        self.tree.heading("ISBN", text="ISBN Number")
        
        self.tree.column("ID", width=40, anchor=CENTER)
        self.tree.column("Title", width=250)
        self.tree.column("Author", width=150)
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
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in backend.view():
            self.tree.insert("", END, values=row)

    def search_command(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in backend.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.tree.insert("", END, values=row)

    def add_command(self):
        if self.title_text.get() == "":
            messagebox.showerror("Error", "Book Title is required")
            return
        backend.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.view_command()
        self.clear_command()

    def delete_command(self):
        if self.selected_tuple:
            backend.delete(self.selected_tuple[0])
            self.view_command()
            self.clear_command()
        else:
            messagebox.showwarning("Selection Error", "Please select a book from the list first")

    def update_command(self):
        if self.selected_tuple:
            backend.update(self.selected_tuple[0], self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
            self.view_command()
        else:
            messagebox.showwarning("Selection Error", "Please select a book from the list first")

    def request_view_command(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in backend.request_view():
            self.tree.insert("", END, values=row)

    def issue_view_command(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in backend.issue_view():
            self.tree.insert("", END, values=row)
