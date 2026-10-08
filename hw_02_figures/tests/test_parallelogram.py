import pytest

from ..src.Circle import Circle
from ..src.Figure import Figure
from ..src.Parallelogram import Parallelogram
from ..src.Rectangle import Rectangle

pytestmark = pytest.mark.usefixtures("log_test_case")


@pytest.mark.parametrize(
    "params, expected_area",
    [
        ((10, 5, 4), 40),
        ((6, 3, 2), 12),
        ((7, 3, 3), 21),
        ((2.5, 4, 1.5), 3.75),
    ],
)
def test_parallelogram_area_is_side_a_times_height(params, expected_area):
    parallelogram = Parallelogram(*params)
    assert parallelogram.area == pytest.approx(expected_area)
    assert isinstance(parallelogram.area, (int, float))


@pytest.mark.parametrize(
    "params, expected_perimeter",
    [
        ((10, 5, 4), 30),
        ((6, 3, 2), 18),
        ((2.5, 4, 1.5), 13),
    ],
)
def test_parallelogram_perimeter_is_twice_sum_of_sides(params, expected_perimeter):
    parallelogram = Parallelogram(*params)
    assert parallelogram.perimeter == pytest.approx(expected_perimeter)


def test_parallelogram_has_name():
    assert Parallelogram(10, 5, 4).name == "Parallelogram"


def test_parallelogram_is_figure_instance():
    assert isinstance(Parallelogram(10, 5, 4), Figure)


@pytest.mark.parametrize("params", [("aaa", 5, 4), (10, None, 4), (10, 5, "*&^")])
def test_create_parallelogram_with_non_numeric_parameters_raises_type_error(params):
    with pytest.raises(TypeError, match="Parallelogram parameters should be numeric"):
        Parallelogram(*params)


@pytest.mark.parametrize("params", [(0, 5, 4), (-10, 5, 4), (10, 0, 4), (10, -5, 4), (10, 5, 0), (10, 5, -4)])
def test_create_parallelogram_with_non_positive_parameters_raises_value_error(params):
    with pytest.raises(ValueError, match="Parallelogram parameters should be > 0"):
        Parallelogram(*params)


@pytest.mark.parametrize("params", [(10, 5, 6), (10, 3.9, 4)])
def test_create_parallelogram_with_height_longer_than_side_b_raises_value_error(params):
    with pytest.raises(ValueError, match="Parallelogram height cannot exceed side_b"):
        Parallelogram(*params)


def test_parallelogram_with_height_equal_to_side_b_matches_rectangle():
    side_a, side_b = 7, 3
    parallelogram = Parallelogram(side_a, side_b, side_b)
    rectangle = Rectangle(side_a, side_b)

    assert parallelogram.area == pytest.approx(rectangle.area)
    assert parallelogram.perimeter == pytest.approx(rectangle.perimeter)


def test_parallelogram_add_area_with_parallelogram_returns_sum_of_areas():
    parallelogram1 = Parallelogram(10, 5, 4)
    parallelogram2 = Parallelogram(6, 3, 2)
    assert parallelogram1.add_area(parallelogram2) == pytest.approx(parallelogram1.area + parallelogram2.area)


def test_parallelogram_add_area_with_different_figure_returns_sum_of_areas(create_rectangle):
    parallelogram = Parallelogram(10, 5, 4)
    assert parallelogram.add_area(create_rectangle) == pytest.approx(parallelogram.area + create_rectangle.area)


def test_parallelogram_add_area_with_invalid_argument_raises_value_error():
    parallelogram = Parallelogram(10, 5, 4)

    with pytest.raises(ValueError, match="Cannot add area of"):
        parallelogram.add_area("not a figure")


def test_parallelograms_with_same_parameters_are_equal_and_hash_equally():
    parallelogram1 = Parallelogram(10, 5, 4)
    parallelogram2 = Parallelogram(10, 5, 4)
    parallelogram3 = Parallelogram(5, 10, 4)

    assert parallelogram1 == parallelogram2
    assert hash(parallelogram1) == hash(parallelogram2)
    assert parallelogram1 != parallelogram3
    assert hash(parallelogram1) != hash(parallelogram3)
    assert Parallelogram(4, 2, 2) != Rectangle(4, 2)


def test_parallelogram_comparison_operators_compare_by_area():
    smaller = Parallelogram(6, 3, 2)
    larger = Parallelogram(10, 5, 4)
    equal = Parallelogram(4, 5, 3)

    assert smaller < larger
    assert larger > smaller
    assert smaller <= equal
    assert smaller <= larger
    assert larger >= smaller
    assert smaller >= equal


def test_parallelogram_ordering_rejects_non_parallelograms():
    parallelogram = Parallelogram(10, 5, 4)

    with pytest.raises(TypeError, match="Cannot compare Parallelogram with non-Parallelogram object"):
        parallelogram < Circle(2)


def test_parallelogram_str_and_repr_list_all_parameters():
    parallelogram = Parallelogram(2.5, 4, 1.5)
    expected = "Parallelogram(side_a=2.5, side_b=4, height=1.5)"
    assert str(parallelogram) == expected
    assert repr(parallelogram) == expected


@pytest.mark.parametrize("attribute", ["side_a", "side_b", "height"])
def test_parallelogram_properties_are_immutable(attribute):
    parallelogram = Parallelogram(10, 5, 4)

    with pytest.raises(AttributeError):
        setattr(parallelogram, attribute, 10)
