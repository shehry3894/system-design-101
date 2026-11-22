# Mutex (threading.Lock): only one thread can hold it at a time. Others wait.
# Use when: several threads change the same data.
# Docs: https://docs.python.org/3/library/threading.html#lock-objects
from threading import Lock, Thread

counter = 0
lock = Lock()


def increment():
    global counter
    for _ in range(100_000):
        with lock:  # acquire() ... release(), even if an error happens
            counter += 1  # read + add + write: without the lock, threads can overwrite each other


threads = [Thread(target=increment) for _ in range(2)]
[t.start() for t in threads]
[t.join() for t in threads]

print(counter)
assert counter == 200_000
