import logging
import operator

import pytest

from ..src.Circle import Circle
from ..src.Figure import Figure
from ..src.RegularPolygon import RegularPolygon
from ..src.Square import Square
from ..src.Triangle import Triangle

pytestmark = pytest.mark.usefixtures("log_test_case")

INVALID_CONSTRUCTIONS = [
    ((6.0, 2), TypeError, "RegularPolygon sides should be an integer"),
    (("6", 2), TypeError, "RegularPolygon sides should be an integer"),
    ((None, 2), TypeError, "RegularPolygon sides should be an integer"),
    ((2, 2), ValueError, "RegularPolygon sides should be >= 3"),
    ((0, 2), ValueError, "RegularPolygon sides should be >= 3"),
    ((-5, 2), ValueError, "RegularPolygon sides should be >= 3"),
    ((6, "2"), TypeError, "RegularPolygon side length should be numeric"),
    ((6, None), TypeError, "RegularPolygon side length should be numeric"),
    ((6, [2]), TypeError, "RegularPolygon side length should be numeric"),
    ((6, 0), ValueError, "RegularPolygon side length should be > 0"),
    ((6, -1), ValueError, "RegularPolygon side length should be > 0"),
    ((6, -0.5), ValueError, "RegularPolygon side length should be > 0"),
]


@pytest.mark.parametrize(
    "params, expected_area",
    [
        ((6, 2), 10.392304845413264),
        ((5, 1), 1.720477400588967),
        ((8, 1.5), 10.863961030678928),
    ],
)
def test_regular_polygon_area_is_n_a_squared_over_four_tan_pi_over_n(params, expected_area):
    assert RegularPolygon(*params).area == pytest.approx(expected_area)


@pytest.mark.parametrize(
    "params, expected_perimeter",
    [((6, 2), 12), ((5, 1), 5), ((8, 1.5), 12)],
)
def test_regular_polygon_perimeter_is_sides_times_side_length(params, expected_perimeter):
    assert RegularPolygon(*params).perimeter == pytest.approx(expected_perimeter)


@pytest.mark.parametrize("side", [3, 2.5])
def test_regular_polygon_with_four_sides_matches_square(side):
    polygon = RegularPolygon(4, side)
    square = Square(side)

    assert polygon.area == pytest.approx(square.area)
    assert polygon.perimeter == pytest.approx(square.perimeter)


@pytest.mark.parametrize("side", [3, 2.5])
def test_regular_polygon_with_three_sides_matches_equilateral_triangle(side):
    polygon = RegularPolygon(3, side)
    triangle = Triangle(side, side, side)

    assert polygon.area == pytest.approx(triangle.area)
    assert polygon.perimeter == pytest.approx(triangle.perimeter)


def test_regular_polygon_follows_figure_contract():
    polygon = RegularPolygon(6, 2)

    assert isinstance(polygon, Figure)
    assert polygon.name == "RegularPolygon"
    assert isinstance(polygon.area, (int, float))
    assert isinstance(polygon.perimeter, (int, float))


@pytest.mark.parametrize("sides", [6.0, "6", None])
def test_create_regular_polygon_with_non_integer_sides_raises_type_error(sides):
    with pytest.raises(TypeError, match="RegularPolygon sides should be an integer"):
        RegularPolygon(sides, 2)


@pytest.mark.parametrize("sides", [2, 0, -5])
def test_create_regular_polygon_with_fewer_than_three_sides_raises_value_error(sides):
    with pytest.raises(ValueError, match="RegularPolygon sides should be >= 3"):
        RegularPolygon(sides, 2)


def test_create_regular_polygon_with_three_sides_is_accepted():
    assert RegularPolygon(3, 2).sides == 3


@pytest.mark.parametrize("side_length", ["2", None, [2]])
def test_create_regular_polygon_with_non_numeric_side_length_raises_type_error(side_length):
    with pytest.raises(TypeError, match="RegularPolygon side length should be numeric"):
        RegularPolygon(6, side_length)


