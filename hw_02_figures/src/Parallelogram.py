from ..src.Figure import Figure
from .logging_config import logger


class Parallelogram(Figure):
    name = "Parallelogram"

    def __init__(self, base, side, height):
        params = [base, side, height]
        if not all(isinstance(param, (int, float)) for param in params):
            logger.error("Parallelogram parameters must be numeric: %r", params)
            raise TypeError("Parallelogram parameters should be numeric")
        if any(param <= 0 for param in params):
            logger.error("Parallelogram parameters must be positive: %r", params)
            raise ValueError("Parallelogram parameters should be > 0")
        if height > side:
            logger.error("Parallelogram height %r exceeds side length: %r", height, side)
            raise ValueError("Parallelogram height cannot exceed side length")

        self._base = base
        self._side = side
        self._height = height
        logger.info("Created %s", self)

    @property
    def base(self):
        return self._base

    @property
    def side(self):
        return self._side

    @property
    def height(self):
        return self._height

    @property
    def area(self):
        area = self.base * self.height
        logger.debug("Calculated %s area: %s", self, area)
        return area

    @property
    def perimeter(self):
        perimeter = 2 * (self.base + self.side)
        logger.debug("Calculated %s perimeter: %s", self, perimeter)
        return perimeter

    def _params(self):
        return (self.base, self.side, self.height)

    def __str__(self):
        return f"{self.name}(base={self.base}, side={self.side}, height={self.height})"

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
