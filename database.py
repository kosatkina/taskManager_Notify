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
        title = get_title(content)

    # ToDo -- Add validation

    # Insert record into note_list
    cursor.execute("INSERT INTO note_list (title, date_created) VALUES (?, ?)", (title, dt))
    id = cursor.lastrowid

    # Insert into note
    cursor.execute("INSERT INTO note (id, content) VALUES (?, ?)", (id, content))

    conn.commit()
    print(f"Added new note '{title}'")


# Function to generate note's title
def get_title(content):
    if not content or content.strip() == "":
        return "(Untitled Note)"
    
    strippedTitle = content.strip()

    if len(strippedTitle) > TITLE_LEN:
        return strippedTitle[:(TITLE_LEN - 3)] + "..."
    else:
        return strippedTitle
    

# Function to read records from database
def read_notes():

    cursor.execute("""SELECT id, title, date_created 
                   FROM note_list 
                   ORDER BY date_created DESC
        """)
    notes = cursor.fetchall()

    if not notes:
        print("No notes found...")
    else:
        for note in notes:
            print(f"{note[0]} - {note[1]} (Created: {note[2]})")


# Function to search note by title
def search_note(word_to_search):

    search_pattern = f"%{word_to_search}%"
    cursor.execute("SELECT * FROM note_list WHERE title LIKE ?", (search_pattern,))
    notes = cursor.fetchall()

    # ToDo -- Add validation

    if not notes:
        print("No notes found...")
    else:
        print("Search Results: ")
        for note in notes:
            print(f"{note[0]} - {note[1]} (Created: {note[2]})")


# Function to find note by id
def find_note_by_id(id):

    cursor.execute("""SELECT note_list.id, note_list.title, note_list.date_created, note_list.date_updated 
                FROM note_list 
                JOIN note ON note_list.id = note.id
                WHERE note_list.id = ?
        """, (id,))
    
    result = cursor.fetchone()

    if result:
        print(f"{result[0]} - {result[1]} (Created: {result[2]}) (Updated: {result[3]})")
        return result
    else:
        return None


# Function to update existing note
def update_note(id, new_content):

    # Check if note exists
    note_to_update = find_note_by_id(id)
    if not note_to_update:
        return

    dt = datetime.now().strftime("%c")

    # ToDo -- Add validation

    cursor.execute("UPDATE note SET content = ? WHERE id = ?", (new_content, id))
    cursor.execute("UPDATE note_list SET date_updated = ? WHERE id = ?", (dt, id))

    conn.commit
    print(f"Note {id} updated.")


# Function to delete note
def delete_note_by_id(id):
    
    # ToDo -- Add verification

    cursor.execute("DELETE FROM note_list WHERE id = ?", (id,))
    
    conn.commit()
    print(f"Note {id} deleted.")

# Function to close connection
def close_connection():
    conn.close()
