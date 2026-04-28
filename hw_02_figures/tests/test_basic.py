import pytest

from ..src.Figure import Figure


def test_new_class():
    with pytest.raises(TypeError):
        temp = Figure()


def test_figure_perimeter_raises_not_implemented():
    class MinimalFigure(Figure):
        area = 1
    f = MinimalFigure()
    with pytest.raises(NotImplementedError):
        _ = f.perimeter


def test_figure_add_area_sums_two_subclasses():
    class MinimalFigure(Figure):
        def __init__(self, a):
            self._area = a

        @property
        def area(self):
            return self._area

        @property
        def perimeter(self):
            return 0

    f1 = MinimalFigure(5)
    f2 = MinimalFigure(7)
    assert f1.add_area(f2) == 12


def test_figure_add_area_rejects_non_figure():
    class MinimalFigure(Figure):
        area = 1

        @property
        def perimeter(self):
            return 0

    f = MinimalFigure()
    with pytest.raises(ValueError) as error:
        f.add_area(42)
    assert error.value.args[0] == "Could not calculate area with argument given"
