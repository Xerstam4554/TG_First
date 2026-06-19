import sqlite3


def init_db():
    """Initialize the database"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS slots (id INTEGER PRIMARY KEY, date TEXT, time TEXT, is_free True)""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY, user_id INTEGER 
    name TEXT, phone TEXT, service TEXT, date TEXT, time TEXT, status TEXT)""")
    conn.commit()
    conn.close()

with open("token.txt", "r") as f:
    TOKEN = f.read()