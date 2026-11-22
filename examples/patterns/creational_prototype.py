# Prototype: make new objects by copying a ready-made one, instead of building from scratch.
# Use when: creating an object is expensive or has many settings, and you need many similar copies.
# Source: https://www.gofpattern.com/creational/patterns/prototype-pattern.php
import copy


class Restaurant:
    def __init__(self, name: str, menu: list[str], settings: dict):
        self.name = name
        self.menu = menu  # imagine this was loaded from a slow DB call
        self.settings = settings

    def clone(self) -> "Restaurant":
        return copy.deepcopy(self)  # deep: the copy gets its own menu list, not a shared one


template = Restaurant("Template", ["burger", "fries"], {"delivery": True})

branch = template.clone()
branch.name = "Branch #2"
branch.menu.append("shake")

print(template.name, template.menu)
print(branch.name, branch.menu)
assert template.menu == ["burger", "fries"]  # the original did not change
