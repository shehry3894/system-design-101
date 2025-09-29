# Definition: Subtypes must be substitutable for their base types without breaking behavior.
# Why: Inheritance should not violate expectations of the base class.

# ❌ Bad: Square violates Rectangle's contract
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def set_width(self, w):
        self.width = self.height = w  # Changes both → breaks behavior

    def set_height(self, h):
        self.width = self.height = h

# ✅ Good: Avoid Square extending Rectangle; model separately
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side
