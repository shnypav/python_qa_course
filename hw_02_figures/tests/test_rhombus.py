from math import sqrt

import pytest

from ..src.Circle import Circle
from ..src.Ellipse import Ellipse
from ..src.Figure import Figure
from ..src.Rectangle import Rectangle
from ..src.Rhombus import Rhombus
from ..src.Square import Square


@pytest.mark.parametrize(
    "diagonal_a, diagonal_b, expected_area",
    [
        (6, 8, 24),
        (4, 4, 8),
        (2.5, 4, 5),
    ],
)
def test_rhombus_area(diagonal_a, diagonal_b, expected_area):
    rhombus = Rhombus(diagonal_a, diagonal_b)
    assert rhombus.area == pytest.approx(expected_area)
    assert isinstance(rhombus.area, (int, float))


@pytest.mark.parametrize(
    "diagonal_a, diagonal_b, expected_perimeter",
    [
        (6, 8, 20),
        (4, 4, 4 * sqrt(8)),
    ],
)
def test_rhombus_perimeter(diagonal_a, diagonal_b, expected_perimeter):
    rhombus = Rhombus(diagonal_a, diagonal_b)
    assert rhombus.perimeter == pytest.approx(expected_perimeter)


def test_rhombus_side():
    rhombus = Rhombus(6, 8)
    assert rhombus.side == pytest.approx(5)


def test_rhombus_has_name():
    assert Rhombus(3, 4).name == "Rhombus"


def test_rhombus_is_figure_instance():
    assert isinstance(Rhombus(3, 4), Figure)


@pytest.mark.parametrize("diagonal_a, diagonal_b", [("aaa", 4), (3, None), (2, "*&^")])
def test_create_rhombus_with_invalid_diagonals(diagonal_a, diagonal_b):
    with pytest.raises(TypeError, match="Diagonals should be numeric"):
        Rhombus(diagonal_a, diagonal_b)


@pytest.mark.parametrize(
    "diagonal_a, diagonal_b",
    [(0, 4), (3, 0), (-2, 5), (4, -1)],
)
def test_create_rhombus_with_non_positive_diagonals(diagonal_a, diagonal_b):
    with pytest.raises(ValueError, match="Rhombus diagonals should be > 0"):
        Rhombus(diagonal_a, diagonal_b)


def test_rhombus_add_area_with_rhombus():
    rhombus1 = Rhombus(6, 8)
    rhombus2 = Rhombus(4, 4)
    assert rhombus1.add_area(rhombus2) == pytest.approx(rhombus1.area + rhombus2.area)


def test_rhombus_add_area_with_different_figure(create_rectangle):
    rhombus = Rhombus(6, 8)
    assert rhombus.add_area(create_rectangle) == pytest.approx(rhombus.area + create_rectangle.area)


def test_rhombus_matches_square_when_diagonals_form_square():
    side = 4
    diagonal = side * sqrt(2)
    rhombus = Rhombus(diagonal, diagonal)
    square = Square(side)

    assert rhombus.area == pytest.approx(square.area)
    assert rhombus.perimeter == pytest.approx(square.perimeter)


def test_rhombus_equality():
    rhombus1 = Rhombus(6, 8)
    rhombus2 = Rhombus(6, 8)
    rhombus3 = Rhombus(8, 6)

    assert rhombus1 == rhombus2
    assert rhombus1 != rhombus3
    assert rhombus1 != Square(4)


def test_rhombus_hash():
    rhombus1 = Rhombus(6, 8)
    rhombus2 = Rhombus(6, 8)
    rhombus3 = Rhombus(8, 6)

    assert hash(rhombus1) == hash(rhombus2)
    assert hash(rhombus1) != hash(rhombus3)


def test_rhombus_comparison_operators():
    smaller = Rhombus(4, 4)
    larger = Rhombus(6, 8)
    equal = Rhombus(4, 4)

    assert smaller < larger
    assert larger > smaller
    assert smaller <= equal
    assert smaller <= larger
    assert larger >= smaller
    assert smaller >= equal


def test_rhombus_ordering_rejects_non_rhombuses():
    rhombus = Rhombus(6, 8)

    with pytest.raises(TypeError, match="Cannot compare Rhombus with non-Rhombus object"):
        rhombus < Ellipse(2, 3)


def test_rhombus_add_area_with_invalid_argument():
    rhombus = Rhombus(6, 8)

    with pytest.raises(ValueError, match="Cannot add area of"):
        rhombus.add_area("not a figure")


def test_rhombus_str_and_repr():
    rhombus = Rhombus(6, 8.5)
    expected = "Rhombus(diagonal_a=6, diagonal_b=8.5)"
    assert str(rhombus) == expected
    assert repr(rhombus) == expected


def test_rhombus_properties_are_immutable():
    rhombus = Rhombus(6, 8)

    with pytest.raises(AttributeError):
        rhombus.diagonal_a = 10
    with pytest.raises(AttributeError):
        rhombus.diagonal_b = 10


def test_rhombus_add_area_with_circle():
    rhombus = Rhombus(6, 8)
    circle = Circle(2)

    assert rhombus.add_area(circle) == pytest.approx(rhombus.area + circle.area)
