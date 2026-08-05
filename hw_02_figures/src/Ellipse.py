from math import pi, sqrt

from ..src.Figure import Figure


class Ellipse(Figure):
    name = "Ellipse"

    def __init__(self, semi_major_axis, semi_minor_axis):
        if not all(
            isinstance(axis, (int, float))
            for axis in [semi_major_axis, semi_minor_axis]
        ):
            raise TypeError("Semi-axes should be numeric")
        if semi_major_axis < 0 or semi_minor_axis < 0:
            raise ValueError("Semi-axes should be >= 0")
        self._semi_major_axis = semi_major_axis
        self._semi_minor_axis = semi_minor_axis

    @property
    def semi_major_axis(self):
        return self._semi_major_axis

    @property
    def semi_minor_axis(self):
        return self._semi_minor_axis

    @property
    def area(self):
        return pi * self.semi_major_axis * self.semi_minor_axis

    @property
    def perimeter(self):
        a = self.semi_major_axis
        b = self.semi_minor_axis
        return pi * (3 * (a + b) - sqrt((3 * a + b) * (a + 3 * b)))

    def __str__(self):
        return (
            f"{self.name}(semi_major_axis={self.semi_major_axis}, "
            f"semi_minor_axis={self.semi_minor_axis})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Ellipse):
            return False
        return (
            self.semi_major_axis == other.semi_major_axis
            and self.semi_minor_axis == other.semi_minor_axis
        )

    def __hash__(self):
        return hash((self.semi_major_axis, self.semi_minor_axis))

    def __lt__(self, other):
        if not isinstance(other, Ellipse):
            raise TypeError("Cannot compare Ellipse with non-Ellipse object")
        return self.area < other.area

    def __gt__(self, other):
        if not isinstance(other, Ellipse):
            raise TypeError("Cannot compare Ellipse with non-Ellipse object")
        return self.area > other.area

    def __le__(self, other):
        if not isinstance(other, Ellipse):
            raise TypeError("Cannot compare Ellipse with non-Ellipse object")
        return self.area <= other.area

    def __ge__(self, other):
        if not isinstance(other, Ellipse):
            raise TypeError("Cannot compare Ellipse with non-Ellipse object")
        return self.area >= other.area

    def add_area(self, figure):
        if not hasattr(figure, "area"):
            raise ValueError(f"Cannot add area of {figure} - it's not a valid figure")
        return self.area + figure.area
