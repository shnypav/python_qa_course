import pytest

from ..src.Circle import Circle
from ..src.Figure import Figure
from ..src.Rectangle import Rectangle
from ..src.Square import Square
from ..src.Triangle import Triangle

pytestmark = pytest.mark.usefixtures("log_test_case")


@pytest.mark.parametrize(
    "figure",
    [
        Circle(2),
        Rectangle(2, 3),
        Square(4),
        Triangle(3, 4, 5),
    ],
)
def test_concrete_figures_are_figure_instances(figure):
    assert isinstance(figure, Figure)
    assert isinstance(figure.area, (int, float))
    assert isinstance(figure.perimeter, (int, float))


def test_figure_subclass_without_perimeter_raises_not_implemented():
    class CustomFigure(Figure):
        area = 10

    figure = CustomFigure()

    with pytest.raises(NotImplementedError, match="Subclasses must implement perimeter calculation"):
        figure.perimeter


@pytest.mark.parametrize(
    "left, right",
    [
        (Circle(3), Square(3)),
        (Square(4), Rectangle(4, 4)),
        (Triangle(3, 4, 5), (3, 4, 5)),
    ],
)
def test_figures_are_not_equal_to_different_types(left, right):
    assert left != right


@pytest.mark.parametrize("operator", ["<", ">", "<=", ">="])
def test_circle_ordering_rejects_non_circles(operator):
    circle = Circle(3)

    with pytest.raises(TypeError, match="Cannot compare Circle with non-Circle object"):
        if operator == "<":
            circle < 3
        elif operator == ">":
            circle > 3
        elif operator == "<=":
            circle <= 3
        else:
            circle >= 3


def test_add_area_is_symmetric_for_standard_figures():
    circle = Circle(2)
    rectangle = Rectangle(3, 4)

    assert circle.add_area(rectangle) == pytest.approx(rectangle.add_area(circle))
