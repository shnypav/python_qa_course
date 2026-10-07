from math import sqrt

import pytest

from ..src.Circle import Circle
from ..src.Figure import Figure
from ..src.RegularPolygon import RegularPolygon
from ..src.Square import Square
from ..src.Triangle import Triangle

pytestmark = pytest.mark.usefixtures("log_test_case")


@pytest.mark.parametrize(
    "sides_count, side_length, expected_area",
    [
        (3, 2, sqrt(3)),
        (4, 3, 9),
        (4, 2.5, 6.25),
        (6, 2, 6 * sqrt(3)),
    ],
)
def test_regular_polygon_area_matches_apothem_formula(sides_count, side_length, expected_area):
    polygon = RegularPolygon(sides_count, side_length)
    assert polygon.area == pytest.approx(expected_area)
    assert isinstance(polygon.area, (int, float))


@pytest.mark.parametrize(
    "sides_count, side_length, expected_perimeter",
    [
        (3, 2, 6),
        (5, 1.5, 7.5),
        (8, 4, 32),
    ],
)
def test_regular_polygon_perimeter_is_sides_count_times_side_length(sides_count, side_length, expected_perimeter):
    polygon = RegularPolygon(sides_count, side_length)
    assert polygon.perimeter == pytest.approx(expected_perimeter)


@pytest.mark.parametrize(
    "sides_count, expected_angle",
    [(3, 60), (4, 90), (6, 120), (8, 135)],
)
def test_regular_polygon_interior_angle_depends_on_sides_count(sides_count, expected_angle):
    assert RegularPolygon(sides_count, 1).interior_angle == pytest.approx(expected_angle)


def test_regular_polygon_has_name():
    assert RegularPolygon(5, 1).name == "RegularPolygon"


def test_regular_polygon_is_figure_instance():
    assert isinstance(RegularPolygon(5, 1), Figure)


@pytest.mark.parametrize("sides_count", [4.0, "6", None])
def test_create_regular_polygon_with_non_integer_sides_count_raises_type_error(sides_count):
    with pytest.raises(TypeError, match="Number of sides should be an integer"):
        RegularPolygon(sides_count, 1)


@pytest.mark.parametrize("side_length", ["aaa", None, "*&^"])
def test_create_regular_polygon_with_non_numeric_side_length_raises_type_error(side_length):
    with pytest.raises(TypeError, match="Side length should be numeric"):
        RegularPolygon(4, side_length)


@pytest.mark.parametrize("sides_count", [2, 0, -3])
def test_create_regular_polygon_with_fewer_than_three_sides_raises_value_error(sides_count):
    with pytest.raises(ValueError, match="Regular polygon should have at least 3 sides"):
        RegularPolygon(sides_count, 1)


@pytest.mark.parametrize("side_length", [0, -1, -2.5])
def test_create_regular_polygon_with_non_positive_side_length_raises_value_error(side_length):
    with pytest.raises(ValueError, match="Side length should be > 0"):
        RegularPolygon(4, side_length)


def test_regular_polygon_with_four_sides_matches_square():
    polygon = RegularPolygon(4, 3)
    square = Square(3)

    assert polygon.area == pytest.approx(square.area)
    assert polygon.perimeter == pytest.approx(square.perimeter)


def test_regular_polygon_with_three_sides_matches_equilateral_triangle():
    polygon = RegularPolygon(3, 5)
    triangle = Triangle(5, 5, 5)

    assert polygon.area == pytest.approx(triangle.area)
    assert polygon.perimeter == pytest.approx(triangle.perimeter)


def test_regular_polygon_add_area_with_regular_polygon_returns_sum_of_areas():
    polygon1 = RegularPolygon(6, 2)
    polygon2 = RegularPolygon(4, 3)
    assert polygon1.add_area(polygon2) == pytest.approx(polygon1.area + polygon2.area)


def test_regular_polygon_add_area_with_different_figure_returns_sum_of_areas(create_rectangle):
    polygon = RegularPolygon(6, 2)
    assert polygon.add_area(create_rectangle) == pytest.approx(polygon.area + create_rectangle.area)


def test_regular_polygon_add_area_with_invalid_argument_raises_value_error():
    polygon = RegularPolygon(6, 2)

    with pytest.raises(ValueError, match="Cannot add area of"):
        polygon.add_area("not a figure")


def test_regular_polygons_with_same_parameters_are_equal_and_hash_equally():
    polygon1 = RegularPolygon(6, 2)
    polygon2 = RegularPolygon(6, 2)
    polygon3 = RegularPolygon(6, 3)

    assert polygon1 == polygon2
    assert hash(polygon1) == hash(polygon2)
    assert polygon1 != polygon3
    assert hash(polygon1) != hash(polygon3)
    assert RegularPolygon(4, 3) != Square(3)


def test_regular_polygon_comparison_operators_compare_by_area():
    smaller = RegularPolygon(4, 3)
    larger = RegularPolygon(6, 2)
    equal = RegularPolygon(4, 3)

    assert smaller < larger
    assert larger > smaller
    assert smaller <= equal
    assert smaller <= larger
    assert larger >= smaller
    assert smaller >= equal


def test_regular_polygon_ordering_rejects_non_regular_polygons():
    polygon = RegularPolygon(4, 3)

    with pytest.raises(TypeError, match="Cannot compare RegularPolygon with non-RegularPolygon object"):
        polygon < Circle(2)


def test_regular_polygon_str_and_repr_list_both_parameters():
    polygon = RegularPolygon(5, 1.5)
    expected = "RegularPolygon(sides_count=5, side_length=1.5)"
    assert str(polygon) == expected
    assert repr(polygon) == expected


@pytest.mark.parametrize("attribute", ["sides_count", "side_length", "interior_angle"])
def test_regular_polygon_properties_are_immutable(attribute):
    polygon = RegularPolygon(4, 3)

    with pytest.raises(AttributeError):
        setattr(polygon, attribute, 10)
