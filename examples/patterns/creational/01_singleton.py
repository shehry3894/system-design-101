# singleton.py
# Intent: Ensure a class has only one instance, and provide a global access point to it.
# Focus: Single shared instance — avoid multiple copies of something that should be centralized.
# Granularity: Works at the class level — controls how many objects can exist.
from threading import Lock

class DatabaseConnection:
    """Singleton class for managing a single database connection."""

    _instance = None
    _lock = Lock()  # thread-safety


    def __new__(cls, db_name=":memory:"):
        # Ensure only one instance is ever created
        with cls._lock:
            if cls._instance is None:
                print("🔌 Creating new database connection...")
                cls._instance = super().__new__(cls)
                cls._instance.connection = "conn" # sqlite3.connect(db_name)
            else:
                print("♻️ Reusing existing database connection...")
        return cls._instance

    def get_connection(self):
        return self.connection


# --- Client Code ---
if __name__ == "__main__":
    # First call: creates a new connection
    db1 = DatabaseConnection("app.db")
    conn1 = db1.get_connection()

    # Second call: reuses the same connection
    db2 = DatabaseConnection("app.db")
    conn2 = db2.get_connection()

    # Verify both are the same object
    print("Same instance?", db1 is db2)          # True
    print("Same connection?", conn1 is conn2)    # True


# --------------------------------------------------------
# Key Benefits Shown in This Example
# --------------------------------------------------------
# 1. Single Shared Instance:
#    All parts of the app use the same database connection, avoiding overhead
#    of creating multiple connections.
#
# 2. Controlled Access:
#    The Singleton ensures only one object controls the resource (the DB connection).
#
# 3. Lazy Initialization:
#    The connection is created only when the DatabaseConnection is first used.
#
# 4. Thread Safety:
#    Using a lock prevents race conditions when multiple threads try to create
#    the connection at the same time.
