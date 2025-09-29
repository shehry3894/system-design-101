# Definition: Software entities should be open for extension but closed for modification.
# Why: You shouldn’t modify existing code to add new functionality — instead, extend it.

# ❌ Bad: Every time we add a new shape, we modify area_calculator
class AreaCalculator:
    def calculate(self, shape):
        if isinstance(shape, Rectangle):
            return shape.width * shape.height
        elif isinstance(shape, Circle):
            return 3.14 * shape.radius ** 2


# ✅ Good: Each shape implements area itself (extendable without modifying calculator)
class Shape:
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2


def calculate_area(shape: Shape):
    return shape.area()
