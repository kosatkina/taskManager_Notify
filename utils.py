import sqlite3
import re

import sqlite3
from datetime import datetime

# Constants
DB_PATH = 'notify.db'
TITLE_LEN = 20
CONTENT_LEN = 500

# Helper function to connect to the db
def get_connection():
    try: 
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None


# Function to generate title from note's content
def get_title(content):
    
    first_line = content.strip().split("\n")[0]
    
    if not first_line:
        return "Untitled note".ljust(TITLE_LEN)
    
    stripped = first_line.strip()

    if len(stripped) > TITLE_LEN:
        return stripped[:(TITLE_LEN - 3)] + "..."
    else:
        return stripped.ljust(TITLE_LEN)
    

# Functions to validate user input
def sanitize_input(text):
    return text.strip()

def clean_content(content):
    # Limit content length in 500 characters
    return content.strip()[:CONTENT_LEN]

def escape_like(value):
    # Escape wildcard characters in LIKE query
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")