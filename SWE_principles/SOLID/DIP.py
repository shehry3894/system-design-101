# Definition: High-level modules ("what" of system) should not depend on low-level modules ("how" of system).
# Both should depend on abstractions.
# Why: Reduces coupling, increases flexibility and testability.
from abc import ABC, abstractmethod

# ❌ Bad: High-level directly depends on low-level
class MySQLDatabase:
    def save(self, data):
        print(f"Saving {data} to MySQL")

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # tightly coupled, creates and directly uses MySQLDatabase (low-level).

    def save_user(self, user):
        self.db.save(user)

# ✅ Good: Depend on abstraction
class Database(ABC):
    @abstractmethod
    def save(self, data): pass

class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to MySQL")

class PostgreSQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to PostgreSQL")

class UserService:
    def __init__(self, db: Database):
        self.db = db  # inject dependency

    def save_user(self, user):
        self.db.save(user)

# Usage
service = UserService(PostgreSQLDatabase())
service.save_user("Alice")
