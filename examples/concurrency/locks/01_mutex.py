# Simplest lock — only one thread can hold it at a time.
# Other threads block until the lock is released.

from threading import Lock, Thread

counter = 0
lock = Lock()


def increment():
    global counter
    for _ in range(100000):
        with lock:  # acquire() + release() automatically
            counter += 1


threads = [Thread(target=increment) for _ in range(2)]
[t.start() for t in threads]
[t.join() for t in threads]

print(counter)  # ✅ Always correct, no race condition
