from pysmad.bodies import Earth


def test_mu():
    assert Earth.MU == 398600.4418


def test_radius():
    assert Earth.RADIUS == 6378.137


def test_flattening():
    assert Earth.FLATTENING == 1 / 298.2572235
