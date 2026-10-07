import pytest

from ..src.Circle import Circle
from ..src.Figure import Figure
from ..src.Rectangle import Rectangle
from ..src.Trapezoid import Trapezoid

pytestmark = pytest.mark.usefixtures("log_test_case")


@pytest.mark.parametrize(
    "params, expected_area",
    [
        ((10, 4, 5, 5, 4), 28),
        ((8, 5, 5, 4, 4), 26),
        ((6, 6, 5, 5, 4), 24),
        ((6.5, 2.5, 2.5, 2.5, 1.5), 6.75),
    ],
)
def test_trapezoid_area_is_half_bases_sum_times_height(params, expected_area):
    trapezoid = Trapezoid(*params)
    assert trapezoid.area == pytest.approx(expected_area)
    assert isinstance(trapezoid.area, (int, float))


@pytest.mark.parametrize(
    "params, expected_perimeter",
    [
        ((10, 4, 5, 5, 4), 24),
        ((8, 5, 5, 4, 4), 22),
        ((6.5, 2.5, 2.5, 2.5, 1.5), 14),
    ],
)
def test_trapezoid_perimeter_is_sum_of_all_sides(params, expected_perimeter):
    trapezoid = Trapezoid(*params)
    assert trapezoid.perimeter == pytest.approx(expected_perimeter)


def test_trapezoid_has_name():
    assert Trapezoid(10, 4, 5, 5, 4).name == "Trapezoid"


def test_trapezoid_is_figure_instance():
    assert isinstance(Trapezoid(10, 4, 5, 5, 4), Figure)


@pytest.mark.parametrize(
    "params",
    [("aaa", 4, 5, 5, 4), (10, None, 5, 5, 4), (10, 4, 5, 5, "*&^")],
)
def test_create_trapezoid_with_non_numeric_parameters_raises_type_error(params):
    with pytest.raises(TypeError, match="Trapezoid parameters should be numeric"):
        Trapezoid(*params)


@pytest.mark.parametrize(
    "params",
    [(0, 4, 5, 5, 4), (10, -4, 5, 5, 4), (10, 4, 0, 5, 4), (10, 4, 5, -5, 4), (10, 4, 5, 5, 0)],
)
def test_create_trapezoid_with_non_positive_parameters_raises_value_error(params):
    with pytest.raises(ValueError, match="Trapezoid parameters should be > 0"):
        Trapezoid(*params)


@pytest.mark.parametrize("params", [(10, 4, 3, 5, 4), (10, 4, 5, 3, 4)])
def test_create_trapezoid_with_height_longer_than_leg_raises_value_error(params):
    with pytest.raises(ValueError, match="Trapezoid height cannot exceed leg length"):
        Trapezoid(*params)


@pytest.mark.parametrize("params", [(10, 4, 5, 5, 3), (10, 4, 4, 4, 4), (6, 6, 5, 4, 4)])
def test_create_trapezoid_with_legs_not_joining_bases_raises_value_error(params):
    with pytest.raises(ValueError, match="Trapezoid dimensions are inconsistent"):
        Trapezoid(*params)


def test_trapezoid_with_equal_bases_and_vertical_legs_matches_rectangle():
    base, height = 7, 3
    trapezoid = Trapezoid(base, base, height, height, height)
    rectangle = Rectangle(base, height)

    assert trapezoid.area == pytest.approx(rectangle.area)
    assert trapezoid.perimeter == pytest.approx(rectangle.perimeter)


def test_trapezoid_add_area_with_trapezoid_returns_sum_of_areas():
    trapezoid1 = Trapezoid(10, 4, 5, 5, 4)
    trapezoid2 = Trapezoid(8, 5, 5, 4, 4)
    assert trapezoid1.add_area(trapezoid2) == pytest.approx(trapezoid1.area + trapezoid2.area)


def test_trapezoid_add_area_with_different_figure_returns_sum_of_areas(create_rectangle):
    trapezoid = Trapezoid(10, 4, 5, 5, 4)
    assert trapezoid.add_area(create_rectangle) == pytest.approx(trapezoid.area + create_rectangle.area)


def test_trapezoid_add_area_with_invalid_argument_raises_value_error():
    trapezoid = Trapezoid(10, 4, 5, 5, 4)

    with pytest.raises(ValueError, match="Cannot add area of"):
        trapezoid.add_area("not a figure")


def test_trapezoids_with_same_parameters_are_equal_and_hash_equally():
    trapezoid1 = Trapezoid(10, 4, 5, 5, 4)
    trapezoid2 = Trapezoid(10, 4, 5, 5, 4)
    trapezoid3 = Trapezoid(4, 10, 5, 5, 4)

    assert trapezoid1 == trapezoid2
    assert hash(trapezoid1) == hash(trapezoid2)
    assert trapezoid1 != trapezoid3
    assert hash(trapezoid1) != hash(trapezoid3)
    assert Trapezoid(4, 4, 2, 2, 2) != Rectangle(4, 2)


def test_trapezoid_comparison_operators_compare_by_area():
    smaller = Trapezoid(6, 6, 5, 5, 4)
    larger = Trapezoid(10, 4, 5, 5, 4)
    equal = Trapezoid(6, 6, 5, 5, 4)

    assert smaller < larger
    assert larger > smaller
    assert smaller <= equal
    assert smaller <= larger
    assert larger >= smaller
    assert smaller >= equal


def test_trapezoid_ordering_rejects_non_trapezoids():
    trapezoid = Trapezoid(10, 4, 5, 5, 4)

    with pytest.raises(TypeError, match="Cannot compare Trapezoid with non-Trapezoid object"):
        trapezoid < Circle(2)


def test_trapezoid_str_and_repr_list_all_parameters():
    trapezoid = Trapezoid(6.5, 2.5, 2.5, 2.5, 1.5)
    expected = "Trapezoid(base_a=6.5, base_b=2.5, leg_c=2.5, leg_d=2.5, height=1.5)"
    assert str(trapezoid) == expected
    assert repr(trapezoid) == expected


@pytest.mark.parametrize("attribute", ["base_a", "base_b", "leg_c", "leg_d", "height"])
def test_trapezoid_properties_are_immutable(attribute):
    trapezoid = Trapezoid(10, 4, 5, 5, 4)

    with pytest.raises(AttributeError):
        setattr(trapezoid, attribute, 10)
