import pytest

from ..src.Figure import Figure
from ..src.Rhombus import Rhombus


@pytest.mark.parametrize("side, height, expected_area", [
    (5, 4, 20),
    (3, 3, 9),
    (2.5, 1.5, 3.75),
])
def test_rhombus_area(side, height, expected_area):
    rhombus = Rhombus(side, height)
    assert rhombus.area == pytest.approx(expected_area)


@pytest.mark.parametrize("side, height, expected_perimeter", [
    (5, 4, 20),
    (3, 3, 12),
    (2.5, 1.5, 10),
])
def test_rhombus_perimeter(side, height, expected_perimeter):
    rhombus = Rhombus(side, height)
    assert rhombus.perimeter == pytest.approx(expected_perimeter)


def test_rhombus_has_name(create_rhombus):
    assert create_rhombus.name == "Rhombus"


def test_rhombus_is_figure(create_rhombus):
    assert isinstance(create_rhombus, Figure)


@pytest.mark.parametrize("side, height", [("aaa", 4), (5, "*&^"), (None, 4), (5, None)])
def test_create_rhombus_with_invalid_types(side, height):
    with pytest.raises(TypeError) as error:
        Rhombus(side, height)
    assert error.value.args[0] == "Side and height should be numeric"


@pytest.mark.parametrize("side, height", [(0, 4), (5, 0), (-5, 4), (5, -4)])
def test_create_rhombus_with_non_positive_dimensions(side, height):
    with pytest.raises(ValueError) as error:
        Rhombus(side, height)
    assert error.value.args[0] == "Rhombus side and height should be > 0"


def test_create_rhombus_with_height_greater_than_side():
    with pytest.raises(ValueError) as error:
        Rhombus(3, 5)
    assert error.value.args[0] == "Rhombus height cannot exceed its side"


def test_rhombus_add_area(create_rhombus, create_square):
    # default figures from conftest.py: rhombus = 20, square = 1
    assert create_rhombus.add_area(create_square) == 21


def test_rhombus_equality():
    assert Rhombus(5, 4) == Rhombus(5, 4)
    assert Rhombus(5, 4) != Rhombus(5, 3)
    assert Rhombus(5, 4) != (5, 4)


def test_rhombus_str(create_rhombus):
    assert str(create_rhombus) == "Rhombus(side=5, height=4)"
