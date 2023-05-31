from ..src.Figure import Figure
from math import pi


class Circle(Figure):
    name = "Circle"

    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius should be >= 0")
        self.radius = radius

    # Returns the area of the circle using the formula area = pi * radius^2
    @property
    def area(self):
        area = pi * (self.radius ** 2)
        return area

    @property
    def perimeter(self):
        """

        @return: 
        """
        # Perimeter property which calculates and returns the perimeter of the circle using the formula: 2 * pi * radius
        perimeter = 2 * pi * self.radius
        return perimeter
