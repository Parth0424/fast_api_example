# db_setup.py
import sqlite3

def create_database():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT
                )''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
