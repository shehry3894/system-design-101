# Definition: No client should be forced to depend on methods it does not use.
# Why: Prefer many small, specific interfaces over one large, bloated one

from abc import ABC, abstractmethod

# ❌ Bad: Fat interface
class Machine(ABC):
    @abstractmethod
    def print(self): pass

    @abstractmethod
    def scan(self): pass

    @abstractmethod
    def fax(self): pass

class OldPrinter(Machine):
    def print(self):
        print("Printing...")

    def scan(self):  # Not supported
        raise NotImplementedError("No scanner available")

    def fax(self):  # Not supported
        raise NotImplementedError("No fax available")

# ✅ Good: Segregated interfaces
class Printer(ABC):
    @abstractmethod
    def print(self): pass

class Scanner(ABC):
    @abstractmethod
    def scan(self): pass

class Fax(ABC):
    @abstractmethod
    def fax(self): pass

class SimplePrinter(Printer):
    def print(self):
        print("Printing only")
