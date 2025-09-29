# Synchronizes a fixed number of threads → all must reach the barrier before continuing.
from threading import Barrier, Thread

barrier = Barrier(3)

def worker(n):
    print(f"Thread {n} waiting at barrier")
    barrier.wait()
    print(f"Thread {n} passed barrier")

[Thread(target=worker, args=(i,)).start() for i in range(2)]
