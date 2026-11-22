# Like Lock, but a thread can acquire it multiple times without deadlocking itself.
# Useful when the same thread calls multiple functions that all need the same lock.

from threading import RLock

lock = RLock()

def outer():
    with lock:
        print("Outer acquired lock")
        inner()

def inner():
    with lock:  # ✅ works fine (same thread can re-acquire), NOTE: without RLock, it will be a deadlock!
        print("Inner acquired lock")

outer()
