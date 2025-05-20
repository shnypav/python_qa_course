from math import sqrt

from .Figure import Figure


class Triangle(Figure):
    name = "Triangle"

    def __init__(self, a, b, c):
        super().__init__()
        if not all(isinstance(side, (int, float)) for side in [a, b, c]):
            raise TypeError("All sides should be numeric")
        if any(side <= 0 for side in [a, b, c]):
            raise ValueError("Triangle sides should be > 0")

        # Check triangle inequality theorem
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            raise ValueError("Triangle inequality theorem violated")

        self.a = a
        self.b = b
        self.c = c
        dept = self.a * self.b * self.c
        self._area = self._calculate_area()
        self._perimeter = self._calculate_perimeter()

    def _calculate_perimeter(self):
        return self.a + self.b + self.c

    def _calculate_area(self):
        # Heron's formula
        s = (self.a + self.b + self.c) / 2
        return sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

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
