from math import pi

import pytest

from ..src.Annulus import Annulus
from ..src.Circle import Circle
from ..src.Figure import Figure
from ..src.Rectangle import Rectangle

pytestmark = pytest.mark.usefixtures("log_test_case")


@pytest.mark.parametrize(
    "outer_radius, inner_radius, expected_area",
    [
        (3, 1, 8 * pi),
        (5, 4, 9 * pi),
        (2.5, 1.5, 4 * pi),
        (1, 0, pi),
    ],
)
def test_annulus_area_is_difference_of_circle_areas(outer_radius, inner_radius, expected_area):
    annulus = Annulus(outer_radius, inner_radius)
    assert annulus.area == pytest.approx(expected_area)
    assert isinstance(annulus.area, (int, float))


@pytest.mark.parametrize(
    "outer_radius, inner_radius, expected_perimeter",
    [
        (3, 1, 8 * pi),
        (2.5, 1.5, 8 * pi),
        (1, 0, 2 * pi),
    ],
)
def test_annulus_perimeter_is_sum_of_both_circumferences(outer_radius, inner_radius, expected_perimeter):
    annulus = Annulus(outer_radius, inner_radius)
    assert annulus.perimeter == pytest.approx(expected_perimeter)


def test_annulus_width_is_difference_of_radii():
    assert Annulus(5, 3.5).width == pytest.approx(1.5)


def test_annulus_has_name():
    assert Annulus(3, 1).name == "Annulus"


def test_annulus_is_figure_instance():
    assert isinstance(Annulus(3, 1), Figure)


@pytest.mark.parametrize("outer_radius, inner_radius", [("aaa", 1), (3, None), (2, "*&^")])
def test_create_annulus_with_non_numeric_radii_raises_type_error(outer_radius, inner_radius):
    with pytest.raises(TypeError, match="Radii should be numeric"):
        Annulus(outer_radius, inner_radius)


@pytest.mark.parametrize("outer_radius, inner_radius", [(3, -1), (-3, -4), (-1, -2)])
def test_create_annulus_with_negative_radii_raises_value_error(outer_radius, inner_radius):
    with pytest.raises(ValueError, match="Radii should be >= 0"):
        Annulus(outer_radius, inner_radius)


@pytest.mark.parametrize("outer_radius, inner_radius", [(3, 3), (2, 5), (0, 0)])
def test_create_annulus_with_inner_radius_not_less_than_outer_raises_value_error(outer_radius, inner_radius):
    with pytest.raises(ValueError, match="Inner radius should be less than outer radius"):
        Annulus(outer_radius, inner_radius)


def test_annulus_with_zero_inner_radius_matches_circle():
    radius = 5
    annulus = Annulus(radius, 0)
    circle = Circle(radius)

    assert annulus.area == pytest.approx(circle.area)
    assert annulus.perimeter == pytest.approx(circle.perimeter)


def test_annulus_add_area_with_annulus_returns_sum_of_areas():
    annulus1 = Annulus(3, 1)
    annulus2 = Annulus(5, 4)
    assert annulus1.add_area(annulus2) == pytest.approx(annulus1.area + annulus2.area)


def test_annulus_add_area_with_different_figure_returns_sum_of_areas(create_rectangle):
    annulus = Annulus(3, 1)
    assert annulus.add_area(create_rectangle) == pytest.approx(annulus.area + create_rectangle.area)


def test_annulus_add_area_with_invalid_argument_raises_value_error():
    annulus = Annulus(3, 1)

    with pytest.raises(ValueError, match="Cannot add area of"):
        annulus.add_area("not a figure")


def test_annuli_with_same_radii_are_equal_and_hash_equally():
    annulus1 = Annulus(3, 1)
    annulus2 = Annulus(3, 1)
    annulus3 = Annulus(3, 2)

    assert annulus1 == annulus2
    assert hash(annulus1) == hash(annulus2)
    assert annulus1 != annulus3
    assert hash(annulus1) != hash(annulus3)
    assert Annulus(3, 0) != Circle(3)


def test_annulus_comparison_operators_compare_by_area():
    smaller = Annulus(3, 1)
    larger = Annulus(5, 4)
    equal = Annulus(3, 1)

    assert smaller < larger
    assert larger > smaller
    assert smaller <= equal
    assert smaller <= larger
    assert larger >= smaller
    assert smaller >= equal


def test_annulus_ordering_rejects_non_annuli():
    annulus = Annulus(3, 1)

    with pytest.raises(TypeError, match="Cannot compare Annulus with non-Annulus object"):
        annulus < Rectangle(2, 3)


def test_annulus_str_and_repr_list_both_radii():
    annulus = Annulus(3, 1.5)
    expected = "Annulus(outer_radius=3, inner_radius=1.5)"
    assert str(annulus) == expected
    assert repr(annulus) == expected


@pytest.mark.parametrize("attribute", ["outer_radius", "inner_radius", "width"])
def test_annulus_properties_are_immutable(attribute):
    annulus = Annulus(3, 1)

    with pytest.raises(AttributeError):
        setattr(annulus, attribute, 10)
