import pytest

from ..src.Square import Square



# test_square_perimeter: A pytest function for verifying the perimeter of a Square object.
#
# This test function uses parametrized inputs to check if the Square object returns the expected perimeter.
#
# Arguments:
# side (int): The length of one side of the square.
# expected_perimeter (int): The expected perimeter value for a square with the given side length.

@pytest.mark.parametrize("side, expected_perimeter", [(0, 0), (2, 2 * 4)])
def test_square_perimeter(side, expected_perimeter):
    square = Square(side)
    assert square.perimeter == expected_perimeter






@pytest.mark.parametrize("side, expected_area", [(0, 0), (3, 3 * 3)])
def test_square_area(side, expected_area):
    square = Square(side)
    assert square.area == expected_area


# test_square_has_name(create_square): A pytest function for verifying the name attribute of a Square object.
#
# This function asserts that the name attribute of the passed create_square instance, which is the fixture representing the Square object,
# is equal to "Square". This test ensures that the name attribute of the Square object is correctly set.
#
# Arguments:
# create_square (Square): The instance of the Square object to be tested for its name attribute.
def test_square_has_name(create_square):
    assert create_square.name == "Square"


def test_square_side_less_than_zero():
    with pytest.raises(ValueError) as error:
        Square(-1)
    assert error.type is ValueError
    assert error.value.args[0] == "Square side should be > 0"


@pytest.mark.parametrize("side", ["aaa", "", None])
def test_create_square_with_invalid_side(side):
    with pytest.raises(TypeError) as error:
        Square(side)
    assert error.type is TypeError
