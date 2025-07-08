import sqlite3
from utils import get_connection, get_title
from datetime import datetime

# Constants
TITLE_LEN = 20


# CRUD operations
# Function to initialize the database
def init_db():
    
    try:
        # Connect to the DB and create cursor
        conn = get_connection()
        cursor = conn.cursor()

        # Create a note_list and note tables to store metadata
        create_note_list_table_query = """CREATE TABLE IF NOT EXISTS note_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    date_created TEXT NOT NULL,
                    date_updated TEXT)
            """
        create_note_table_query = """CREATE TABLE IF NOT EXISTS note (
                    id INTEGER PRIMARY KEY,
                    content TEXT,
                    FOREIGN KEY (id) REFERENCES note_list(id) ON DELETE CASCADE)
            """
        cursor.execute(create_note_list_table_query) 
        cursor.execute(create_note_table_query)

        # Commit command
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error initializing the database: {e}")
    finally:
        if conn:
            conn.close()


# Function to add a new note
def create_note(content, title=None):

    dt = datetime.now().strftime("%c")

    # Generate title
    if not title or title.strip() == "":
        title = get_title(content)

    # ToDo -- Add validation

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insert record into note_list and note tables
        insert_note_query = "INSERT INTO note_list (title, date_created) VALUES (?, ?)"
        insert_note_content_query = "INSERT INTO note (id, content) VALUES (?, ?)"
        
        cursor.execute(insert_note_query, (title, dt))
        note_id = cursor.lastrowid

        cursor.execute(insert_note_content_query, (note_id, content))

        conn.commit()
        print(f"Added new note '{title}'")

    except sqlite3.Error as e:
        print(f"Error creating note: {e}")
    finally:
        if conn:
            conn.close()


# Function to read records from database
def read_notes():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        select_query = """SELECT id, title, date_created 
                    FROM note_list 
                    ORDER BY date_created DESC
            """

        cursor.execute(select_query)
        notes = cursor.fetchall()

        # Display notes if any exist
        if not notes:
            print("No notes found...")
        else:
            for note in notes:
                print(f"{note[0]} - {note[1]} (Created: {note[2]})")
    
    except sqlite3.Error as e:
        print(f"Error reading notes: {e}")
    finally:
        if conn:
            conn.close()


# Function to search note by title
def search_note(word_to_search):

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{word_to_search}%"
        select_by_pattern_query = "SELECT * FROM note_list WHERE title LIKE ?"
        
        cursor.execute(select_by_pattern_query, (search_pattern,))
        notes = cursor.fetchall()

        # ToDo -- Add validation

        if not notes:
            print("No notes found...")
        else:
            print("Search Results: ")
            for note in notes:
                print(f"{note[0]} - {note[1]} (Created: {note[2]})")

    except sqlite3.Error as e:
        print(f"Error searching notes: {e}")
    finally:
        if conn:
            conn.close()


# Function to find note by id
def find_note_by_id(id):

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        select_by_id_query = """SELECT note_list.id, note_list.title, note_list.date_created, note_list.date_updated 
                    FROM note_list 
                    JOIN note ON note_list.id = note.id
                    WHERE note_list.id = ?
            """
        cursor.execute(select_by_id_query, (id,))
        
        result = cursor.fetchone()

        if result:
            print(f"{result[0]} - {result[1]} (Created: {result[2]}) (Updated: {result[3]})")
            return result
        else:
            return None
        
    except sqlite3.Error as e:
        print(f"Error searching note by id: {e}")
        return None
    finally:
        if conn:
            conn.close()


# Function to update existing note
def update_note(id, new_content):

    # Check if note exists
    note_to_update = find_note_by_id(id)
    if not note_to_update:
        return

    dt = datetime.now().strftime("%c")
    new_title = get_title(new_content)

    # ToDo -- Add validation

    try:
        conn = get_connection()
        cursor = conn.cursor()

        update_note_query = "UPDATE note SET content = ? WHERE id = ?"
        update_note_list_query = "UPDATE note_list SET title = ?, date_updated = ? WHERE id = ?"

        cursor.execute(update_note_query, (new_content, id))
        cursor.execute(update_note_list_query, (new_title, dt, id))

        conn.commit()
        print(f"Note {id} updated.")

    except sqlite3.Error as e:
        print(f"Error updating note: {e}")
    finally:
        if conn:
            conn.close()


# Function to delete note
def delete_note_by_id(id):
    
    # ToDo -- Add verification

    try: 
        conn = get_connection()
        cursor = conn.cursor()

        delete_note_query = "DELETE FROM note_list WHERE id = ?"
        cursor.execute(delete_note_query, (id,))
        
        conn.commit()
        print(f"Note {id} deleted.")

    except sqlite3.Error as e:
        print(f"Error deleting note: {e}")
    finally:
        if conn:
            conn.close()

