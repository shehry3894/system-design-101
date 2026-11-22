# builder.py
# Intent: Construct a complex object step by step.
# Focus: How to assemble the product.
# Granularity: Incremental construction (can skip steps, choose order).
from abc import ABC, abstractmethod

# --- Product ---
class GUIForm:
    """The complex object being built step by step."""
    def __init__(self):
        self.components = []

    def add_component(self, component: str):
        self.components.append(component)

    def show(self):
        print("Form components:")
        for comp in self.components:
            print(f" - {comp}")


# --- Abstract Builder ---
class GUIFormBuilder(ABC):
    @abstractmethod
    def add_button(self): pass

    @abstractmethod
    def add_checkbox(self): pass

    @abstractmethod
    def get_result(self) -> GUIForm: pass


# --- Concrete Builders ---
class WindowsFormBuilder(GUIFormBuilder):
    def __init__(self):
        self.form = GUIForm()

    def add_button(self):
        self.form.add_component("Windows-style Button")

    def add_checkbox(self):
        self.form.add_component("Windows-style Checkbox")

    def get_result(self) -> GUIForm:
        return self.form


class MacFormBuilder(GUIFormBuilder):
    def __init__(self):
        self.form = GUIForm()

    def add_button(self):
        self.form.add_component("Mac-style Button")

    def add_checkbox(self):
        self.form.add_component("Mac-style Checkbox")

    def get_result(self) -> GUIForm:
        return self.form


# --- Director ---
class FormDirector:
    """Controls the building process order."""
    def __init__(self, builder: GUIFormBuilder):
        self._builder = builder

    def construct_minimal_form(self):
        self._builder.add_button()

    def construct_full_form(self):
        self._builder.add_button()
        self._builder.add_checkbox()


# --- Client Code ---
if __name__ == "__main__":
    # Build a Windows Form
    win_builder = WindowsFormBuilder()
    director = FormDirector(win_builder)
    director.construct_full_form()
    form = win_builder.get_result()
    print("Windows Form:")
    form.show()

    print()

    # Build a Mac Form
    mac_builder = MacFormBuilder()
    director = FormDirector(mac_builder)
    director.construct_minimal_form()
    form = mac_builder.get_result()
    print("Mac Form:")
    form.show()



# Key Benefits Shown in This Example
# ----------------------------------
# Step-by-step construction: The form is built gradually (buttons, checkboxes, etc.),
# rather than requiring everything at once in a complex constructor.
#
# Encapsulation of construction: The logic of how a form is built (Windows vs. Mac style)
# is kept inside the builders, not in the client or the director.
#
# Decoupling: The client only depends on the Director and Builder interfaces.
# It doesn’t need to know the details of how components are added or stored.
#
# Flexibility: You can easily define different builders (e.g., WindowsFormBuilder,
# MacFormBuilder, or MobileFormBuilder) without changing the client code.
#
# Reusability: The same construction process (the Director’s algorithm) can be reused
# to build different representations of a form (Windows-style, Mac-style, etc.).
#
# Readability & Maintainability: By splitting product creation into steps,
# the code is cleaner and avoids overly long constructors or massive setup logic.