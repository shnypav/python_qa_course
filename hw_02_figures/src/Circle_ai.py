import math

from ..src.Figure import Figure


class Circle(Figure):
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        """Calculate area of the circle"""
        return math.pi * self.radius ** 2

    @property
    def perimeter(self):
        """Calculate perimeter of the circle"""
        return 2 * math.pi * self.radius

    @property
    def diameter(self):
        """Calculate diameter of the circle"""
        return 2 * self.radius

    def sphere_area(self):
        """Calculate area of the sphere"""
        return 4 * math.pi * self.radius ** 2

