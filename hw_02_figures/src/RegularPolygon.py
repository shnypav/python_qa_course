from math import pi, tan

from ..src.Figure import Figure
from .logging_config import logger


class RegularPolygon(Figure):
    name = "RegularPolygon"

    def __init__(self, sides_count, side_length):
        if not isinstance(sides_count, int):
            logger.error("RegularPolygon sides count must be an integer: %r", sides_count)
            raise TypeError("Number of sides should be an integer")
        if not isinstance(side_length, (int, float)):
            logger.error("RegularPolygon side length must be numeric: %r", side_length)
            raise TypeError("Side length should be numeric")
        if sides_count < 3:
            logger.error("RegularPolygon needs at least 3 sides: %r", sides_count)
            raise ValueError("Regular polygon should have at least 3 sides")
        if side_length <= 0:
            logger.error("RegularPolygon side length must be positive: %r", side_length)
            raise ValueError("Side length should be > 0")
        self._sides_count = sides_count
        self._side_length = side_length
        logger.info("Created %s", self)

    @property
    def sides_count(self):
        return self._sides_count

    @property
    def side_length(self):
        return self._side_length

    @property
    def interior_angle(self):
        """
        Calculate the interior angle of the polygon.

        @return: Interior angle in degrees ((n - 2) * 180 / n)
        """
        return (self.sides_count - 2) * 180 / self.sides_count

    @property
    def area(self):
        n = self.sides_count
        area = n * self.side_length ** 2 / (4 * tan(pi / n))
        logger.debug("Calculated %s area: %s", self, area)
        return area

    @property
    def perimeter(self):
        perimeter = self.sides_count * self.side_length
        logger.debug("Calculated %s perimeter: %s", self, perimeter)
        return perimeter

    def __str__(self):
        return (
            f"{self.name}(sides_count={self.sides_count}, "
            f"side_length={self.side_length})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, RegularPolygon):
            return False
        return (
            self.sides_count == other.sides_count
            and self.side_length == other.side_length
        )

    def __hash__(self):
        return hash((self.sides_count, self.side_length))

    def _check_comparable(self, other):
        if not isinstance(other, RegularPolygon):
            logger.error("Cannot compare RegularPolygon with %s", type(other).__name__)
            raise TypeError("Cannot compare RegularPolygon with non-RegularPolygon object")

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
            logger.error("Cannot add RegularPolygon area to invalid object: %r", figure)
            raise ValueError(f"Cannot add area of {figure} - it's not a valid figure")
        total = self.area + figure.area
        logger.info("Added %s area %s to %s area %s: %s", self, self.area, figure, figure.area, total)
        return total
