import sqlite3

def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE if NOT exists book(id INTEGER PRIMARY KEY, title text, author text, year INTEGER, isbn INTEGER)")
    conn.commit()
    conn.close()

def issue():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE if NOT exists issue(id INTEGER PRIMARY KEY, title text, author text, year INTEGER, isbn INTEGER)")
    conn.commit()
    conn.close()

def request():
    conn = sqlite3.connect("request.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE if NOT exists request(id INTEGER PRIMARY KEY, title text, author text, year INTEGER, isbn INTEGER)")
    conn.commit()
    conn.close()

def insert(title, author, year, isbn):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO book (title, author, year, isbn) VALUES(?,?,?,?)', (title, author, year, isbn))
    conn.commit()
    conn.close()

def request_insert(title, author, year, isbn):
    conn = sqlite3.connect('request.db')
    cur = conn.cursor()
    # Corrected: Added NULL for the PRIMARY KEY 'id' column to match the 5-column schema
    cur.execute('INSERT INTO request (id, title, author, year, isbn) VALUES(NULL,?,?,?,?)', (title, author, year, isbn))
    conn.commit()
    conn.close()

def request_view():
    conn = sqlite3.connect('request.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM request")
    rows = cur.fetchall()
    conn.close()
    return rows

def request_delete(id):
    conn = sqlite3.connect('request.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM request WHERE id=?", (id,))
    conn.commit()
    conn.close()

def issue_delete(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM issue WHERE id=?", (id,))
    conn.commit()
    conn.close()

def issue_insert(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    # Check if already issued
    cur.execute("SELECT * FROM issue WHERE id=?", (id,))
    if cur.fetchone():
        conn.close()
        return False
    # Transfer book details
    cur.execute('INSERT INTO issue (id, title, author, year, isbn) SELECT id, title, author, year, isbn FROM book WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return True

def issue_view():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM issue")
    rows = cur.fetchall()
    conn.close()
    return rows

def view():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(title="", author="", year="", isbn=""):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, title, author, year, isbn):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
    conn.commit()
    conn.close()

connect()
issue()
request()