@pytest.mark.parametrize("side_length", [0, -1, -0.5])
def test_create_regular_polygon_with_non_positive_side_length_raises_value_error(side_length):
    with pytest.raises(ValueError, match="RegularPolygon side length should be > 0"):
        RegularPolygon(6, side_length)


@pytest.mark.parametrize(
    "params, error, message",
    [
        ((2, -1), ValueError, "RegularPolygon sides should be >= 3"),
        ((6.0, "2"), TypeError, "RegularPolygon sides should be an integer"),
    ],
)
def test_create_regular_polygon_with_both_arguments_invalid_reports_sides_error(params, error, message):
    with pytest.raises(error, match=message):
        RegularPolygon(*params)


@pytest.mark.parametrize("params, error, message", INVALID_CONSTRUCTIONS)
def test_rejected_regular_polygon_construction_logs_error(caplog, params, error, message):
    with caplog.at_level(logging.ERROR, logger="hw_02_figures"):
        with pytest.raises(error, match=message):
            RegularPolygon(*params)

    assert any(
        record.levelno == logging.ERROR and record.name == "hw_02_figures"
        for record in caplog.records
    )


def test_regular_polygon_str_and_repr_list_sides_and_side_length():
    polygon = RegularPolygon(6, 2.5)
    expected = "RegularPolygon(sides=6, side_length=2.5)"

    assert str(polygon) == expected
    assert repr(polygon) == expected


def test_regular_polygons_with_same_parameters_are_equal_and_hash_equally():
    polygon1 = RegularPolygon(6, 2)
    polygon2 = RegularPolygon(6, 2)

    assert polygon1 == polygon2
    assert hash(polygon1) == hash(polygon2)
    assert polygon1 != RegularPolygon(5, 2)
    assert polygon1 != RegularPolygon(6, 3)


def test_regular_polygon_is_not_equal_to_other_objects():
    assert RegularPolygon(4, 2) != Square(2)
    assert (RegularPolygon(4, 2) == "not a figure") is False
    assert (RegularPolygon(4, 2) == 8) is False


def test_regular_polygon_comparison_operators_compare_by_area():
    smaller = RegularPolygon(5, 1)
    larger = RegularPolygon(6, 2)
    equal = RegularPolygon(5, 1)

    assert smaller < larger
    assert larger > smaller
    assert smaller <= equal
    assert smaller <= larger
    assert larger >= smaller
    assert smaller >= equal
    assert not smaller < equal
    assert not smaller > equal


@pytest.mark.parametrize("compare", [operator.lt, operator.gt, operator.le, operator.ge])
@pytest.mark.parametrize("other", [Circle(2), 5])
def test_regular_polygon_ordering_rejects_non_regular_polygons(compare, other):
    with pytest.raises(TypeError, match="Cannot compare RegularPolygon with non-RegularPolygon object"):
        compare(RegularPolygon(6, 2), other)


def test_regular_polygon_add_area_with_regular_polygon_returns_sum_of_areas():
    polygon1 = RegularPolygon(6, 2)
    polygon2 = RegularPolygon(5, 1)

    assert polygon1.add_area(polygon2) == pytest.approx(polygon1.area + polygon2.area)


def test_regular_polygon_add_area_with_different_figure_returns_sum_of_areas(create_rectangle):
    polygon = RegularPolygon(6, 2)

    assert polygon.add_area(create_rectangle) == pytest.approx(polygon.area + create_rectangle.area)


def test_regular_polygon_add_area_with_invalid_argument_raises_value_error():
    with pytest.raises(ValueError, match="Cannot add area of"):
        RegularPolygon(6, 2).add_area("not a figure")


@pytest.mark.parametrize("attribute", ["sides", "side_length", "area", "perimeter"])
def test_regular_polygon_properties_are_read_only(attribute):
    polygon = RegularPolygon(6, 2)

    with pytest.raises(AttributeError):
        setattr(polygon, attribute, 10)
