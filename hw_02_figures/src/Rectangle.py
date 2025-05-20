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
        """
        Calculate the perimeter of the rectangle.
        
        @return: Perimeter of the rectangle (2 * (a + b))
        """
        return 2 * (self.side_a + self.side_b)

    @property
    def area(self) -> object:
        """
        Calculate the area of the rectangle.
        
        @return: Area of the rectangle (a * b)
        """
        area = self.side_a * self.side_b
        return area
