# prototype.py
# Intent: Create new objects by cloning an existing object (instead of instantiating a new one from scratch).
# Focus: Copying existing objects efficiently, especially when creating them is expensive (complex setup, DB calls).
# Granularity: Works at the object level — you already have one “prototype” instance, and you duplicate it

from abc import ABC, abstractmethod
import copy

# --- Prototype Interface ---
class Prototype(ABC):
    @abstractmethod
    def clone(self) -> "Prototype":
        pass


# --- Abstract Products ---
class Button(Prototype, ABC):
    def __init__(self, label: str, color: str):
        self.label = label
        self.color = color

    @abstractmethod
    def render(self) -> None:
        pass


class Checkbox(Prototype, ABC):
    def __init__(self, checked: bool = False):
        self.checked = checked

    @abstractmethod
    def render(self) -> None:
        pass


# --- Concrete Products (Windows family) ---
class WindowsButton(Button):
    def render(self):
        print(f"Windows Button [{self.label}] with color {self.color}")

    def clone(self) -> "WindowsButton":
        return copy.deepcopy(self)


class WindowsCheckbox(Checkbox):
    def render(self):
        print(f"Windows Checkbox [{'X' if self.checked else ' '}]")

    def clone(self) -> "WindowsCheckbox":
        return copy.deepcopy(self)


# --- Concrete Products (Mac family) ---
class MacButton(Button):
    def render(self):
        print(f"Mac Button [{self.label}] with color {self.color}")

    def clone(self) -> "MacButton":
        return copy.deepcopy(self)


class MacCheckbox(Checkbox):
    def render(self):
        print(f"Mac Checkbox [{'✔' if self.checked else '✘'}]")

    def clone(self) -> "MacCheckbox":
        return copy.deepcopy(self)


# --- Client Code ---
if __name__ == "__main__":
    # Create original prototypes
    win_button_proto = WindowsButton(label="OK", color="blue")
    mac_checkbox_proto = MacCheckbox(checked=True)

    # Clone them to create variations
    win_button_clone = win_button_proto.clone()
    win_button_clone.label = "Cancel"  # modify clone
    win_button_clone.color = "red"

    mac_checkbox_clone = mac_checkbox_proto.clone()
    mac_checkbox_clone.checked = False

    print("Original Prototypes:")
    win_button_proto.render()
    mac_checkbox_proto.render()

    print("\nCloned & Modified:")
    win_button_clone.render()
    mac_checkbox_clone.render()


# --------------------------------------------------------
# Key Benefits Shown in This Example
# --------------------------------------------------------
# 1. Efficient Object Creation:
#    Instead of instantiating and configuring a new button/checkbox from scratch,
#    you can quickly clone an existing prototype.
#
# 2. Decoupling from Concrete Classes:
#    The client only calls .clone(), not knowing or caring about whether it’s a Windows or Mac product.
#
# 3. Flexibility for Runtime Variations:
#    You can create a prototype library (predefined WindowsButton, MacCheckbox, etc.)
#    and then clone/modify them at runtime for new needs.
#
# 4. Maintainability:
#    Reduces duplication of initialization code since all common setup lives in the prototype.
