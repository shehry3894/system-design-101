# Abstract Factory: one factory creates a whole family of objects that belong together.
# Use when: objects must match each other (all Mac widgets, or all Windows widgets, never mixed).
# Source: https://www.gofpattern.com/creational/patterns/abstract-factory-pattern.php
# Factory Method makes one product. Abstract Factory makes a matching set.
from abc import ABC, abstractmethod


class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: ...


class WindowsButton(Button):
    def render(self):
        return "Windows button"


class WindowsCheckbox(Checkbox):
    def render(self):
        return "Windows checkbox"


class MacButton(Button):
    def render(self):
        return "Mac button"


class MacCheckbox(Checkbox):
    def render(self):
        return "Mac checkbox"


class UIFactory(ABC):
    @abstractmethod
    def button(self) -> Button: ...

    @abstractmethod
    def checkbox(self) -> Checkbox: ...


class WindowsFactory(UIFactory):
    def button(self):
        return WindowsButton()

    def checkbox(self):
        return WindowsCheckbox()


class MacFactory(UIFactory):
    def button(self):
        return MacButton()

    def checkbox(self):
        return MacCheckbox()


def build_form(factory: UIFactory) -> list[str]:  # client knows only the abstract types
    return [factory.button().render(), factory.checkbox().render()]


print(build_form(WindowsFactory()))
print(build_form(MacFactory()))
assert build_form(MacFactory()) == ["Mac button", "Mac checkbox"]
