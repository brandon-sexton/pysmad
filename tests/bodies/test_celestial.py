import unittest

from openspace.bodies.celestial import Earth, Moon, Sun
from openspace.math.linalg import Vector3D
from openspace.time import Epoch


class TestEarth(unittest.TestCase):
    def test_mu(self):
        self.assertEqual(398600.4418, Earth.MU)

    def test_radius(self):
        self.assertEqual(6378.137, Earth.RADIUS)

    def test_flattening(self):
        self.assertEqual(1 / 298.2572235, Earth.FLATTENING)


class TestSun(unittest.TestCase):

    EPOCH: Epoch = Epoch.from_gregorian(2022, 2, 25, 0, 1, 9.184)
    TRUTH: Vector3D = Vector3D(1.353158384133262e8, -5.514968448042840e7, -2.390803633125914e7)

    def test_get_position(self):
        sun_pos = Sun.get_position(self.EPOCH)
        self.assertAlmostEqual(sun_pos.magnitude() / self.TRUTH.magnitude(), 1, 4)
        self.assertAlmostEqual(sun_pos.angle(self.TRUTH), 0, 2)


class TestMoon(unittest.TestCase):

    EPOCH: Epoch = Epoch.from_gregorian(2022, 2, 25, 0, 1, 9.184)
    TRUTH: Vector3D = Vector3D(-6.454159844478600e4, -3.280761448809440e5, -1.566863311585961e5)

    def test_get_position(self):
        moon_pos = Moon.get_position(self.EPOCH)
        self.assertAlmostEqual(moon_pos.magnitude() / self.TRUTH.magnitude(), 1, 4)
        self.assertAlmostEqual(moon_pos.angle(self.TRUTH), 0, 3)
