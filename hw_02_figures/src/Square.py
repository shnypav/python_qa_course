from ..src.Rectangle import Rectangle


class Square(Rectangle):
    name = "Square"

    def __init__(self, side):
        if side < 0:
            raise ValueError("Square side should be > 0")
        super().__init__(side_a=side, side_b=side)
        
