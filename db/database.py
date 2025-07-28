import sqlite3
from db.utils import get_connection, get_title, clean_content, sanitize_input, escape_like
from datetime import datetime
from logger import logger


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
        logger.info("Database initialized successfully.")

    except sqlite3.Error as e:
        logger.exception("Error initializing the database.")
    finally:
        if conn:
            conn.close()


# Function to add a new note
def create_note(content, title=None):

    dt = datetime.now().strftime("%c")

    # Input validation
    content = clean_content(content)

    # Generate and clean title
    if not title or title.strip() == "":
        title = get_title(content)

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
        logger.info(f"Added new note '{title.strip()}' (ID: {note_id})")

        return note_id

    except sqlite3.Error as e:
        logger.exception("Error creating note.")
    finally:
        if conn:
            conn.close()


# Function to read records from database
def read_notes():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        select_query = """SELECT note_list.id, note_list.title, note_list.date_created, note_list.date_updated, note.content 
                    FROM note_list 
                    JOIN note ON note_list.id = note.id
                    ORDER BY note_list.date_created DESC
            """

        cursor.execute(select_query)
        notes = cursor.fetchall()
        
        logger.info(f"Fetched {len(notes)} notes from the database.")
        return notes
    
    except sqlite3.Error as e:
        logger.exception("Error reading notes.")
        return []

    finally:
        if conn:
            conn.close()


# Function to search note by title
def search_note(word_to_search):

    # Validate user input
    word_to_search = sanitize_input(word_to_search)
    word_to_search = escape_like(word_to_search)
    search_pattern = f"%{word_to_search}%"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        select_by_pattern_query = """SELECT note_list.id, note_list.title, note_list.date_created, note_list.date_updated, note.content 
                                    FROM note_list 
                                    JOIN note ON note_list.id = note.id
                                    WHERE note_list.title LIKE ?
                                    ORDER BY note_list.date_created DESC"""
        
        cursor.execute(select_by_pattern_query, (search_pattern,))
        notes = cursor.fetchall()

        logger.info(f"Search for '{word_to_search}' returned {len(notes)} result(s).")
        return notes

    except sqlite3.Error as e:
        logger.exception("Error searching notes.")
        return []
    finally:
        if conn:
            conn.close()


# Function to find note by id
def find_note_by_id(id):

    # Validate user input
    if not str(id).isdigit():
        print("Invalid note #")
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        select_by_id_query = """SELECT note_list.id, note_list.title, note_list.date_created, note_list.date_updated, note.content 
                    FROM note_list 
                    JOIN note ON note_list.id = note.id
                    WHERE note_list.id = ?
            """
        cursor.execute(select_by_id_query, (id,))
        
        result = cursor.fetchone()

        return result
        
    except sqlite3.Error as e:
        logger.exception(f"Error finding note ID {id}.")
        return None
    finally:
        if conn:
            conn.close()


# Function to update existing note
def update_note(id, new_content):

    if not str(id).isdigit():
        print("Invalid note #")
        return None
    
    # Check if note exists
    note_to_update = find_note_by_id(id)
    if not note_to_update:
        return

    dt = datetime.now().strftime("%c")
    new_content = clean_content(new_content)
    new_title = get_title(new_content)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        update_note_query = "UPDATE note SET content = ? WHERE id = ?"
        update_note_list_query = "UPDATE note_list SET title = ?, date_updated = ? WHERE id = ?"

        cursor.execute(update_note_query, (new_content, id))
        cursor.execute(update_note_list_query, (new_title, dt, id))

        conn.commit()
        logger.info(f"Note {id} updated to new title: {new_title}")

        return True

    except sqlite3.Error as e:
        logger.exception(f"Error updating note ID {id}.")
    finally:
        if conn:
            conn.close()


# Function to delete note
def delete_note_by_id(id):

    if not str(id).isdigit():
        print("Invalid note #")
        return None
    
    try: 
        conn = get_connection()
        cursor = conn.cursor()

        delete_note_query = "DELETE FROM note_list WHERE id = ?"
        cursor.execute(delete_note_query, (id,))
        
        conn.commit()
        logger.info(f"Note ID {id} deleted successfully.")

        return True

    except sqlite3.Error as e:
        logger.exception(f"Error deleting note ID {id}.")
    finally:
        if conn:
            conn.close()

