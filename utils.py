import sqlite3

import sqlite3
from datetime import datetime

# Constants
TITLE_LEN = 20
DB_PATH = 'notify.db'

# Helper function to connect to the db
def get_connection():
    try: 
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None


# Function to initialize the database
def init_db():
    
    try:
        # Create DB and cursor
        conn = get_connection()
        cursor = conn.cursor()

        # Create a NoteList and Note tables to store metadata
        create_note_list_table_query = """CREATE TABLE IF NOT EXISTS note_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    date_created TEXT NOT NULL,
                    date_updated TEXT)
            """
        create_note_table_query = """CREATE TABLE IF NOT EXISTS note (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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


# Function to generate note's title
def get_title(content):
    if not content or content.strip() == "":
        return "(Untitled Note)"
    
    strippedTitle = content.strip()

    if len(strippedTitle) > TITLE_LEN:
        return strippedTitle[:(TITLE_LEN - 3)] + "..."
    else:
        return strippedTitle
    
