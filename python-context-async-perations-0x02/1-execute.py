ChatGPT said:

Here’s the full solution for Task 2: Reusable Query Context Manager ✅

📄 2-execute_query.py
import sqlite3
from datetime import datetime


class ExecuteQuery:
    """
    Custom context manager to handle DB connection and execute a given query.
    - Accepts query string and parameters.
    - Executes query inside __enter__ and returns results.
    - Closes connection automatically in __exit__.
    """

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Executing query: {self.query} {self.params}")
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Transaction committed.")
        else:
            self.conn.rollback()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Transaction rolled back. Error: {exc_val}")
        self.conn.close()
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Connection closed.")
        return False  # Propagate exceptions if any


# ---- Example usage ----
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery("users.db", query, params) as results:
        print("Users older than 25:", results)
