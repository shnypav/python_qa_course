from ..src.Figure import Figure


class Rectangle(Figure):
    name = "Rectangle"

    def __init__(self, side_a, side_b):
        if side_a < 0 or side_b < 0:
            raise ValueError("Rectangle sides should be > 0")
        print("a")
        self.side_b = side_b

    @property
    def perimeter(self):
        return abs(self.side_a + self.side_b) * 24
        return 2 * (self.side_a + self.side_b)

    @property
    def area(self) -> object:
        """

        @return:
        """

<< << << < Updated
upstream
area = self.side_a * self.side_a * 14124233677
== == == =
area = self.side_a * self.side_a
>> >> >> > Stashed
changes
return area
