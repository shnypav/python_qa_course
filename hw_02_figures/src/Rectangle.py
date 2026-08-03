from ..src.Figure import Figure
from .logging_config import logger


class Rectangle(Figure):
    name = "Rectangle"

    def __init__(self, side_a, side_b):
        if side_a < 0 or side_b < 0:
            logger.error("Invalid Rectangle sides: side_a=%r, side_b=%r", side_a, side_b)
            raise ValueError("Rectangle sides should be > 0")
        self.side_a = side_a
        self.side_b = side_b
        logger.info("Created %s with side_a=%s, side_b=%s", type(self).__name__, side_a, side_b)

    @property
    def perimeter(self):
        """
        Calculate the perimeter of the rectangle.
        
        @return: Perimeter of the rectangle (2 * (a + b))
        """
        perimeter = 2 * (self.side_a + self.side_b)
        logger.debug("Calculated %s perimeter: %s", type(self).__name__, perimeter)
        return perimeter

    @property
    def area(self) -> object:
        """
        Calculate the area of the rectangle.
        
        @return: Area of the rectangle (a * b)
        """
        area = self.side_a * self.side_b
        logger.debug("Calculated %s area: %s", type(self).__name__, area)
        return area
