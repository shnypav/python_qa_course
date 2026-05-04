import pytest

from ..src.Circle import Circle
from ..src.Rectangle import Rectangle
from ..src.Square import Square
from ..src.Triangle import Triangle
from ..src.Figure import Figure


@pytest.mark.parametrize("side_a, side_b, expected_perimeter",
                         [(2, 3, (2 + 3) * 2), (0, 0, 0), (1.2, 3.5, (1.2 + 3.5) * 2)])
def test_rectangle_perimeter(side_a, side_b, expected_perimeter):
    rectangle = Rectangle(side_a, side_b)
    assert rectangle.perimeter == expected_perimeter


@pytest.mark.parametrize("side_a, side_b, expected_area", [(2, 3, 2 * 3), (0, 0, 0), (1.2, 3.5, 1.2 * 3.5)])
def test_rectangle_area(side_a, side_b, expected_area):
    rectangle = Rectangle(side_a, side_b)
    assert rectangle.area == expected_area


def test_rectangle_name(create_rectangle):
    assert create_rectangle.name == "Rectangle"


@pytest.mark.parametrize("side_a, side_b", [(-1, 1), (1, -3), (-1, -1)])
def test_create_rectangle_side_less_than_zero(side_a, side_b):
    with pytest.raises(ValueError) as error:
        Rectangle(side_a, side_b)
    assert error.type is ValueError
    assert str(error.value) == "Rectangle sides should be > 0"


@pytest.mark.parametrize("side_a, side_b", [("aaa", 3), ("", 1), (1, None)])
def test_create_rectangle_with_invalid_sides(side_a, side_b):
    with pytest.raises(TypeError) as error:
        Rectangle(side_a, side_b)
    assert error.type is TypeError


def test_rectangle_is_figure_instance():
    rect = Rectangle(3, 4)
    assert isinstance(rect, Figure)


def test_rectangle_add_area_with_circle():
    rect = Rectangle(3, 4)  # area = 12
    circle = Circle(2)
    result = rect.add_area(circle)
    assert result == pytest.approx(rect.area + circle.area)
    assert isinstance(result, (int, float))


def test_rectangle_add_area_with_square():
    rect = Rectangle(3, 4)   # area = 12
    square = Square(5)        # area = 25
    result = rect.add_area(square)
    assert result == rect.area + square.area


def test_rectangle_add_area_with_triangle():
    rect = Rectangle(3, 4)       # area = 12
    triangle = Triangle(3, 4, 5)  # area = 6
    result = rect.add_area(triangle)
    assert result == pytest.approx(rect.area + triangle.area)


def test_rectangle_add_area_with_another_rectangle():
    rect1 = Rectangle(2, 3)  # area = 6
    rect2 = Rectangle(4, 5)  # area = 20
    assert rect1.add_area(rect2) == 26


def test_rectangle_add_area_with_invalid_object():
    rect = Rectangle(3, 4)
    with pytest.raises(ValueError) as error:
        rect.add_area("not a figure")
    assert error.type is ValueError
    assert error.value.args[0] == "Could not calculate area with argument given"


def test_rectangle_add_area_is_commutative():
    rect = Rectangle(3, 4)
    square = Square(5)
    assert rect.add_area(square) == square.add_area(rect)


@pytest.mark.parametrize("side_a, side_b", [(1e6, 2e6), (1e-6, 2e-6)])
def test_rectangle_extreme_values(side_a, side_b):
    rect = Rectangle(side_a, side_b)
    assert rect.area == pytest.approx(side_a * side_b)
    assert rect.perimeter == pytest.approx(2 * (side_a + side_b))
