# Semaphore: a counter of free slots. acquire() takes a slot, release() gives one back.
# Use when: at most N threads may use a resource at once (e.g. N DB connections).
# Docs: https://docs.python.org/3/library/threading.html#semaphore-objects
import time
from threading import Lock, Semaphore, Thread

slots = Semaphore(3)  # 3 threads at once
inside = 0
max_inside = 0
count_lock = Lock()


def worker():
    global inside, max_inside
    with slots:  # waits here while all 3 slots are taken
        with count_lock:
            inside += 1
            max_inside = max(max_inside, inside)
        time.sleep(0.1)
        with count_lock:
            inside -= 1


threads = [Thread(target=worker) for _ in range(6)]
[t.start() for t in threads]
[t.join() for t in threads]

print("most threads inside at once:", max_inside)
assert max_inside <= 3
