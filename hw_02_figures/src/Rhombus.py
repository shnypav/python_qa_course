from math import sqrt

from ..src.Figure import Figure


class Rhombus(Figure):
    name = "Rhombus"

    def __init__(self, diagonal_a, diagonal_b):
        if not all(
            isinstance(diagonal, (int, float))
            for diagonal in [diagonal_a, diagonal_b]
        ):
            raise TypeError("Diagonals should be numeric")
        if diagonal_a <= 0 or diagonal_b <= 0:
            raise ValueError("Rhombus diagonals should be > 0")
        self._diagonal_a = diagonal_a
        self._diagonal_b = diagonal_b

    @property
    def diagonal_a(self):
        return self._diagonal_a

    @property
    def diagonal_b(self):
        return self._diagonal_b

    @property
    def side(self):
        return sqrt((self.diagonal_a / 2) ** 2 + (self.diagonal_b / 2) ** 2)

    @property
    def area(self):
        return self.diagonal_a * self.diagonal_b / 2

    @property
    def perimeter(self):
        return 4 * self.side

    def __str__(self):
        return (
            f"{self.name}(diagonal_a={self.diagonal_a}, "
            f"diagonal_b={self.diagonal_b})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Rhombus):
            return False
        return (
            self.diagonal_a == other.diagonal_a
            and self.diagonal_b == other.diagonal_b
        )

    def __hash__(self):
        return hash((self.diagonal_a, self.diagonal_b))

    def __lt__(self, other):
        if not isinstance(other, Rhombus):
            raise TypeError("Cannot compare Rhombus with non-Rhombus object")
        return self.area < other.area

    def __gt__(self, other):
        if not isinstance(other, Rhombus):
            raise TypeError("Cannot compare Rhombus with non-Rhombus object")
        return self.area > other.area

    def __le__(self, other):
        if not isinstance(other, Rhombus):
            raise TypeError("Cannot compare Rhombus with non-Rhombus object")
        return self.area <= other.area

    def __ge__(self, other):
        if not isinstance(other, Rhombus):
            raise TypeError("Cannot compare Rhombus with non-Rhombus object")
        return self.area >= other.area

    def add_area(self, figure):
        if not hasattr(figure, "area"):
            raise ValueError(f"Cannot add area of {figure} - it's not a valid figure")
        return self.area + figure.area
