from math import radians

import pytest

from pysmad.elements import ClassicalElements, GetCartesian


def test_from_classical():

    # Example 2-6 from Vallado
    a = 25015.181
    e = 0.7079772
    i = radians(6.971)
    raan = radians(173.29)
    arg_per = radians(91.553)
    ma = radians(144.225)

    cartesian = GetCartesian.from_classical(ClassicalElements(a, e, i, raan, arg_per, ma))
    assert cartesian.x == pytest.approx(10000, abs=0.5)
    assert cartesian.y == pytest.approx(40000, abs=0.5)
    assert cartesian.z == pytest.approx(-5000, abs=0.5)
    assert cartesian.vx == pytest.approx(-1.5, abs=5e-6)
    assert cartesian.vy == pytest.approx(1, abs=5e-6)
    assert cartesian.vz == pytest.approx(-0.1, abs=5e-6)

    # Example 2-6 from Vallado
    a = 36126.64283480516
    e = 0.83285
    i = radians(87.87)
    raan = radians(227.89)
    arg_per = radians(53.38)
    ma = 0.1327312448297558

    eci = GetCartesian.from_classical(ClassicalElements(a, e, i, raan, arg_per, ma))
    assert eci.x == pytest.approx(6525.344, abs=0.5)
    assert eci.y == pytest.approx(6861.535, abs=0.5)
    assert eci.z == pytest.approx(6449.125, abs=0.5)
    assert eci.vx == pytest.approx(4.902276, abs=5e-4)
    assert eci.vy == pytest.approx(5.533124, abs=5e-4)
    assert eci.vz == pytest.approx(-1.975709, abs=5e-4)
