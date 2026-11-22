# GIL (Global Interpreter Lock): in standard CPython, one thread runs Python bytecode at a time.
# Effect: threads help with waiting (I/O). For CPU work, use processes for true parallelism.
# Docs: https://docs.python.org/3/glossary.html#term-global-interpreter-lock
# Note: Python 3.13+ has an optional free-threaded build without the GIL:
#       https://docs.python.org/3/howto/free-threading-python.html
import multiprocessing
import threading
import time


def cpu_task(n=2_000_000):  # pure computation: needs the GIL the whole time
    x = 0
    for _ in range(n):
        x += 1


def io_task():  # waiting: sleep releases the GIL
    time.sleep(0.5)


def timed(func, worker_cls, workers=4):
    start = time.perf_counter()
    jobs = [worker_cls(target=func) for _ in range(workers)]
    [j.start() for j in jobs]
    [j.join() for j in jobs]
    return time.perf_counter() - start


if __name__ == "__main__":  # required: multiprocessing child processes re-import this file
    print(f"CPU, 4 threads:   {timed(cpu_task, threading.Thread):.2f}s  (take turns)")
    print(f"CPU, 4 processes: {timed(cpu_task, multiprocessing.Process):.2f}s  (run in parallel)")
    io_threads = timed(io_task, threading.Thread)
    print(f"I/O, 4 threads:   {io_threads:.2f}s  (all wait at the same time)")
    assert io_threads < 1.0  # 4 x 0.5s waits overlap instead of adding up to 2s
