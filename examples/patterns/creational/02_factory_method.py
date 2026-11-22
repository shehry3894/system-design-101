# factory.py
# Intent: Create one object, but let subclasses decide which concrete class to instantiate.
# Focus: Which product to create.
# Granularity: One product at a time.

from abc import ABC, abstractmethod


# --- Abstract Product ---
class Button(ABC):
    @abstractmethod
    def render(self) -> None:
        pass


# --- Concrete Products ---
class WindowsButton(Button):
    def render(self):
        print("Rendering a Windows-style Button")


class MacButton(Button):
    def render(self):
        print("Rendering a Mac-style Button")


# --- Factory Class ---
class ButtonFactory:
    """Factory that creates Button objects based on input type."""

    @staticmethod
    def create_button(os_type: str) -> Button:
        if os_type.lower() == "windows":
            return WindowsButton()
        elif os_type.lower() == "mac":
            return MacButton()
        else:
            raise ValueError(f"Unknown OS type: {os_type}")


# --- Client Code ---
if __name__ == "__main__":
    # Client asks factory for buttons
    button1 = ButtonFactory.create_button("windows")
    button1.render()

    button2 = ButtonFactory.create_button("mac")
    button2.render()

# --------------------------------------------------------
# Key Benefits Shown in This Example
# --------------------------------------------------------
# 1. Decoupling:
#    The client code only depends on the Button interface and the factory.
#    It does not need to import or know about WindowsButton or MacButton directly.
#
# 2. Centralized Object Creation Logic:
#    If you want to add a new type of button (e.g., LinuxButton), you only
#    add the new class and extend the factory method. The client code remains unchanged.
#
# 3. Flexibility:
#    You could change how objects are created (e.g., caching, configuration-driven instantiation,
#    or using reflection) entirely inside the factory, and the client code would remain untouched.
#
# 4. Maintainability:
#    Object creation logic lives in one place (the factory), so it’s easier to update
#    or extend without touching multiple parts of the application.
