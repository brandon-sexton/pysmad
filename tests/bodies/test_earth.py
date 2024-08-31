from pysmad.bodies import Earth


def test_radius():
    assert Earth.radius() == 6378.1363


def test_mu():
    assert Earth.mu() == 398600.4415
