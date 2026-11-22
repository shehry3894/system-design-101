# I: Interface Segregation. Don't force a class to depend on methods it does not use.
# Use when: classes implement methods only to raise NotImplementedError.
# Source: https://en.wikipedia.org/wiki/Interface_segregation_principle
from abc import ABC, abstractmethod


# Bad: one big interface. A simple printer must still "implement" scan and fax.
class MachineBad(ABC):
    @abstractmethod
    def print(self, doc): ...

    @abstractmethod
    def scan(self): ...

    @abstractmethod
    def fax(self, number): ...


# Good: small interfaces. Each class picks only what it really does.
class Printer(ABC):
    @abstractmethod
    def print(self, doc): ...


class Scanner(ABC):
    @abstractmethod
    def scan(self): ...


class SimplePrinter(Printer):
    def print(self, doc):
        return f"printed {doc}"


class OfficeMachine(Printer, Scanner):
    def print(self, doc):
        return f"printed {doc}"

    def scan(self):
        return "scanned"


assert SimplePrinter().print("invoice") == "printed invoice"
assert not hasattr(SimplePrinter(), "scan")  # no fake method to call by mistake
print(OfficeMachine().scan())
