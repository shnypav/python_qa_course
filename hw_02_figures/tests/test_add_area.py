import pytest

from ..src.Rectangle import Rectangle


class TempClass:
    pass


def test_add_area_01(create_rectangle, create_square):
    # default figures from conftest.py: rectangle = 2, square = 1
    assert create_rectangle.add_area(create_square) == 3


def test_add_area_02(create_rectangle, create_circle):
    # default figures from conftest.py: rectangle = 2, circle = 0
    assert create_rectangle.add_area(create_circle) == 2


def test_add_area_03(create_square, create_triangle):
    # default figures from conftest.py: square = 1
    temp = create_triangle.add_area(create_square)
    assert create_triangle.area == temp - create_square.area


def test_add_area_04(create_rectangle):
    # default figures from conftest.py: rectangle = 2, rectangle calculated here = 8, 8+2 = 10
    rectangle = Rectangle(4, 2)
    assert create_rectangle.add_area(rectangle) == 10


def test_add_area_05(create_rectangle):
    with pytest.raises(ValueError) as error:
        create_rectangle.add_area(TempClass)
    assert error.type is ValueError
    assert error.value.args[0] == "Could not calculate area with argument given"
