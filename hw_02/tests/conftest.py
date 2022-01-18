import pytest

from ..src.Circle import Circle
from ..src.Triangle import Triangle
from ..src.Rectangle import Rectangle
from ..src.Square import Square


@pytest.fixture()
def create_circle():
    circle = Circle(0)
    return circle


@pytest.fixture()
def create_triangle():
    triangle = Triangle(3, 3, 3)
    return triangle


@pytest.fixture()
def create_rectangle():
    rectangle = Rectangle(1, 2)
    return rectangle


@pytest.fixture()
def create_square():
    square = Square(1)
    return square
