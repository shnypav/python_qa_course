from math import pi, sqrt

import pytest

from ..src.Circle import Circle
from ..src.Ellipse import Ellipse
from ..src.Figure import Figure
from ..src.Rectangle import Rectangle


@pytest.mark.parametrize(
    "semi_major_axis, semi_minor_axis, expected_area",
    [
        (0, 5, 0),
        (5, 0, 0),
        (3, 4, 12 * pi),
        (2.5, 2, 5 * pi),
    ],
)
def test_ellipse_area(semi_major_axis, semi_minor_axis, expected_area):
    ellipse = Ellipse(semi_major_axis, semi_minor_axis)
    assert ellipse.area == pytest.approx(expected_area)
    assert isinstance(ellipse.area, (int, float))


def test_ellipse_perimeter():
    ellipse = Ellipse(3, 4)
    expected = pi * (3 * (3 + 4) - sqrt((3 * 3 + 4) * (3 + 3 * 4)))
    assert ellipse.perimeter == pytest.approx(expected)


def test_ellipse_has_name():
    assert Ellipse(1, 2).name == "Ellipse"


def test_ellipse_is_figure_instance():
    assert isinstance(Ellipse(2, 3), Figure)


@pytest.mark.parametrize("semi_major_axis, semi_minor_axis", [("aaa", 1), (1, None), (2, "*&^")])
def test_create_ellipse_with_invalid_axes(semi_major_axis, semi_minor_axis):
    with pytest.raises(TypeError, match="Semi-axes should be numeric"):
        Ellipse(semi_major_axis, semi_minor_axis)


@pytest.mark.parametrize(
    "semi_major_axis, semi_minor_axis",
    [(-1, 2), (2, -1), (-3, -4)],
)
def test_create_ellipse_with_negative_axes(semi_major_axis, semi_minor_axis):
    with pytest.raises(ValueError, match="Semi-axes should be >= 0"):
        Ellipse(semi_major_axis, semi_minor_axis)


def test_ellipse_add_area_with_ellipse():
    ellipse1 = Ellipse(3, 4)
    ellipse2 = Ellipse(2, 5)
    assert ellipse1.add_area(ellipse2) == pytest.approx(ellipse1.area + ellipse2.area)


def test_ellipse_add_area_with_different_figure(create_rectangle):
    ellipse = Ellipse(3, 4)
    assert ellipse.add_area(create_rectangle) == pytest.approx(ellipse.area + create_rectangle.area)


def test_ellipse_matches_circle_when_axes_are_equal():
    radius = 5
    ellipse = Ellipse(radius, radius)
    circle = Circle(radius)

    assert ellipse.area == pytest.approx(circle.area)
    assert ellipse.perimeter == pytest.approx(circle.perimeter)


def test_ellipse_equality():
    ellipse1 = Ellipse(3, 4)
    ellipse2 = Ellipse(3, 4)
    ellipse3 = Ellipse(4, 3)

    assert ellipse1 == ellipse2
    assert ellipse1 != ellipse3
    assert ellipse1 != Circle(3)


def test_ellipse_hash():
    ellipse1 = Ellipse(3, 4)
    ellipse2 = Ellipse(3, 4)
    ellipse3 = Ellipse(4, 3)

    assert hash(ellipse1) == hash(ellipse2)
    assert hash(ellipse1) != hash(ellipse3)


def test_ellipse_comparison_operators():
    smaller = Ellipse(2, 3)
    larger = Ellipse(4, 5)
    equal = Ellipse(2, 3)

    assert smaller < larger
    assert larger > smaller
    assert smaller <= equal
    assert smaller <= larger
    assert larger >= smaller
    assert smaller >= equal


def test_ellipse_ordering_rejects_non_ellipses():
    ellipse = Ellipse(2, 3)

    with pytest.raises(TypeError, match="Cannot compare Ellipse with non-Ellipse object"):
        ellipse < Circle(2)


def test_ellipse_add_area_with_invalid_argument():
    ellipse = Ellipse(3, 4)

    with pytest.raises(ValueError, match="Cannot add area of"):
        ellipse.add_area("not a figure")


def test_ellipse_str_and_repr():
    ellipse = Ellipse(3, 4.5)
    expected = "Ellipse(semi_major_axis=3, semi_minor_axis=4.5)"
    assert str(ellipse) == expected
    assert repr(ellipse) == expected


def test_ellipse_properties_are_immutable():
    ellipse = Ellipse(3, 4)

    with pytest.raises(AttributeError):
        ellipse.semi_major_axis = 10
    with pytest.raises(AttributeError):
        ellipse.semi_minor_axis = 10


def test_ellipse_add_area_with_rectangle():
    ellipse = Ellipse(2, 3)
    rectangle = Rectangle(4, 5)

    assert ellipse.add_area(rectangle) == pytest.approx(ellipse.area + rectangle.area)
