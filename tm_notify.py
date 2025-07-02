import sqlite3
from datetime import datetime

# Connect to SQLite DB
conn = sqlite3.connect('notify.db')

# Create a cursor to interact with DB and execute queries
cursor = conn.cursor()

# Create a NoteList table to store metadata
cursor.execute("""CREATE TABLE IF NOT EXISTS note_list (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               date_created TEXT NOT NULL,
               date_updated TEXT)
    """)

# Create a Note table to store note content 
cursor.execute("""CREATE TABLE IF NOT EXISTS note (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               content TEXT,
               FOREIGN KEY (id) REFERENCES note_list(id) ON DELETE CASCADE)
    """)

# Commit command
conn.commit()

# Close connection
conn.close()
