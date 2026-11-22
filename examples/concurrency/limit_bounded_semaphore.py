# BoundedSemaphore: a Semaphore that raises an error if you release more than you acquired.
# Use when: you want a bug (an extra release) to fail loudly instead of adding a slot.
# Docs: https://docs.python.org/3/library/threading.html#threading.BoundedSemaphore
from threading import BoundedSemaphore, Semaphore

plain = Semaphore(2)
plain.release()  # bug: no matching acquire, but no error. Now 3 slots exist.

bounded = BoundedSemaphore(2)
try:
    bounded.release()  # same bug
    raised = False
except ValueError:
    raised = True

print("BoundedSemaphore caught the extra release:", raised)
assert raised
