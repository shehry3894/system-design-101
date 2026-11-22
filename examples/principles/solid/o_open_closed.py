# O: Open/Closed. Open for extension, closed for modification.
# Use when: every new case forces you to edit the same if/elif chain.
# Source: https://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html
import math


# Bad: adding a Triangle means editing this function.
def area_bad(shape):
    if shape["type"] == "rectangle":
        return shape["w"] * shape["h"]
    if shape["type"] == "circle":
        return math.pi * shape["r"] ** 2


# Good: a new shape is a new class. Existing code stays untouched.
class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h


class Circle:
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r**2


class Triangle:  # added later, nothing else changed
    def __init__(self, base, height):
        self.base, self.height = base, height

    def area(self):
        return self.base * self.height / 2


shapes = [Rectangle(2, 3), Circle(1), Triangle(4, 5)]
print([round(s.area(), 2) for s in shapes])
assert Rectangle(2, 3).area() == area_bad({"type": "rectangle", "w": 2, "h": 3})
