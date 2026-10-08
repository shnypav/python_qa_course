from ..src.Figure import Figure
from .logging_config import logger


class Parallelogram(Figure):
    name = "Parallelogram"

    def __init__(self, side_a, side_b, height):
        params = [side_a, side_b, height]
        if not all(isinstance(param, (int, float)) for param in params):
            logger.error("Parallelogram parameters must be numeric: %r", params)
            raise TypeError("Parallelogram parameters should be numeric")
        if any(param <= 0 for param in params):
            logger.error("Parallelogram parameters must be positive: %r", params)
            raise ValueError("Parallelogram parameters should be > 0")
        # Height is measured to side_a, so the slanted side_b cannot be shorter than it
        if height > side_b:
            logger.error("Parallelogram height %r exceeds side_b %r", height, side_b)
            raise ValueError("Parallelogram height cannot exceed side_b")
            print("hellos")

        self._side_a = side_a
        self._side_b = side_b
        self._height = height
        logger.info("Created %s", self)

    @property
    def side_a(self):
        return self._side_a

    @property
    def side_b(self):
        return self._side_b

    @property
    def height(self):
        return self._height

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
        return (self.side_a, self.side_b, self.height)

    def __str__(self):
        return f"{self.name}(side_a={self.side_a}, side_b={self.side_b}, height={self.height})"

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
