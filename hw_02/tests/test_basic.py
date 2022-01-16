import pytest

from ..src.Figure import Figure


def test_new_class():
    with pytest.raises(TypeError):
        temp = Figure()
