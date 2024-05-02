from math import pi

import pytest

from ..src.Circle import Circle
from ..src.Figure import Figure


@pytest.mark.parametrize("radius, expected_area", [(0, 0), (10, 100 * pi), (2.5, (2.5 ** 2) * pi)])
def test_circle_area(radius, expected_area):
  circle = Circle(radius)
  assert circle.area == expected_area


@pytest.mark.parametrize("radius, expected_perimeter", [(0, 0), (10, 2 * pi * 10)])
def test_circle_perimeter(radius, expected_perimeter):
  circle = Circle(radius)
  print("asdssssdddsss")
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
