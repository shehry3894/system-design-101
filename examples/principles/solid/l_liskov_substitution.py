# L: Liskov Substitution. A subclass must work anywhere its parent class works.
# Use when: checking if inheritance is right. "Is-a" in real life is not enough.
# Source: https://en.wikipedia.org/wiki/Liskov_substitution_principle


class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h

    def set_width(self, w):
        self.w = w

    def area(self):
        return self.w * self.h


class SquareBad(Rectangle):  # a square "is a" rectangle... but behaves differently
    def set_width(self, w):
        self.w = self.h = w


def stretch(rect: Rectangle):  # written for Rectangle: width changes, height stays
    rect.set_width(10)
    return rect.area()


print("rectangle 2x5 ->", stretch(Rectangle(2, 5)))  # 50, as expected
print("square    5x5 ->", stretch(SquareBad(5, 5)))  # 100, not 50: the caller's assumption broke
assert stretch(Rectangle(2, 5)) == 50
assert stretch(SquareBad(5, 5)) != 50  # this is the violation

# Fix: don't make Square a subclass of Rectangle. Give both a common Shape with area() only.
