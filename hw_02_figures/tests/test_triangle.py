from ..src.Triangle import Triangle
import pytest

@pytest.mark.parametrize("side1, side2, side3, expected_output", [
    (3, 4, 5, True),
    (7, 10, 5, False),
    (6, 8, 10, True),
])
def test_is_right_triangle(side1, side2, side3, expected_output):
    triangle = Triangle(side1, side2, side3)
    assert triangle.is_right_triangle() == expected_output

@pytest.mark.parametrize("side1, side2, side3, expected_output", [
    (3, 3, 3, True),
    (5, 5, 6, False),
    (7, 7, 7, True),
])
def test_is_equilateral(side1, side2, side3, expected_output):
    triangle = Triangle(side1, side2, side3)
    assert triangle.is_equilateral() == expected_output

@pytest.mark.parametrize("side1, side2, side3, expected_output", [
    (5, 5, 7, True),
    (4, 4, 4, False),
    (8, 8, 6, True),
])
def test_is_isosceles(side1, side2, side3, expected_output):
    triangle = Triangle(side1, side2, side3)
    assert triangle.is_isosceles() == expected_output

@pytest.mark.parametrize("side1, side2, side3, expected_output", [
    (3, 4, 5, 6.0),
    (6, 8, 10, 24.0),
    (3, 5, 7, 0),
])
def test_area(side1, side2, side3, expected_output):
    triangle = Triangle(side1, side2, side3)
    assert pytest.approx(triangle.area()) == expected_output
