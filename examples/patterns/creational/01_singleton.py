# Singleton: a class with exactly one instance and one global access point.
# Use when: one shared thing must exist once (a config, a connection pool).
# Source: https://www.gofpattern.com/creational/patterns/singleton-pattern.php
# Python note: a module is already a singleton. Importing it twice gives the same object.
from threading import Lock


class ConnectionPool:
    _instance = None
    _lock = Lock()  # two threads calling at the same moment must not create two pools

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # check again: another thread may have won the race
                    cls._instance = super().__new__(cls)
        return cls._instance


a = ConnectionPool()
b = ConnectionPool()
print("same object:", a is b)
assert a is b
