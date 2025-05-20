import pytest
import math
from ..src.Square import Square
from ..src.Rectangle import Rectangle
from ..src.Circle import Circle
from ..src.Triangle import Triangle


@pytest.mark.parametrize("side, expected_perimeter", [(0, 0), (2, 2 * 4)])
def test_square_perimeter(side, expected_perimeter):
    square = Square(side)
    assert square.perimeter == expected_perimeter


@pytest.mark.parametrize("side, expected_area", [(0, 0), (3, 3 * 3)])
def test_square_area(side, expected_area):
    square = Square(side)
    assert square.area == expected_area


def test_square_has_name(create_square):
    assert create_square.name == "Square"


def test_square_side_less_than_zero():
    with pytest.raises(ValueError) as error:
        Square(-1)
    assert error.type is ValueError
    assert error.value.args[0] == "Rectangle sides should be > 0"


@pytest.mark.parametrize("side", ["aaa", "", None])
def test_create_square_with_invalid_side(side):
    with pytest.raises(TypeError) as error:
        Square(side)
    assert error.type is TypeError


def test_square_add_area_with_circle():
    """Test adding area of a square with a circle"""
    square = Square(4)  # Area = 16
    circle = Circle(2)  # Area = 4π ≈ 12.57
    
    result = square.add_area(circle)
    expected = square.area + circle.area
    
    assert result == pytest.approx(expected)
    assert isinstance(result, (int, float))


def test_square_add_area_with_rectangle():
    """Test adding area of a square with a rectangle"""
    square = Square(5)        # Area = 25
    rectangle = Rectangle(2, 3)  # Area = 6
    
    result = square.add_area(rectangle)
    expected = square.area + rectangle.area
    
    assert result == expected
    assert isinstance(result, (int, float))


def test_square_add_area_with_triangle():
    """Test adding area of a square with a triangle"""
    square = Square(4)          # Area = 16
    triangle = Triangle(3, 4, 5)  # Area = 6
    
    result = square.add_area(triangle)
    expected = square.area + triangle.area
    
    assert result == expected
    assert isinstance(result, (int, float))


def test_square_add_area_with_invalid_object():
    """Test that adding area with an invalid object raises ValueError"""
    square = Square(3)
    
    with pytest.raises(ValueError) as error:
        square.add_area("not a figure")
    
    assert "Could not calculate area with argument given" in str(error.value)


def test_square_representation():
    """Test the string representation of a square"""
    # If Square doesn't have its own __str__ method, it will use Rectangle's
    # This test assumes a reasonable representation that includes the class name
    # and side value
    
    square = Square(5)
    representation = str(square)
    
    assert "Square" in representation or "Rectangle" in representation
    assert "5" in representation


def test_square_equality():
    """Test comparison between squares for equality"""
    # Same squares with same side
    square1 = Square(4)
    square2 = Square(4)
    # Different squares
    square3 = Square(5)
    square4 = Square(7)
    # A rectangle with the same sides as a square
    rectangle = Rectangle(4, 4)

    # Test equality between squares
    assert square1 == square2
    assert square1 != square3
    assert square2 != square4
    assert square3 != square4


def test_very_small_values():
    """Test square creation and calculations with very small values (precision test)"""
    # Use very small value
    small_side = 0.0000001
    square = Square(small_side)
    
    # Check that the square is created successfully
    assert isinstance(square, Square)
    
    # Check area with appropriate precision
    expected_area = small_side * small_side
    assert square.area == pytest.approx(expected_area)
    
    # Check perimeter
    expected_perimeter = 4 * small_side
    assert square.perimeter == pytest.approx(expected_perimeter)


def test_very_large_values():
    """Test square creation and calculations with very large values"""
    # Use very large value
    large_side = 1e9
    square = Square(large_side)
    
    # Check that the square is created successfully
    assert isinstance(square, Square)
    
    # Check area
    expected_area = large_side * large_side
    assert square.area == pytest.approx(expected_area)
    
    # Check perimeter
    expected_perimeter = 4 * large_side
    assert square.perimeter == pytest.approx(expected_perimeter)


def test_square_is_rectangle_with_equal_sides():
    """Test that Square is a special case of Rectangle with equal sides"""
    # Create a square
    side = 5
    square = Square(side)
    
    # Check that it's an instance of both Square and Rectangle
    assert isinstance(square, Square)
    assert isinstance(square, Rectangle)
    
    # Check that sides are equal
    assert square.side_a == square.side_b
    assert square.side_a == side
    
    # Check area and perimeter calculations are consistent with Rectangle
    assert square.area == side * side
    assert square.perimeter == 2 * (side + side)
    
    # Create an equivalent rectangle with equal sides
    rectangle = Rectangle(side, side)
    
    # Check area and perimeter match
    assert square.area == rectangle.area
    assert square.perimeter == rectangle.perimeter