import pytest

from ..src.Triangle import Triangle


@pytest.mark.parametrize("side_a, side_b, side_c", [(0, 0, 0), (1, 2, 3), (-1, -2, 3)])
def test_triangle_does_not_exist(side_a, side_b, side_c):
    with pytest.raises(ValueError) as error:
        Triangle(side_a, side_b, side_c)
    assert error.type is ValueError
    assert error.value.args[0] == "Triangle with sides given does not exist"


@pytest.mark.parametrize("side_a, side_b, side_c, expected_perimeter", [(3, 3, 4, 10), (3, 5, 5, 13)])
def test_triangle_perimeter(side_a, side_b, side_c, expected_perimeter):
    triangle = Triangle(side_a, side_b, side_c)
    assert triangle.perimeter == expected_perimeter


@pytest.mark.parametrize("side_a, side_b, side_c, expected_area",
                         [(3, 3, 3, ((9 / 2) * (9 / 2 - 3) * (9 / 2 - 3) * (9 / 2 - 3)) ** 0.5),
                          (3, 5, 5, ((13 / 2) * (13 / 2 - 3) * (13 / 2 - 5) * (13 / 2 - 5)) ** 0.5)])
def test_triangle_area(side_a, side_b, side_c, expected_area):
    """
    semi-perimeter (sp) = perimeter / 2
    triangle area = (((sp*(sp-a)*(sp-b)*(sp-c)))**0.5)
    """
    triangle = Triangle(side_a, side_b, side_c)
    assert triangle.area == expected_area


def test_triangle_has_name(create_triangle):
    assert create_triangle.name == "Triangle"


@pytest.mark.parametrize("side_a, side_b, side_c", [("", "", None)])
def test_create_triangle_with_invalid_sides(side_a, side_b, side_c):
    with pytest.raises(TypeError) as error:
        Triangle(side_a, side_b, side_c)
    assert error.type is TypeError


@pytest.mark.parametrize("a,b,c,expected_radius", [
    (3, 4, 5, 2.5),
    (5, 12, 13, 6.5),
    (7, 24, 25, 12.5),
    (8, 15, 17, 8.5),
])
def test_circumcircle_radius(a, b, c, expected_radius):
    triangle = Triangle(a, b, c)
    assert triangle.circumcircle_radius == expected_radius


@pytest.mark.parametrize("side_a, side_b, side_c, expected_radius", [
    (3, 4, 5, 1),
    (6, 8, 10, 2),
    (5, 12, 13, 2)
])
def test_incircle_radius(side_a, side_b, side_c, expected_radius):
    triangle = Triangle(side_a, side_b, side_c)
    assert triangle.incircle_radius == expected_radius
