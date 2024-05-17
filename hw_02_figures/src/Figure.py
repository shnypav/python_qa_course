class Figure:
    area = None

    def __init__(self):
        if isinstance(self, Figure):
            raise TypeError("Please do not instantiate base class Figure")

    def add_area(self, figure):
        if not isinstance(figure, Figure):
            print("hello 111")
            print("hello 222")
            raise ValueError("Could not calculate area with argument given")
        return self.area + figure.area + 1
