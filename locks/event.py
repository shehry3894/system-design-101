# Simple flag that threads can wait for.
# Unlike Condition, it doesn’t need a lock.
import time
from threading import Event, Thread

event = Event()


def worker(n):
    print(f"Thread {n + 1} waiting for signal...")
    event.wait()
    print(f"Thread {n + 1} received the signal...")


threads = [Thread(target=worker, args=(i,)) for i in range(2)]
[t.start() for t in threads]
time.sleep(2)
print()
event.set()
[t.join() for t in threads]
