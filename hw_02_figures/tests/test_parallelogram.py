from math import asin, degrees

import pytest

from ..src.Circle import Circle
from ..src.Figure import Figure
from ..src.Parallelogram import Parallelogram
from ..src.Rectangle import Rectangle
from ..src.Rhombus import Rhombus
from ..src.Square import Square

pytestmark = pytest.mark.usefixtures("log_test_case")


@pytest.mark.parametrize(
    "side_a, side_b, angle, expected_area",
    [
        (4, 3, 30, 6),
        (5, 2, 90, 10),
        (2.5, 4, 150, 5),
    ],
)
def test_parallelogram_area_is_sides_product_times_angle_sine(side_a, side_b, angle, expected_area):
    parallelogram = Parallelogram(side_a, side_b, angle)
    assert parallelogram.area == pytest.approx(expected_area)
    assert isinstance(parallelogram.area, (int, float))


@pytest.mark.parametrize(
    "side_a, side_b, angle, expected_perimeter",
    [
        (4, 3, 30, 14),
        (2.5, 4, 150, 13),
    ],
)
def test_parallelogram_perimeter_is_twice_sides_sum(side_a, side_b, angle, expected_perimeter):
    parallelogram = Parallelogram(side_a, side_b, angle)
    assert parallelogram.perimeter == pytest.approx(expected_perimeter)


def test_parallelogram_height_is_side_b_times_angle_sine():
    assert Parallelogram(4, 3, 30).height == pytest.approx(1.5)


def test_parallelogram_with_supplementary_angles_has_same_area():
    assert Parallelogram(4, 3, 60).area == pytest.approx(Parallelogram(4, 3, 120).area)


def test_parallelogram_has_name():
    assert Parallelogram(4, 3, 30).name == "Parallelogram"


def test_parallelogram_is_figure_instance():
    assert isinstance(Parallelogram(4, 3, 30), Figure)


@pytest.mark.parametrize("params", [("aaa", 3, 30), (4, None, 30), (4, 3, "*&^")])
def test_create_parallelogram_with_non_numeric_parameters_raises_type_error(params):
    with pytest.raises(TypeError, match="Parallelogram parameters should be numeric"):
        Parallelogram(*params)


@pytest.mark.parametrize("side_a, side_b", [(0, 3), (4, 0), (-4, 3), (4, -3)])
def test_create_parallelogram_with_non_positive_sides_raises_value_error(side_a, side_b):
    with pytest.raises(ValueError, match="Parallelogram sides should be > 0"):
        Parallelogram(side_a, side_b, 30)


@pytest.mark.parametrize("angle", [0, 180, -30, 200])
def test_create_parallelogram_with_angle_outside_open_range_raises_value_error(angle):
    with pytest.raises(ValueError, match="Parallelogram angle should be between 0 and 180 degrees"):
        Parallelogram(4, 3, angle)


def test_parallelogram_with_right_angle_matches_rectangle():
    parallelogram = Parallelogram(5, 2, 90)
    rectangle = Rectangle(5, 2)

    assert parallelogram.area == pytest.approx(rectangle.area)
    assert parallelogram.perimeter == pytest.approx(rectangle.perimeter)


def test_parallelogram_with_equal_sides_and_right_angle_matches_square():
    parallelogram = Parallelogram(4, 4, 90)
    square = Square(4)

    assert parallelogram.area == pytest.approx(square.area)
    assert parallelogram.perimeter == pytest.approx(square.perimeter)


def test_parallelogram_with_equal_sides_matches_rhombus():
    # Rhombus(6, 8) has side 5 and area 24, so sin(angle) = 24 / 25
    parallelogram = Parallelogram(5, 5, degrees(asin(24 / 25)))
    rhombus = Rhombus(6, 8)

    assert parallelogram.area == pytest.approx(rhombus.area)
    assert parallelogram.perimeter == pytest.approx(rhombus.perimeter)


def test_parallelogram_add_area_with_parallelogram_returns_sum_of_areas():
    parallelogram1 = Parallelogram(4, 3, 30)
    parallelogram2 = Parallelogram(5, 2, 90)
    assert parallelogram1.add_area(parallelogram2) == pytest.approx(parallelogram1.area + parallelogram2.area)


def test_parallelogram_add_area_with_different_figure_returns_sum_of_areas(create_rectangle):
    parallelogram = Parallelogram(4, 3, 30)
    assert parallelogram.add_area(create_rectangle) == pytest.approx(parallelogram.area + create_rectangle.area)


def test_parallelogram_add_area_with_invalid_argument_raises_value_error():
    parallelogram = Parallelogram(4, 3, 30)

    with pytest.raises(ValueError, match="Cannot add area of"):
        parallelogram.add_area("not a figure")


def test_parallelograms_with_same_parameters_are_equal_and_hash_equally():
    parallelogram1 = Parallelogram(4, 3, 30)
    parallelogram2 = Parallelogram(4, 3, 30)
    parallelogram3 = Parallelogram(4, 3, 60)

    assert parallelogram1 == parallelogram2
    assert hash(parallelogram1) == hash(parallelogram2)
    assert parallelogram1 != parallelogram3
    assert hash(parallelogram1) != hash(parallelogram3)
    assert Parallelogram(5, 2, 90) != Rectangle(5, 2)


def test_parallelogram_comparison_operators_compare_by_area():
    smaller = Parallelogram(4, 3, 30)
    larger = Parallelogram(5, 2, 90)
    equal = Parallelogram(4, 3, 30)

    assert smaller < larger
    assert larger > smaller
    assert smaller <= equal
    assert smaller <= larger
    assert larger >= smaller
    assert smaller >= equal


def test_parallelogram_ordering_rejects_non_parallelograms():
    parallelogram = Parallelogram(4, 3, 30)

    with pytest.raises(TypeError, match="Cannot compare Parallelogram with non-Parallelogram object"):
        parallelogram < Circle(2)


def test_parallelogram_str_and_repr_list_all_parameters():
    parallelogram = Parallelogram(4, 3.5, 45)
    expected = "Parallelogram(side_a=4, side_b=3.5, angle=45)"
    assert str(parallelogram) == expected
    assert repr(parallelogram) == expected


@pytest.mark.parametrize("attribute", ["side_a", "side_b", "angle", "height"])
def test_parallelogram_properties_are_immutable(attribute):
    parallelogram = Parallelogram(4, 3, 30)

    with pytest.raises(AttributeError):
        setattr(parallelogram, attribute, 10)
