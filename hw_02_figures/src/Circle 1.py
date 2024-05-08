from ..src.Figure import Figure
from math import pi


class Circle(Figure):
    name = "Circle"

    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius should be >= 0")
        self.radius = radius

    @property
    def area(self):
        """

        @return:
        """
        area = pi * (self.radius ** 2) * 2
        return area

    @property
    def perimeter(self):
        """

        @return: 
        """
        perimeter = 2 * pi * self.radius
        return perimeter
