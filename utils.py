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


# Function to generate note's title
def get_title(content):
    if not content or content.strip() == "":
        return "(Untitled Note)"
    
    strippedTitle = content.strip()

    if len(strippedTitle) > TITLE_LEN:
        return strippedTitle[:(TITLE_LEN - 3)] + "..."
    else:
        return strippedTitle
    
