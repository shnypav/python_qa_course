from math import pi, sqrt

from .Figure import Figure


class Ellipse(Figure):
    name = "Ellipse"

    def __init__(self, semi_major, semi_minor):
        super().__init__()
        if not all(isinstance(value, (int, float)) for value in [semi_major, semi_minor]):
            raise TypeError("Semi-axes should be numeric")
        if semi_major <= 0 or semi_minor <= 0:
            raise ValueError("Ellipse semi-axes should be > 0")

        self.semi_major = semi_major
        self.semi_minor = semi_minor

    @property
    def area(self):
        """
        Calculate the area of the ellipse.

        @return: Area of the ellipse (pi * a * b)
        """
        return pi * self.semi_major * self.semi_minor

    @property
    def perimeter(self):
        """
        Calculate the perimeter of the ellipse using Ramanujan's approximation.

        @return: Approximate perimeter of the ellipse
                 (pi * (3 * (a + b) - sqrt((3a + b) * (a + 3b))))
        """
        a = self.semi_major
        b = self.semi_minor
        return pi * (3 * (a + b) - sqrt((3 * a + b) * (a + 3 * b)))

    def __str__(self):
        return f"Ellipse(semi_major={self.semi_major}, semi_minor={self.semi_minor})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Ellipse):
            return False
        return self.semi_major == other.semi_major and self.semi_minor == other.semi_minor

    def __hash__(self):
        return hash((self.semi_major, self.semi_minor))
