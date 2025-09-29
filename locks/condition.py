# Same as Semaphore, but prevents release() from increasing counter beyond its initial value.
# Good safety check against buggy code.
from threading import Condition, Thread

items = []
condition = Condition()

def producer():
    with condition:
        items.append("🍎")
        print("Produced")
        condition.notify()  # wake up one waiting consumer

def consumer():
    with condition:
        while not items:
            condition.wait()  # wait until notified
        print("Consumed:", items.pop())

Thread(target=consumer).start()
Thread(target=producer).start()
