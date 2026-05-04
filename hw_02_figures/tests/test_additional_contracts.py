import pytest

from ..src.Circle import Circle
from ..src.Rectangle import Rectangle
from ..src.Square import Square
from ..src.Triangle import Triangle


@pytest.mark.parametrize(
    "sides",
    [
        (1, 2, 3),
        (1, 3, 2),
        (3, 1, 2),
    ],
)
def test_degenerate_triangles_are_rejected(sides):
    with pytest.raises(ValueError, match="Triangle inequality theorem violated"):
        Triangle(*sides)


def test_circle_equal_radius_ordering_results():
    left = Circle(4)
    right = Circle(4)

    assert not left < right
    assert not left > right
    assert left <= right
    assert left >= right


def test_rectangle_preserves_constructor_side_values():
    rectangle = Rectangle(2.5, 7)

    assert rectangle.side_a == 2.5
    assert rectangle.side_b == 7
    assert rectangle.area == pytest.approx(17.5)
    assert rectangle.perimeter == pytest.approx(19)


def test_square_initializes_equal_rectangle_sides():
    square = Square(6.5)

    assert square.side_a == 6.5
    assert square.side_b == 6.5
    assert square.area == pytest.approx(42.25)
    assert square.perimeter == pytest.approx(26)


def test_add_area_does_not_mutate_figures():
    rectangle = Rectangle(3, 8)
    triangle = Triangle(5, 5, 6)
    rectangle_area = rectangle.area
    triangle_area = triangle.area
    rectangle_perimeter = rectangle.perimeter
    triangle_perimeter = triangle.perimeter

    result = rectangle.add_area(triangle)

    assert result == pytest.approx(rectangle_area + triangle_area)
    assert rectangle.area == rectangle_area
    assert triangle.area == triangle_area
    assert rectangle.perimeter == rectangle_perimeter
    assert triangle.perimeter == triangle_perimeter
