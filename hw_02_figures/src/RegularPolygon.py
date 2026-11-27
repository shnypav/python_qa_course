from math import pi, tan

from ..src.Figure import Figure
from .logging_config import logger


class RegularPolygon(Figure):
    name = "RegularPolygon"

    def __init__(self, sides, side_length):
        if not isinstance(sides, int):
            logger.error("RegularPolygon sides must be an integer: %r", sides)
            raise TypeError("RegularPolygon sides should be an integer")
        if sides < 3:
            logger.error("RegularPolygon sides must be at least 3: %r", sides)
            raise ValueError("RegularPolygon sides should be >= 3")
        if not isinstance(side_length, (int, float)):
            logger.error("RegularPolygon side length must be numeric: %r", side_length)
            raise TypeError("RegularPolygon side length should be numeric")
        if side_length <= 0:
            logger.error("RegularPolygon side length must be positive: %r", side_length)
            raise ValueError("RegularPolygon side length should be > 0")

        self._sides = sides
        self._side_length = side_length
        logger.info("Created %s", self)

    @property
    def sides(self):
        return self._sides

    @property
    def side_length(self):
        return self._side_length

    @property
    def area(self):
        area = self.sides * self.side_length ** 2 / (4 * tan(pi / self.sides))
        logger.debug("Calculated %s area: %s", self, area)
        return area

    @property
    def perimeter(self):
        perimeter = self.sides * self.side_length
        logger.debug("Calculated %s perimeter: %s", self, perimeter)
        return perimeter

    def _params(self):
        return (self.sides, self.side_length)

    def __str__(self):
        return f"{self.name}(sides={self.sides}, side_length={self.side_length})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, RegularPolygon):
            return False
        return self._params() == other._params()

    def __hash__(self):
        return hash(self._params())

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
