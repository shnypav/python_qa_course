from math import pi, sqrt

import pytest

from ..src.Circle import Circle
from ..src.Ellipse import Ellipse
from ..src.Figure import Figure


@pytest.mark.parametrize("semi_major, semi_minor, expected_area", [
    (3, 2, 6 * pi),
    (1, 1, pi),
    (2.5, 0.5, 1.25 * pi),
])
def test_ellipse_area(semi_major, semi_minor, expected_area):
    ellipse = Ellipse(semi_major, semi_minor)
    assert ellipse.area == pytest.approx(expected_area)


@pytest.mark.parametrize("semi_major, semi_minor", [(3, 2), (5, 1), (2.5, 0.5)])
def test_ellipse_perimeter_matches_ramanujan_formula(semi_major, semi_minor):
    ellipse = Ellipse(semi_major, semi_minor)
    a, b = semi_major, semi_minor
    expected = pi * (3 * (a + b) - sqrt((3 * a + b) * (a + 3 * b)))
    assert ellipse.perimeter == pytest.approx(expected)


def test_ellipse_with_equal_axes_matches_circle():
    """An ellipse with equal semi-axes degenerates into a circle"""
    ellipse = Ellipse(4, 4)
    circle = Circle(4)
    assert ellipse.area == pytest.approx(circle.area)
    assert ellipse.perimeter == pytest.approx(circle.perimeter)


def test_ellipse_has_name(create_ellipse):
    assert create_ellipse.name == "Ellipse"


def test_ellipse_is_figure(create_ellipse):
    assert isinstance(create_ellipse, Figure)


@pytest.mark.parametrize("semi_major, semi_minor", [("aaa", 2), (3, "*&^"), (None, 2), (3, None)])
def test_create_ellipse_with_invalid_types(semi_major, semi_minor):
    with pytest.raises(TypeError) as error:
        Ellipse(semi_major, semi_minor)
    assert error.value.args[0] == "Semi-axes should be numeric"


@pytest.mark.parametrize("semi_major, semi_minor", [(0, 2), (3, 0), (-3, 2), (3, -2)])
def test_create_ellipse_with_non_positive_axes(semi_major, semi_minor):
    with pytest.raises(ValueError) as error:
        Ellipse(semi_major, semi_minor)
    assert error.value.args[0] == "Ellipse semi-axes should be > 0"


def test_ellipse_add_area(create_ellipse, create_circle):
    # default figures from conftest.py: ellipse = 6 * pi, circle = 0
    assert create_ellipse.add_area(create_circle) == pytest.approx(6 * pi)


def test_ellipse_equality():
    assert Ellipse(3, 2) == Ellipse(3, 2)
    assert Ellipse(3, 2) != Ellipse(2, 3)
    assert Ellipse(3, 2) != (3, 2)


def test_ellipse_str(create_ellipse):
    assert str(create_ellipse) == "Ellipse(semi_major=3, semi_minor=2)"
