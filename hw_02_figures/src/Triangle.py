from ..src.Figure import Figure


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
        Calculate the area of a triangle using the semi-perimeter formula:
        semi-perimeter (sp) = perimeter / 2
        triangle area = sqrt(sp * (sp - a) * (sp - b) * (sp - c))
        """
        sp = self.perimeter / 2
        area = (sp * (sp - self.side_a) * (sp - self.side_b) * (sp - self.side_c)) ** 0.5
        return area

    # Property that calculates and returns the circumcircle radius of the triangle
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
    
    def is_right_triangle(self):
        sides = sorted([self.side_a, self.side_b, self.side_c])
        return abs(sides[0] ** 2 + sides[1] ** 2 - sides[2] ** 2) < 1e-9