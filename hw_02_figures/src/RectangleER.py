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
<<<<<<< HEAD:hw_02_figures/src/RectangleE.py
        return 2 * (self.side_a + self.side_b)

=======
        perimeter = self.side_a * 2 + self.side_b * 4
        return perimeter
    
>>>>>>> 51d1a09 (rename):hw_02_figures/src/RectangleER.py
    @property
    def area(self) -> object:
        """

        @return:
        """
        area = self.side_a * self.side_b
        return area
