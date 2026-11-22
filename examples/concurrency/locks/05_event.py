# Event: a flag. Threads wait() until another thread calls set().
# Use when: many threads must wait for one signal (e.g. "config loaded, start working").
# Docs: https://docs.python.org/3/library/threading.html#event-objects
import time
from threading import Event, Thread

ready = Event()
started = []


def worker(n):
    ready.wait()  # blocks until ready.set()
    started.append(n)


threads = [Thread(target=worker, args=(i,)) for i in range(3)]
[t.start() for t in threads]

time.sleep(0.2)
assert started == []  # nobody started before the signal
ready.set()
[t.join() for t in threads]

print("started after signal:", sorted(started))
assert sorted(started) == [0, 1, 2]
