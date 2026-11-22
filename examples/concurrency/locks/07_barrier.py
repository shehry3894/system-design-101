# Barrier: N threads wait at a point. All continue only when all N have arrived.
# Use when: work runs in phases and phase 2 needs every thread done with phase 1.
# Docs: https://docs.python.org/3/library/threading.html#barrier-objects
from threading import Barrier, Thread

N = 3
barrier = Barrier(N)  # needs exactly N threads; with fewer, wait() blocks forever
log = []


def worker(n):
    log.append(f"phase1-{n}")
    barrier.wait()
    log.append(f"phase2-{n}")


threads = [Thread(target=worker, args=(i,)) for i in range(N)]
[t.start() for t in threads]
[t.join() for t in threads]

print(log)
assert all(entry.startswith("phase1") for entry in log[:N])  # every phase 1 before any phase 2
