import pytest

from ..src.Rectangle import Rectangle


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


def test_rectangle_add_area_with_another_rectangle():
    r1 = Rectangle(3, 4)   # area = 12
    r2 = Rectangle(2, 5)   # area = 10
    assert r1.add_area(r2) == 22


def test_rectangle_add_area_with_square():
    from ..src.Square import Square
    rect = Rectangle(3, 4)   # area = 12
    sq = Square(3)           # area = 9
    assert rect.add_area(sq) == 21


def test_rectangle_add_area_with_circle():
    import math
    from ..src.Circle import Circle
    rect = Rectangle(3, 4)  # area = 12
    circle = Circle(2)      # area = 4π
    assert rect.add_area(circle) == pytest.approx(12 + 4 * math.pi)


def test_rectangle_add_area_with_triangle():
    from ..src.Triangle import Triangle
    rect = Rectangle(3, 4)         # area = 12
    triangle = Triangle(3, 4, 5)   # area = 6
    assert rect.add_area(triangle) == 18


def test_rectangle_add_area_with_invalid_object():
    rect = Rectangle(3, 4)
    with pytest.raises(ValueError) as error:
        rect.add_area("not a figure")
    assert error.type is ValueError
    assert error.value.args[0] == "Could not calculate area with argument given"


@pytest.mark.parametrize("side_a, side_b", [(0, 5), (5, 0), (0, 0)])
def test_rectangle_zero_sides_are_allowed(side_a, side_b):
    rect = Rectangle(side_a, side_b)
    assert rect.area == 0


def test_rectangle_large_values():
    rect = Rectangle(1e6, 1e6)
    assert rect.area == pytest.approx(1e12)
    assert rect.perimeter == pytest.approx(4e6)
