from math import radians, sin

from ..src.Figure import Figure
from .logging_config import logger


class Parallelogram(Figure):
    name = "Parallelogram"

    def __init__(self, side_a, side_b, angle):
        params = [side_a, side_b, angle]
        if not all(isinstance(param, (int, float)) for param in params):
            logger.error("Parallelogram parameters must be numeric: %r", params)
            raise TypeError("Parallelogram parameters should be numeric")
        if side_a <= 0 or side_b <= 0:
            logger.error("Parallelogram sides must be positive: %r, %r", side_a, side_b)
            raise ValueError("Parallelogram sides should be > 0")
        if not 0 < angle < 180:
            logger.error("Parallelogram angle out of range: %r", angle)
            raise ValueError("Parallelogram angle should be between 0 and 180 degrees")
        self._side_a = side_a
        self._side_b = side_b
        self._angle = angle
        logger.info("Created %s", self)

    @property
    def side_a(self):
        return self._side_a

    @property
    def side_b(self):
        return self._side_b

    @property
    def angle(self):
        """
        Get the angle between the sides.

        @return: Angle in degrees
        """
        return self._angle

    @property
    def height(self):
        """
        Calculate the height dropped onto side_a.

        @return: Height of the parallelogram (b * sin(angle))
        """
        return self.side_b * sin(radians(self.angle))

    @property
    def area(self):
        area = self.side_a * self.height
        logger.debug("Calculated %s area: %s", self, area)
        return area

    @property
    def perimeter(self):
        perimeter = 2 * (self.side_a + self.side_b)
        logger.debug("Calculated %s perimeter: %s", self, perimeter)
        return perimeter

    def _params(self):
        return (self.side_a, self.side_b, self.angle)

    def __str__(self):
        return (
            f"{self.name}(side_a={self.side_a}, side_b={self.side_b}, "
            f"angle={self.angle})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Parallelogram):
            return False
        return self._params() == other._params()

    def __hash__(self):
        return hash(self._params())

    def _check_comparable(self, other):
        if not isinstance(other, Parallelogram):
            logger.error("Cannot compare Parallelogram with %s", type(other).__name__)
            raise TypeError("Cannot compare Parallelogram with non-Parallelogram object")

    def __lt__(self, other):
        self._check_comparable(other)
        return self.area < other.area

    def __gt__(self, other):
        self._check_comparable(other)
        return self.area > other.area

    def __le__(self, other):
        self._check_comparable(other)
        return self.area <= other.area

    def __ge__(self, other):
        self._check_comparable(other)
        return self.area >= other.area

    def add_area(self, figure):
        if not hasattr(figure, "area"):
            logger.error("Cannot add Parallelogram area to invalid object: %r", figure)
            raise ValueError(f"Cannot add area of {figure} - it's not a valid figure")
        total = self.area + figure.area
        logger.info("Added %s area %s to %s area %s: %s", self, self.area, figure, figure.area, total)
        return total
