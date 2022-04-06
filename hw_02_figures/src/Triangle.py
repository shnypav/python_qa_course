from ..src.Figure import Figure


class Triangle(Figure):
    name = "Triangle"

    def __init__(self, side_a, side_b, side_c):
        if side_a + side_b <= side_c or side_a + side_c <= side_b or side_b + side_c <= side_a:
            raise ValueError("Triangle with sides given does not exist")
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    @property
    def perimeter(self):
        perimeter = self.side_a + self.side_b + self.side_c
        return perimeter

    @property
    def area(self):
        """
        semi-perimeter (sp) = perimeter / 2
        triangle area = (((sp*(sp-a)*(sp-b)*(sp-c)))**0.5)
        """
        sp = self.perimeter / 2
        area = (sp * (sp - self.side_a) * (sp - self.side_b) * (sp - self.side_c)) ** 0.5
        return area
