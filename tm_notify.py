import sqlite3
from datetime import datetime

# Constants
TITLE_LEN = 21

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

# CRUD operations
# Function to add a new note
def create_note(content, title=None):

    dt = datetime.now().strftime("%c")

    # Generate title
    if not title or title.strip() == "":
        strippedTitle = content.strip()
        if not strippedTitle:
            title = "(Untitled Note)"
        else:
            if len(strippedTitle) > TITLE_LEN:
                title = strippedTitle[:(TITLE_LEN - 3)] + "..."
            else:
                title = strippedTitle

    # Insert record into note_list
    cursor.execute("INSERT INTO note_list (title, date_created) VALUES (?, ?)", (title, dt))
    id = cursor.lastrowid

    # Insert into note
    cursor.execute("INSERT INTO note (id, content) VALUES (?, ?)", (id, content))

    conn.commit()
    print(f"Added new note '{title}'")



# Close connection
conn.close()
