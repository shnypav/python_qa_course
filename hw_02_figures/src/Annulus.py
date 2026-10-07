from math import pi

from ..src.Figure import Figure
from .logging_config import logger


class Annulus(Figure):
    name = "Annulus"

    def __init__(self, outer_radius, inner_radius):
        if not all(
            isinstance(radius, (int, float))
            for radius in [outer_radius, inner_radius]
        ):
            logger.error("Annulus radii must be numeric: %r, %r", outer_radius, inner_radius)
            raise TypeError("Radii should be numeric")
        if outer_radius < 0 or inner_radius < 0:
            logger.error("Annulus radii must be non-negative: %r, %r", outer_radius, inner_radius)
            raise ValueError("Radii should be >= 0")
        if inner_radius >= outer_radius:
            logger.error("Annulus inner radius %r is not less than outer radius %r", inner_radius, outer_radius)
            raise ValueError("Inner radius should be less than outer radius")
        self._outer_radius = outer_radius
        self._inner_radius = inner_radius
        logger.info("Created %s", self)

    @property
    def outer_radius(self):
        return self._outer_radius

    @property
    def inner_radius(self):
        return self._inner_radius

    @property
    def width(self):
        return self.outer_radius - self.inner_radius

    @property
    def area(self):
        area = pi * (self.outer_radius ** 2 - self.inner_radius ** 2)
        logger.debug("Calculated %s area: %s", self, area)
        return area

    @property
    def perimeter(self):
        perimeter = 2 * pi * (self.outer_radius + self.inner_radius)
        logger.debug("Calculated %s perimeter: %s", self, perimeter)
        return perimeter

    def __str__(self):
        return (
            f"{self.name}(outer_radius={self.outer_radius}, "
            f"inner_radius={self.inner_radius})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Annulus):
            return False
        return (
            self.outer_radius == other.outer_radius
            and self.inner_radius == other.inner_radius
        )

    def __hash__(self):
        return hash((self.outer_radius, self.inner_radius))

    def _check_comparable(self, other):
        if not isinstance(other, Annulus):
            logger.error("Cannot compare Annulus with %s", type(other).__name__)
            raise TypeError("Cannot compare Annulus with non-Annulus object")

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
            logger.error("Cannot add Annulus area to invalid object: %r", figure)
            raise ValueError(f"Cannot add area of {figure} - it's not a valid figure")
        total = self.area + figure.area
        logger.info("Added %s area %s to %s area %s: %s", self, self.area, figure, figure.area, total)
        return total
