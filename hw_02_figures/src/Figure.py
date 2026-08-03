from .logging_config import logger


class Figure:
    area = None

    def __init__(self):
        if self.__class__ is Figure:
            logger.error("Attempted to instantiate abstract Figure")
            raise TypeError("Please do not instantiate base class Figure")

    def add_area(self, figure):
        if not isinstance(figure, Figure):
            logger.error("Cannot add area of %r to %s: not a Figure", figure, type(self).__name__)
            raise ValueError("Could not calculate area with argument given")
        total = self.area + figure.area
        logger.info("Added areas: %s (%s) + %s (%s) = %s", self, self.area, figure, figure.area, total)
        return total

    @property
    def perimeter(self):
        """
        Calculate the perimeter of the figure.
        This method should be implemented by subclasses.
        
        @return: Perimeter of the figure
        """
        logger.error("Perimeter requested from %s without an implementation", type(self).__name__)
        raise NotImplementedError("Subclasses must implement perimeter calculation")
