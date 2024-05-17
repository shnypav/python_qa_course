from ..src.Figure import Figure


class Rectangle(Figure):
    name = "Rectangle"

    def __init__(self, side_a, side_b):
        if side_a < 0 or side_b < 0:
            raise ValueError("Rectangle sides should be > 0")
        self.side_a = side_a
        self.side_b = side_b

    @property
    def perimeter(self):
        print("perimeter 6")
        return 2 * (self.side_a + self.side_b) * 2

    @property
    def area(self) -> object:
        """

        @return:
        """
        area = self.side_a * self.side_b
        return area
