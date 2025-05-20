class Figure:
    area = None

    def __init__(self):
        if self.__class__ is Figure:
            raise TypeError("Please do not instantiate base class Figure")

    def add_area(self, figure):
        if not isinstance(figure, Figure):
            raise ValueError("Could not calculate area with argument given")
        return self.area + figure.area

    @property
    def perimeter(self):
        """
        Calculate the perimeter of the figure.
        This method should be implemented by subclasses.
        
        @return: Perimeter of the figure
        """
        raise NotImplementedError("Subclasses must implement perimeter calculation")
