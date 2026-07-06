import pytest

from ..src.Circle import Circle
from ..src.Triangle import Triangle
from ..src.Rectangle import Rectangle
from ..src.Square import Square
from ..src.Rhombus import Rhombus
from ..src.Trapezoid import Trapezoid
from ..src.Ellipse import Ellipse


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


@pytest.fixture()
def create_rhombus():
    rhombus = Rhombus(5, 4)
    return rhombus


@pytest.fixture()
def create_trapezoid():
    trapezoid = Trapezoid(10, 4, 4, 5, 5)
    return trapezoid


@pytest.fixture()
def create_ellipse():
    ellipse = Ellipse(3, 2)
    return ellipse
