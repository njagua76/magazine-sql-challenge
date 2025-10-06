
import sqlite3

DB_FILE = "magazine.db"

def get_connection():
    """Return a SQLite database connection."""
    return sqlite3.connect(DB_FILE)

def create_tables():
    """Create the authors, magazines, and articles tables with constraints."""
    conn = get_connection()
    cur = conn.cursor()

    # Enable foreign key support
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        );
    """)

    conn.commit()
    conn.close()
"""this handles the db setup and connection"""