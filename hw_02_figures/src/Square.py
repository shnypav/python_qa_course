from ..src.Rectangle import Rectangle


class Square(Rectangle):
    name = "Square"

    def __init__(self, side):
        if side < 0:
            raise ValueError("Rectangle sides should be > 0")
        super().__init__(side_a=side, side_b=side)
    
    def __eq__(self, other):
        if not isinstance(other, Square):
            return False
        return self.side_a == other.side_a
    
    def __str__(self):
        return f"Square with side {self.side_a}"
        
