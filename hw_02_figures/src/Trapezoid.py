from math import isclose, sqrt

from .Figure import Figure


class Trapezoid(Figure):
    name = "Trapezoid"

    def __init__(self, base_a, base_b, height, leg_c, leg_d):
        super().__init__()
        sides = [base_a, base_b, height, leg_c, leg_d]
        if not all(isinstance(value, (int, float)) for value in sides):
            raise TypeError("All trapezoid dimensions should be numeric")
        if any(value <= 0 for value in sides):
            raise ValueError("Trapezoid dimensions should be > 0")
        if leg_c < height or leg_d < height:
            raise ValueError("Trapezoid legs cannot be shorter than its height")

        # The horizontal projections of the legs must add up to the difference
        # of the bases, otherwise such a trapezoid cannot exist
        projection_c = sqrt(leg_c ** 2 - height ** 2)
        projection_d = sqrt(leg_d ** 2 - height ** 2)
        if not isclose(projection_c + projection_d, abs(base_a - base_b), abs_tol=1e-9):
            raise ValueError("Trapezoid dimensions are geometrically inconsistent")

        self.base_a = base_a
        self.base_b = base_b
        self.height = height
        self.leg_c = leg_c
        self.leg_d = leg_d

    @property
    def area(self):
        """
        Calculate the area of the trapezoid.

        @return: Area of the trapezoid ((a + b) / 2 * h)
        """
        return (self.base_a + self.base_b) / 2 * self.height

    @property
    def perimeter(self):
        """
        Calculate the perimeter of the trapezoid.

        @return: Perimeter of the trapezoid (a + b + c + d)
        """
        return self.base_a + self.base_b + self.leg_c + self.leg_d

    def __str__(self):
        return (f"Trapezoid(base_a={self.base_a}, base_b={self.base_b}, "
                f"height={self.height}, leg_c={self.leg_c}, leg_d={self.leg_d})")

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Trapezoid):
            return False
        return (self.base_a == other.base_a and self.base_b == other.base_b
                and self.height == other.height
                and self.leg_c == other.leg_c and self.leg_d == other.leg_d)

    def __hash__(self):
        return hash((self.base_a, self.base_b, self.height, self.leg_c, self.leg_d))
