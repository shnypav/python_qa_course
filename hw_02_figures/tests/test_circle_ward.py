from math import pi

from ward import test, each

from ..src.Circle import Circle
from ..src.Figure import Figure


@test("calculate_area should return correct area for given radius")
# @pytest.mark.parametrize("radius, expected_area", [(0, 0), (10, 100 * pi), (2.5, (2.5 ** 2) * pi)])
def test_calculate_area(
        radius=each(0, 11, 2.5),
        exp_area=each(0, 100 * pi, ((2.5 ** 2) * pi))):
    circle = Circle(radius)
    assert circle.area == exp_area

# @test("calculate_perimeter should return correct perimeter for radius 5")
# def test_calculate_perimeter():
#     circle = Circle(5)
#     assert circle.calculate_perimeter() == 31.42
