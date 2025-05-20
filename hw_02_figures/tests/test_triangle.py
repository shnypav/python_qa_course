import pytest
import math
from ..src.Triangle import Triangle
from ..src.Circle import Circle
from ..src.Rectangle import Rectangle


def test_triangle_add_area_with_another_triangle():
    """Test adding area of a triangle with another triangle"""
    triangle1 = Triangle(3, 4, 5)  # Area = 6
    triangle2 = Triangle(5, 5, 6)  # Area = 12

    result = triangle1.add_area(triangle2)
    expected = 6 + 12

    assert result == expected
    assert isinstance(result, (int, float))

def test_triangle_is_equilateral():
    """Test checking if a triangle is equilateral"""
    # Equilateral triangle
    triangle = Triangle(5, 5, 5)

    # Check sides
    assert triangle.a == triangle.b == triangle.c

    # Check area calculation for equilateral triangle
    expected_area = (math.sqrt(3) / 4) * (5 ** 2)
    assert triangle.area == pytest.approx(expected_area)

def test_triangle_is_isosceles():
    """Test checking if a triangle is isosceles"""
    # Isosceles triangle
    triangle = Triangle(5, 5, 8)

    # Check that two sides are equal
    assert triangle.a == triangle.b != triangle.c

    # Calculate height to the unequal side
    s = (triangle.a + triangle.b + triangle.c) / 2
    area = math.sqrt(s * (s - triangle.a) * (s - triangle.b) * (s - triangle.c))
    height = 2 * area / triangle.c

    # Check area calculation
    assert triangle.area == pytest.approx(0.5 * triangle.c * height)

def test_triangle_is_right_angled():
    """Test checking if a triangle is right-angled (Pythagorean theorem)"""
    # Right-angled triangle (3-4-5)
    triangle = Triangle(3, 4, 5)

    # Check Pythagorean theorem
    assert triangle.a**2 + triangle.b**2 == pytest.approx(triangle.c**2)

    # Check area calculation for right-angled triangle
    assert triangle.area == pytest.approx(0.5 * 3 * 4)

def test_triangle_inequality_theorem():
    """Test that triangle inequality theorem is enforced"""
    # These should all fail because they violate the triangle inequality theorem
    invalid_cases = [
        (1, 1, 3),  # 1 + 1 < 3
        (2, 7, 3),  # 2 + 3 < 7
        (10, 3, 5)  # 3 + 5 < 10
    ]

    for a, b, c in invalid_cases:
        with pytest.raises(ValueError) as error:
            Triangle(a, b, c)
        assert "Triangle inequality theorem violated" in str(error.value)

def test_triangle_representation():
    """Test the string representation of a triangle"""
    triangle = Triangle(3, 4, 5)
    representation = str(triangle)

    assert "Triangle" in representation
    assert "3" in representation
    assert "4" in representation
    assert "5" in representation

def test_negative_side_values():
    """Test that creating a triangle with negative sides raises ValueError"""
    # Test cases with negative sides
    negative_cases = [
        (-1, 4, 5),
        (3, -4, 5),
        (3, 4, -5),
        (-3, -4, -5)
    ]

    for a, b, c in negative_cases:
        with pytest.raises(ValueError) as error:
            Triangle(a, b, c)
        assert "Triangle sides should be > 0" in str(error.value)

def test_non_numeric_side_values():
    """Test that creating a triangle with non-numeric sides raises TypeError"""
    # Test cases with non-numeric sides
    non_numeric_cases = [
        ("3", 4, 5),
        (3, "4", 5),
        (3, 4, "5"),
        ("a", "b", "c"),
        (None, 4, 5),
        ([1, 2], 3, 4),
        (3, {}, 5)
    ]

    for a, b, c in non_numeric_cases:
        with pytest.raises(TypeError) as error:
            Triangle(a, b, c)
        assert "All sides should be numeric" in str(error.value)

