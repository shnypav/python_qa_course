from math import sqrt

import pytest

from ..src.Figure import Figure
from ..src.Trapezoid import Trapezoid


@pytest.mark.parametrize("base_a, base_b, height, leg_c, leg_d, expected_area", [
    (10, 4, 4, 5, 5, 28),
    (8, 2, 3, 5, sqrt(13), 15),
    (7, 4, 4, 4, 5, 22),  # right trapezoid: leg_c is perpendicular to the bases
])
def test_trapezoid_area(base_a, base_b, height, leg_c, leg_d, expected_area):
    trapezoid = Trapezoid(base_a, base_b, height, leg_c, leg_d)
    assert trapezoid.area == pytest.approx(expected_area)


@pytest.mark.parametrize("base_a, base_b, height, leg_c, leg_d, expected_perimeter", [
    (10, 4, 4, 5, 5, 24),
    (8, 2, 3, 5, sqrt(13), 15 + sqrt(13)),
    (7, 4, 4, 4, 5, 20),
])
def test_trapezoid_perimeter(base_a, base_b, height, leg_c, leg_d, expected_perimeter):
    trapezoid = Trapezoid(base_a, base_b, height, leg_c, leg_d)
    assert trapezoid.perimeter == pytest.approx(expected_perimeter)


def test_trapezoid_has_name(create_trapezoid):
    assert create_trapezoid.name == "Trapezoid"


def test_trapezoid_is_figure(create_trapezoid):
    assert isinstance(create_trapezoid, Figure)


@pytest.mark.parametrize("dimensions", [
    ("aaa", 4, 4, 5, 5),
    (10, None, 4, 5, 5),
    (10, 4, "", 5, 5),
    (10, 4, 4, [], 5),
])
def test_create_trapezoid_with_invalid_types(dimensions):
    with pytest.raises(TypeError) as error:
        Trapezoid(*dimensions)
    assert error.value.args[0] == "All trapezoid dimensions should be numeric"


@pytest.mark.parametrize("dimensions", [
    (0, 4, 4, 5, 5),
    (10, -4, 4, 5, 5),
    (10, 4, 0, 5, 5),
    (10, 4, 4, -5, 5),
    (10, 4, 4, 5, 0),
])
def test_create_trapezoid_with_non_positive_dimensions(dimensions):
    with pytest.raises(ValueError) as error:
        Trapezoid(*dimensions)
    assert error.value.args[0] == "Trapezoid dimensions should be > 0"


@pytest.mark.parametrize("dimensions", [
    (10, 4, 5, 4, 5),  # leg_c shorter than height
    (10, 4, 5, 5, 4),  # leg_d shorter than height
])
def test_create_trapezoid_with_legs_shorter_than_height(dimensions):
    with pytest.raises(ValueError) as error:
        Trapezoid(*dimensions)
    assert error.value.args[0] == "Trapezoid legs cannot be shorter than its height"


@pytest.mark.parametrize("dimensions", [
    (10, 4, 4, 5, 4),  # projections add up to 3, bases differ by 6
    (5, 4, 3, 5, 5),   # projections add up to 8, bases differ by 1
])
def test_create_geometrically_impossible_trapezoid(dimensions):
    with pytest.raises(ValueError) as error:
        Trapezoid(*dimensions)
    assert error.value.args[0] == "Trapezoid dimensions are geometrically inconsistent"


def test_trapezoid_add_area(create_trapezoid, create_rectangle):
    # default figures from conftest.py: trapezoid = 28, rectangle = 2
    assert create_trapezoid.add_area(create_rectangle) == 30


def test_trapezoid_equality():
    assert Trapezoid(10, 4, 4, 5, 5) == Trapezoid(10, 4, 4, 5, 5)
    assert Trapezoid(10, 4, 4, 5, 5) != Trapezoid(7, 4, 4, 4, 5)
    assert Trapezoid(10, 4, 4, 5, 5) != (10, 4, 4, 5, 5)


def test_trapezoid_str(create_trapezoid):
    assert str(create_trapezoid) == "Trapezoid(base_a=10, base_b=4, height=4, leg_c=5, leg_d=5)"
