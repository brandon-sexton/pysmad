import pytest

from pysmad.math import EquationsOfMotion


def test_from_a_e():
    a = 36126.64283480516
    e = 0.83285
    assert EquationsOfMotion.semi_parameter.from_a_e(a, e) == pytest.approx(11067.79)
