# Condition: a lock + "wait until something is true". wait() sleeps, notify() wakes a waiter.
# Use when: a consumer must wait until a producer adds data (producer/consumer queue).
# Docs: https://docs.python.org/3/library/threading.html#condition-objects
from threading import Condition, Thread

items = []
consumed = []
condition = Condition()


def consumer():
    with condition:
        condition.wait_for(lambda: items)  # sleeps (lock released) until items is non-empty
        consumed.append(items.pop())


def producer():
    with condition:
        items.append("order-1")
        condition.notify()  # wake one waiting consumer


c = Thread(target=consumer)
p = Thread(target=producer)
c.start()
p.start()
c.join()
p.join()

print("consumed:", consumed)
assert consumed == ["order-1"]
