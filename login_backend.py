import sqlite3
from tkinter import *
from tkinter import messagebox
from admin import admin
from student import student

def connect():
    conn=sqlite3.connect("login.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE if NOT exists user(rollno INTEGER PRIMARY KEY, name text, password text)")
    cur.execute("CREATE TABLE if NOT exists admin(id INTEGER PRIMARY KEY, name text, password text)")
    # Ensure a default admin exists if the table is empty
    cur.execute("SELECT * FROM admin WHERE name='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO admin (name, password) VALUES ('admin', 'admin')")
    conn.commit()
    conn.close()

def insert(rollno,name,password):
    conn=sqlite3.connect('login.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO user VALUES(?,?,?)',(rollno,name,password))
    conn.commit()
    conn.close()

def check(name,password, login_window):
    conn=sqlite3.connect('login.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM admin WHERE name =? AND password = ?',(name,password))
    if cur.fetchone():
        login_window.destroy() # Close login window
        window = Tk()
        window.title('Admin_User')
        window.geometry('700x450')
        obj=admin(window)
        window.mainloop()
    else:
        messagebox.showinfo('error','INVALID CREDENTIALS for ADMIN LOGIN')
    conn.close()

def checks(name,password, login_window):                       # for student login
    conn=sqlite3.connect('login.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user WHERE name = ? AND password = ?', (name, password))
    if cur.fetchone():
        login_window.destroy() # Close login window
        window = Tk()
        window.title('Student_User')
        window.geometry('700x400')
        obj = student(window)
        window.mainloop()
    else:
        messagebox.showinfo('error','INVALID CREDENTIALS for STUDENT LOGIN')
    conn.close()

connect()
