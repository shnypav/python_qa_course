from ..src.Figure import Figure

"""
Class Triangle inherits from the Figure class. It represents a triangle figure.

Attributes:
- name (str): The name of the figure.
- side_a (float): Length of the first side of the triangle.
- side_b (float): Length of the second side of the triangle.
- side_c (float): Length of the third side of the triangle.

Methods:
- __init__(self, side_a, side_b, side_c): Initializes a new instance of the class. Sets up the sides of the triangle and checks if the triangle
  with provided sides can exist.

Properties:
- perimeter (float): Returns the perimeter of the triangle.
- area (float): Returns the area of the triangle using the Heron's formula.
- circumcircle_radius (float): Returns the radius of the circumcircle of the triangle. It's the radius of a circle passing through the vertices
  of the triangle.
- incircle_radius (float): Returns the radius of an incircle of the triangle. It's the radius of a circle inscribed in the triangle.
"""


class Triangle(Figure):
    name = "Triangle"

    def __init__(self, side_a, side_b, side_c):
        if side_a + side_b <= side_c or side_a + side_c <= side_b or side_b + side_c <= side_a:
            raise ValueError("Triangle with sides given does not exist")
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    @property
    def perimeter(self):
        perimeter = self.side_a + self.side_b + self.side_c
        return perimeter

    @property
    def area(self):
        """
        semi-perimeter (sp) = perimeter / 2
        triangle area = (((sp*(sp-a)*(sp-b)*(sp-c)))**0.5)
        """
        sp = self.perimeter / 2
        area = (sp * (sp - self.side_a) * (sp - self.side_b) * (sp - self.side_c)) ** 0.5
        return area

    @property
    def circumcircle_radius(self):
        """
        circumcircle radius (R) = (a*b*c) / (4 * area)
        """
        circumcircle_radius = (self.side_a * self.side_b * self.side_c) / (4 * self.area)
        return circumcircle_radius

    @property
    def incircle_radius(self):
        """
        incircle radius (r) = area / (perimeter / 2)
        """
        incircle_radius = self.area / (self.perimeter / 2)
        return incircle_radius
