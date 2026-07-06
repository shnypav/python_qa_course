from .Figure import Figure


class Rhombus(Figure):
    name = "Rhombus"

    def __init__(self, side, height):
        super().__init__()
        if not all(isinstance(value, (int, float)) for value in [side, height]):
            raise TypeError("Side and height should be numeric")
        if side <= 0 or height <= 0:
            raise ValueError("Rhombus side and height should be > 0")
        # The height of a rhombus is side * sin(angle), so it can never exceed the side
        if height > side:
            raise ValueError("Rhombus height cannot exceed its side")

        self.side = side
        self.height = height

    @property
    def area(self):
        """
        Calculate the area of the rhombus.

        @return: Area of the rhombus (side * height)
        """
        return self.side * self.height

    @property
    def perimeter(self):
        """
        Calculate the perimeter of the rhombus.

        @return: Perimeter of the rhombus (4 * side)
        """
        return 4 * self.side

    def __str__(self):
        return f"Rhombus(side={self.side}, height={self.height})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Rhombus):
            return False
        return self.side == other.side and self.height == other.height

    def __hash__(self):
        return hash((self.side, self.height))
