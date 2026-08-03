import pytest

from ..src.Figure import Figure
from ..src.Rectangle import Rectangle
from ..src.Circle import Circle

pytestmark = pytest.mark.usefixtures("log_test_case")


def test_new_class():
    with pytest.raises(TypeError):
        temp = Figure()


def test_figure_add_area_raises_for_non_figure():
    """Figure.add_area should raise ValueError when the argument is not a Figure"""
    rect = Rectangle(2, 3)
    with pytest.raises(ValueError) as error:
        rect.add_area(42)
    assert error.value.args[0] == "Could not calculate area with argument given"


def test_figure_add_area_works_with_two_concrete_figures():
    """add_area should return the sum of two concrete figure areas"""
    rect = Rectangle(3, 4)   # area = 12
    circle = Circle(1)        # area = pi
    result = rect.add_area(circle)
    assert result == pytest.approx(rect.area + circle.area)


def test_figure_subclass_can_be_instantiated():
    """A concrete subclass of Figure can be instantiated without error"""
    class MinimalFigure(Figure):
        area = 5

        @property
        def perimeter(self):
            return 10

    fig = MinimalFigure()
    assert isinstance(fig, Figure)
    assert fig.area == 5
    assert fig.perimeter == 10
