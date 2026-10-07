from math import isclose, sqrt

from ..src.Figure import Figure
from .logging_config import logger


class Trapezoid(Figure):
    name = "Trapezoid"

    def __init__(self, base_a, base_b, leg_c, leg_d, height):
        params = [base_a, base_b, leg_c, leg_d, height]
        if not all(isinstance(param, (int, float)) for param in params):
            logger.error("Trapezoid parameters must be numeric: %r", params)
            raise TypeError("Trapezoid parameters should be numeric")
        if any(param <= 0 for param in params):
            logger.error("Trapezoid parameters must be positive: %r", params)
            raise ValueError("Trapezoid parameters should be > 0")
        if height > leg_c or height > leg_d:
            logger.error("Trapezoid height %r exceeds leg length: %r, %r", height, leg_c, leg_d)
            raise ValueError("Trapezoid height cannot exceed leg length")

        # Horizontal projections of the legs must close the gap between the bases
        projection_c = sqrt(leg_c ** 2 - height ** 2)
        projection_d = sqrt(leg_d ** 2 - height ** 2)
        bases_difference = abs(base_a - base_b)
        if not (
            isclose(bases_difference, projection_c + projection_d, abs_tol=1e-9)
            or isclose(bases_difference, abs(projection_c - projection_d), abs_tol=1e-9)
        ):
            logger.error("Trapezoid dimensions are inconsistent: %r", params)
            raise ValueError("Trapezoid dimensions are inconsistent")

        self._base_a = base_a
        self._base_b = base_b
        self._leg_c = leg_c
        self._leg_d = leg_d
        self._height = height
        logger.info("Created %s", self)

    @property
    def base_a(self):
        return self._base_a

    @property
    def base_b(self):
        return self._base_b

    @property
    def leg_c(self):
        return self._leg_c

    @property
    def leg_d(self):
        return self._leg_d

    @property
    def height(self):
        return self._height

    @property
    def area(self):
        area = (self.base_a + self.base_b) / 2 * self.height
        logger.debug("Calculated %s area: %s", self, area)
        return area

    @property
    def perimeter(self):
        perimeter = self.base_a + self.base_b + self.leg_c + self.leg_d
        logger.debug("Calculated %s perimeter: %s", self, perimeter)
        return perimeter

    def _params(self):
        return (self.base_a, self.base_b, self.leg_c, self.leg_d, self.height)

    def __str__(self):
        return (
            f"{self.name}(base_a={self.base_a}, base_b={self.base_b}, "
            f"leg_c={self.leg_c}, leg_d={self.leg_d}, height={self.height})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Trapezoid):
            return False
        return self._params() == other._params()

    def __hash__(self):
        return hash(self._params())

    def _check_comparable(self, other):
        if not isinstance(other, Trapezoid):
            logger.error("Cannot compare Trapezoid with %s", type(other).__name__)
            raise TypeError("Cannot compare Trapezoid with non-Trapezoid object")

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
            logger.error("Cannot add Trapezoid area to invalid object: %r", figure)
            raise ValueError(f"Cannot add area of {figure} - it's not a valid figure")
        total = self.area + figure.area
        logger.info("Added %s area %s to %s area %s: %s", self, self.area, figure, figure.area, total)
        return total