def test_perimeter_calculation():
    """Test the perimeter calculation of a triangle"""
    # Test cases with different triangles
    test_cases = [
        (3, 4, 5, 12),           # Right triangle
        (5, 5, 5, 15),           # Equilateral triangle
        (5, 5, 8, 18),           # Isosceles triangle
        (7, 8, 9, 24),           # Scalene triangle
        (10.5, 12.5, 13.5, 36.5) # Decimal values
    ]

    for a, b, c, expected_perimeter in test_cases:
        triangle = Triangle(a, b, c)
        assert triangle.perimeter == expected_perimeter
        # Also test that the perimeter matches the sum of sides
        assert triangle.perimeter == a + b + c

def test_triangle_equality():
    """Test comparison between triangles for equality"""
    # Same triangles with same dimensions
    triangle1 = Triangle(3, 4, 5)
    triangle2 = Triangle(3, 4, 5)
    # Different triangles
    triangle3 = Triangle(5, 5, 5)
    triangle4 = Triangle(7, 8, 9)

    # Test equality
    assert triangle1 == triangle2
    assert triangle1 != triangle3
    assert triangle2 != triangle4
    assert triangle3 != triangle4
    
    # Different order of sides should be considered different triangles 
    # based on the implementation
    triangle5 = Triangle(5, 3, 4)
    assert triangle1 != triangle5

def test_very_small_values():
    """Test triangle creation and calculations with very small values (precision test)"""
    # Use very small values that are valid for a triangle
    triangle = Triangle(0.0000001, 0.0000002, 0.0000002)
    
    # Check that the triangle is created successfully
    assert isinstance(triangle, Triangle)
    
    # Calculate expected area using Heron's formula
    s = (0.0000001 + 0.0000002 + 0.0000002) / 2
    expected_area = math.sqrt(s * (s - 0.0000001) * (s - 0.0000002) * (s - 0.0000002))
    
    # Check area with appropriate precision
    assert triangle.area == pytest.approx(expected_area)
    
    # Check perimeter
    expected_perimeter = 0.0000001 + 0.0000002 + 0.0000002
    assert triangle.perimeter == pytest.approx(expected_perimeter)

def test_very_large_values():
    """Test triangle creation and calculations with very large values"""
    # Use very large values that are valid for a triangle
    large_a = 1e9
    large_b = 2e9
    large_c = 2.5e9
    
    triangle = Triangle(large_a, large_b, large_c)
    
    # Check that the triangle is created successfully
    assert isinstance(triangle, Triangle)
    
    # Calculate expected area using Heron's formula
    s = (large_a + large_b + large_c) / 2
    expected_area = math.sqrt(s * (s - large_a) * (s - large_b) * (s - large_c))
    
    # Check area
    assert triangle.area == pytest.approx(expected_area)
    
    # Check perimeter
    expected_perimeter = large_a + large_b + large_c
    assert triangle.perimeter == pytest.approx(expected_perimeter)

def test_add_area_with_circle():
    """Test adding area of a triangle with a circle"""
    triangle = Triangle(3, 4, 5)  # Area = 6
    circle = Circle(2)            # Area = 4π ≈ 12.57
    
    result = triangle.add_area(circle)
    expected = triangle.area + circle.area
    
    assert result == pytest.approx(expected)
    assert isinstance(result, (int, float))

def test_add_area_with_rectangle():
    """Test adding area of a triangle with a rectangle"""
    triangle = Triangle(3, 4, 5)    # Area = 6
    rectangle = Rectangle(2, 3)     # Area = 6
    
    result = triangle.add_area(rectangle)
    expected = triangle.area + rectangle.area
    
    assert result == expected
    assert isinstance(result, (int, float))

def test_add_area_with_invalid_object():
    """Test that adding area with an invalid object raises ValueError"""
    triangle = Triangle(3, 4, 5)
    
    with pytest.raises(ValueError) as error:
        triangle.add_area("not a figure")
    
    assert "Could not calculate area with argument given" in str(error.value)