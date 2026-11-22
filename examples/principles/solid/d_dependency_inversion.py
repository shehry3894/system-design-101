# D: Dependency Inversion. Business logic depends on an interface, not on a concrete DB or API.
# Use when: you want to swap Postgres for something else, or use a fake in tests.
# Source: https://en.wikipedia.org/wiki/Dependency_inversion_principle
from abc import ABC, abstractmethod


# Bad: UserServiceBad creates Postgres itself. You can't swap it or test without it.
class PostgresDB:
    def save(self, data):
        return f"postgres saved {data}"


class UserServiceBad:
    def __init__(self):
        self.db = PostgresDB()


# Good: depend on an abstraction and receive it from outside ("dependency injection").
class Database(ABC):
    @abstractmethod
    def save(self, data) -> str: ...


class Postgres(Database):
    def save(self, data):
        return f"postgres saved {data}"


class InMemory(Database):  # a fake for tests
    def __init__(self):
        self.rows = []

    def save(self, data):
        self.rows.append(data)
        return "saved in memory"


class UserService:
    def __init__(self, db: Database):
        self.db = db

    def register(self, email):
        return self.db.save(email)


fake = InMemory()
UserService(fake).register("a@b.com")
assert fake.rows == ["a@b.com"]
print(UserService(Postgres()).register("a@b.com"))
