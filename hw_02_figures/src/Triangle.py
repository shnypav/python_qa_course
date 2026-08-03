from math import sqrt

from .Figure import Figure
from .logging_config import logger


class Triangle(Figure):
    name = "Triangle"

    def __init__(self, a, b, c):
        super().__init__()
        if not all(isinstance(side, (int, float)) for side in [a, b, c]):
            logger.error("Triangle sides must be numeric: %r, %r, %r", a, b, c)
            raise TypeError("All sides should be numeric")
        if any(side <= 0 for side in [a, b, c]):
            logger.error("Triangle sides must be positive: %r, %r, %r", a, b, c)
            raise ValueError("Triangle sides should be > 0")

        # Check triangle inequality theorem
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            logger.error("Triangle inequality violated: %r, %r, %r", a, b, c)
            raise ValueError("Triangle inequality theorem violated")

        self.a = a
        self.b = b
        self.c = c
        self._area = self._calculate_area()
        self._perimeter = self._calculate_perimeter()
        logger.info("Created Triangle with sides=(%s, %s, %s), area=%s, perimeter=%s", a, b, c, self._area, self._perimeter)

    def _calculate_perimeter(self):
        perimeter = self.a + self.b + self.c
        logger.debug("Calculated Triangle perimeter: %s", perimeter)
        return perimeter

    def _calculate_area(self):
        # Heron's formula
        s = (self.a + self.b + self.c) / 2
        area = sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
        logger.debug("Calculated Triangle area: %s", area)
        return area

    @property
    def area(self):
        return self._area

    @property
    def perimeter(self):
        return self._perimeter

    def __str__(self):
        return f"Triangle(a={self.a}, b={self.b}, c={self.c})"

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return (self.a == other.a and self.b == other.b and self.c == other.c)
