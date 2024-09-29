from math import radians

import pytest

from pysmad.elements import CartesianElements, GetClassicalElements


def test_from_cartesian():
    x = 10000
    y = 40000
    z = -5000
    vx = -1.5
    vy = 1
    vz = -0.1
    classical = GetClassicalElements.from_cartesian(CartesianElements(x, y, z, vx, vy, vz))
    assert classical.semimajor_axis == pytest.approx(25015.181, abs=0.5)
    assert classical.eccentricity == pytest.approx(0.7079772, abs=5e-6)
    assert classical.inclination == pytest.approx(radians(6.971), abs=5e-6)
    assert classical.raan == pytest.approx(radians(173.29), abs=5e-6)
    assert classical.argument_of_perigee == pytest.approx(radians(91.553), abs=5e-6)
    assert classical.mean_anomaly == pytest.approx(radians(144.225), abs=5e-6)
