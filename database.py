import sqlite3

def get_db_connection():
    conn = sqlite3.connect("semrush_data.db")  # SQLite database file
    conn.row_factory = sqlite3.Row  # Allows access by column name
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            ranking INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
