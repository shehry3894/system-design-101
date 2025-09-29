# abstract_factory.py
# Intent: Create families of related objects without specifying their concrete classes.
# Focus: Consistency across families (products work together).
# Granularity: Multiple products that belong to the same family.
from abc import ABC, abstractmethod

# --- Abstract Products ---
class Button(ABC):
    @abstractmethod
    def render(self) -> None:
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self) -> None:
        pass

# --- Concrete Products (Windows family) ---
class WindowsButton(Button):
    def render(self):
        print("Rendering a Windows-style Button")

class WindowsCheckbox(Checkbox):
    def render(self):
        print("Rendering a Windows-style Checkbox")

# --- Concrete Products (Mac family) ---
class MacButton(Button):
    def render(self):
        print("Rendering a Mac-style Button")

class MacCheckbox(Checkbox):
    def render(self):
        print("Rendering a Mac-style Checkbox")

# --- Abstract Factory ---
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox: pass

# --- Concrete Factories ---
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

# --- Client Code ---
def client_app(factory: GUIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    button.render()
    checkbox.render()

if __name__ == "__main__":
    print("Using Windows Factory:")
    client_app(WindowsFactory())

    print("\nUsing Mac Factory:")
    client_app(MacFactory())


# --------------------------------------------------------
# Key Benefits Shown in This Example
# --------------------------------------------------------
# 1. Consistency Across Families:
#    A factory guarantees that the client always gets a same family of products.
#    (e.g., WindowsButton pairs with WindowsCheckbox, not with a MacCheckbox).
#
# 2. Decoupling:
#    The client code depends only on abstract interfaces (Button, Checkbox, GUIFactory).
#    It has no direct knowledge of WindowsButton, MacButton, etc.
#
# 3. Extensibility:
#    Adding a new product family (e.g., LinuxFactory with LinuxButton + LinuxCheckbox)
#    requires no changes in the client code — only the new factory and product classes.
#
# 4. Single Responsibility:
#    The client focuses on using the UI elements,
#    while each factory focuses on creating the right family of products.
#
# 5. Maintainability:
#    Families of related products are created in one place (the factory),
#    ensuring easier maintenance and fewer bugs from mismatched combinations.
