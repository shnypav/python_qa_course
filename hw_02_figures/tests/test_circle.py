from math import pi

import pytest

from ..src.Circle import Circle
from ..src.Figure import Figure


@pytest.mark.parametrize("radius, expected_area", [(0, 0), (10, 100 * pi), (2.5, (2.5 ** 2) * pi)])
def test_circle_area(radius, expected_area):
    circle = Circle(radius)
    assert circle.area == expected_area
    assert isinstance(circle.area, (int, float))


@pytest.mark.parametrize("radius, expected_perimeter", [(0, 0), (10, 2 * pi * 10)])
def test_circle_perimeter(radius, expected_perimeter):
    circle = Circle(radius)
    assert circle.perimeter == expected_perimeter


def test_circle_has_name(create_circle):
    assert create_circle.name == "Circle"


# not sure if it makes any sense to check this
def test_circle_is_instance():
    assert isinstance(Circle.__class__, Figure.__class__)


@pytest.mark.parametrize("radius", ["aaa", "*&^", "", None])
def test_create_circle_with_invalid_radius(radius):
    with pytest.raises(TypeError) as error:
        Circle(radius)
    assert error.type is TypeError


def test_create_circle_radius_less_than_zero():
    with pytest.raises(ValueError) as error:
        Circle(-1)
    assert error.type is ValueError
    assert error.value.args[0] == "Radius should be >= 0"


def test_circle_add_area():
    """Test adding areas of two circles"""
    circle1 = Circle(5)
    circle2 = Circle(10)
    expected_area = circle1.area + circle2.area
    assert circle1.add_area(circle2) == expected_area


def test_circle_add_area_with_different_figure(create_square):
    """Test adding area of a circle with a different figure type"""
    circle = Circle(5)
    expected_area = circle.area + create_square.area
    assert circle.add_area(create_square) == expected_area


@pytest.mark.parametrize("radius", [1e6, 1e9])
def test_circle_with_large_radius(radius):
    """Test creating circles with very large radius values"""
    circle = Circle(radius)
    assert circle.area == pi * (radius ** 2)
    assert circle.perimeter == 2 * pi * radius


def test_circle_with_float_in_string():
    """Test that a string that represents a valid float is rejected"""
    with pytest.raises(TypeError):
        Circle("10.5")


def test_circle_zero_radius():
    """Test that a circle with zero radius has specific properties"""
    circle = Circle(0)
    assert circle.area == 0
    assert circle.perimeter == 0
    assert isinstance(circle, Circle)


def test_circle_diameter():
    """Test calculating circle diameter"""
    circle = Circle(5)
    expected_diameter = 10
    assert circle.diameter == expected_diameter


def test_circle_with_very_small_radius():
    """Test creating circles with very small radius values"""
    # Test with a very small (but valid) radius
    small_radius = 1e-10
    circle = Circle(small_radius)
    assert circle.area == pytest.approx(pi * (small_radius ** 2))
    assert circle.perimeter == pytest.approx(2 * pi * small_radius)


def test_circle_equality():
    """Test that circles with the same radius are equal"""
    circle1 = Circle(5)
    circle2 = Circle(5)
    # Currently they would be different objects but equal in radius
    assert circle1.radius == circle2.radius
    # Now we can check equality
    assert circle1 == circle2
    # Also check inequality
    circle3 = Circle(10)
    print("hello")
    assert circle1 != circle3


def test_circle_repr():
    """Test the string representation of a circle"""
    circle = Circle(5)
    # Check the string representation includes the name and radius
    assert str(circle) == "Circle(radius=5)"
    # Different radius
    circle2 = Circle(10)
    assert str(circle2) == "Circle(radius=10)"


def test_circle_hash():
    """Test that circles with the same radius have the same hash"""
    circle1 = Circle(5)
    circle2 = Circle(5)
    assert hash(circle1) == hash(circle2)
    # Different radius should have different hash
    circle3 = Circle(10)
    assert hash(circle1) != hash(circle3)


def test_circle_comparison_operators():
    """Test comparison operators for circles"""
    circle1 = Circle(5)
    circle2 = Circle(10)
    circle3 = Circle(5)

    # Test less than
    assert circle1 < circle2
    # Test greater than
    assert circle2 > circle1
    # Test less than or equal
    assert circle1 <= circle3
    assert circle1 <= circle2
    # Test greater than or equal
    assert circle2 >= circle1
    assert circle1 >= circle3


def test_circle_add_area_with_invalid_argument():
    """Test adding area with an invalid argument"""
    circle = Circle(5)
    with pytest.raises(ValueError) as error:
        circle.add_area("not a figure")
    assert error.type is ValueError
    assert "Cannot add area of" in str(error.value)


def test_circle_properties_immutability():
    """Test that circle properties cannot be modified"""
    circle = Circle(5)
    with pytest.raises(AttributeError):
        circle.radius = 10
    with pytest.raises(AttributeError):
        circle.area = 100
    with pytest.raises(AttributeError):
        circle.perimeter = 100
    with pytest.raises(AttributeError):
        circle.diameter = 20


def test_circle_str_and_repr():
    """Test the string and representation methods"""
    circle = Circle(5)
    assert str(circle) == "Circle(radius=5)"
    assert repr(circle) == "Circle(radius=5)"

    # Test with different radius
    circle2 = Circle(10.5)
    assert str(circle2) == "Circle(radius=10.5)"
    assert repr(circle2) == "Circle(radius=10.5)"
