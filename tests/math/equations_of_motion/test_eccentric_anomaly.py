from math import radians

from pysmad.math import EquationsOfMotion


def test_from_e_nu():
    e = 0.83285
    nu = radians(92.335)
    assert EquationsOfMotion.eccentric_anomaly.from_e_nu(e, nu) == 0.6095079699392008
