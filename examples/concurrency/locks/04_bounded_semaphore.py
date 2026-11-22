from threading import BoundedSemaphore, Thread
import time

# Allow max 2 threads at the same time
bounded_sem = BoundedSemaphore(2)


def worker(n):
    print(f"{n + 1} is trying to acquire...")
    bounded_sem.acquire()
    print(f"{n + 1} acquired semaphore")

    time.sleep(1)

    bounded_sem.release()
    print(f"{n + 1} released semaphore")
    try:
        bounded_sem.release() # ❌ Raises ValueError
    except ValueError:
        print('ERROR: releasing a released lock!') # catching this error will cause more errors for other threads


threads = [Thread(target=worker, args=(i,)) for i in range(5)]
[t.start() for t in threads]
[t.join() for t in threads]
