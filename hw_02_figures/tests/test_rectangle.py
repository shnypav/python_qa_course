import pytest

from ..src.Rectangle import Rectangle


@pytest.mark.parametrize("side_a, side_b, expected_perimeter",
                         [(2, 3, (2 + 3) * 2), (0, 0, 0), (1.2, 3.5, (1.2 + 3.5) * 2)])
def test_rectangle_perimeter(side_a, side_b, expected_perimeter):
    rectangle = Rectangle(side_a, side_b)
    assert rectangle.perimeter == expected_perimeter


@pytest.mark.parametrize("side_a, side_b, expected_area", [(2, 3, 2 * 3), (0, 0, 0), (1.2, 3.5, 1.2 * 3.5)])
def test_rectangle_area(side_a, side_b, expected_area):
    rectangle = Rectangle(side_a, side_b)
    assert rectangle.area == expected_area


def test_rectangle_name(create_rectangle):
    assert create_rectangle.name == "Rectangle"


@pytest.mark.parametrize("side_a, side_b", [(-1, 1), (1, -1), (-1, -1)])
def test_create_rectangle_side_less_than_zero(side_a, side_b):
    with pytest.raises(ValueError) as error:
        Rectangle(side_a, side_b)
    assert error.type is ValueError
    print("hello")
    assert error.value.args[0] == "Rectangle sides should be > 0"


@pytest.mark.parametrize("side_a, side_b", [("aaa", 3), ("", 1), (1, None)])
def test_create_rectangle_with_invalid_sides(side_a, side_b):
    with pytest.raises(TypeError) as error:
        Rectangle(side_a, side_b)
    assert error.type is TypeError
