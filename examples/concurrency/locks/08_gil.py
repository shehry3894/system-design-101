# The Global Interpreter Lock (GIL) is a mutex (mutual exclusion lock) used in CPython (the most common Python impl).
# CPython’s memory management is not thread-safe by default.
# It ensures that only one thread executes Python bytecode at a time, even on multi-core processors.
# Only one thread can access Python objects at a time, avoiding complex race conditions.

import time
import threading
import multiprocessing


# --- CPU-bound task: Increment loop ---
def cpu_task(n=10 ** 7):
    x = 0
    for _ in range(n):
        x += 1
    return x


# --- I/O-bound task: Sleep (simulates waiting for network/file I/O) ---
def io_task(seconds=2):
    time.sleep(seconds)
    return f"Slept {seconds}s"


# --- Benchmark helper ---
def benchmark(func, executor, num_workers, label):
    start = time.time()

    if executor == "threading":
        threads = [threading.Thread(target=func) for _ in range(num_workers)]
        for t in threads: t.start()
        for t in threads: t.join()

    elif executor == "multiprocessing":
        processes = [multiprocessing.Process(target=func) for _ in range(num_workers)]
        for p in processes: p.start()
        for p in processes: p.join()

    end = time.time()
    print(f"{label} with {executor}: {end - start:.2f}s")


if __name__ == "__main__":
    workers = 4

    print("\n=== CPU-bound test ===")
    benchmark(cpu_task, "threading", workers, "CPU task")  # 0.6s, one thread executes at a time
    benchmark(cpu_task, "multiprocessing", workers, "CPU task")  # 0.3s, true parallel execution.

    print("\n=== I/O-bound test ===")
    benchmark(io_task, "threading", workers, "IO task")  # 2s, threads overlap while sleeping (releases GIL).
    benchmark(io_task, "multiprocessing", workers, "IO task")  # 2s, all processes can do parallel sleeping
