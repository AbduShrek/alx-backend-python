import sqlite3
from datetime import datetime


class DatabaseConnection:
    """
    Custom context manager for SQLite database connections.
    - __enter__: opens the connection and returns a cursor
    - __exit__: closes the connection safely (even if error occurs)
    """

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Connection opened to {self.db_name}")
        return self.cursor  # return cursor so it can be used inside 'with'

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit only if no exception occurred
        if exc_type is None:
            self.conn.commit()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Transaction committed.")
        else:
            self.conn.rollback()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Transaction rolled back. Error: {exc_val}")
        # Always close connection
        self.conn.close()
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Connection closed.")
        # Returning False will propagate exception if one occurred
        return False


# ---- Example usage ----
if __name__ == "__main__":
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Users:", results)
