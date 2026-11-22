# Controls access to a pool of resources (not just 1 like a Mutex).
# Initialized with a counter → decremented on acquire(), incremented on release().

from threading import Semaphore, Thread
import time, random

sem = Semaphore(3)  # allow up to 3 threads at once

def worker(n):
    with sem:
        print(f"Thread {n+1} got access")
        time.sleep(random.random())
        print(f"\nThread {n+1} released")

    sem.release() # doesn't

threads = [Thread(target=worker, args=(i,)) for i in range(6)]
[t.start() for t in threads]
[t.join() for t in threads]
