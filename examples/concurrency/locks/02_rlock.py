# RLock (re-entrant lock): the thread that holds it can take it again.
# Use when: a locked function calls another function that takes the same lock.
# Docs: https://docs.python.org/3/library/threading.html#rlock-objects
from threading import RLock

lock = RLock()  # with a plain Lock(), inner() would wait forever on its own thread: deadlock


def outer():
    with lock:
        return inner()


def inner():
    with lock:  # same thread, second acquire: allowed
        return "inner ran"


print(outer())
assert outer() == "inner ran"
