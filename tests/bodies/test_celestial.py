import unittest

from pysmad.bodies.celestial import Earth, Moon, Sun
from pysmad.math.linalg import Vector3D
from pysmad.time import Epoch


class TestEarth(unittest.TestCase):
    def test_mu(self):
        self.assertEqual(398600.4418, Earth.MU)

    def test_radius(self):
        self.assertEqual(6378.137, Earth.RADIUS)

    def test_flattening(self):
        self.assertEqual(1 / 298.2572235, Earth.FLATTENING)

    def test_c(self):
        c00 = Earth.C[0][0]
        c10 = Earth.C[1][0]
        c11 = Earth.C[1][1]
        c20 = Earth.C[2][0]
        c21 = Earth.C[2][1]
        c22 = Earth.C[2][2]
        c30 = Earth.C[3][0]
        c31 = Earth.C[3][1]
        c32 = Earth.C[3][2]
        c33 = Earth.C[3][3]
        c40 = Earth.C[4][0]
        c41 = Earth.C[4][1]
        c42 = Earth.C[4][2]
        c43 = Earth.C[4][3]
        c44 = Earth.C[4][4]
        self.assertAlmostEqual(1, c00, 15)
        self.assertAlmostEqual(0, c10, 15)
        self.assertAlmostEqual(0, c11, 15)
        self.assertAlmostEqual(-0.0010826261738522227, c20, 15)
        self.assertAlmostEqual(-2.6673947523748365e-10, c21, 15)
        self.assertAlmostEqual(1.574615325722917e-06, c22, 15)
        self.assertAlmostEqual(2.5324105185677225e-06, c30, 15)
        self.assertAlmostEqual(2.1931496313133285e-06, c31, 15)
        self.assertAlmostEqual(3.0904390039164885e-07, c32, 15)
        self.assertAlmostEqual(1.0058351340882285e-07, c33, 15)
        self.assertAlmostEqual(1.6198975999169731e-06, c40, 15)
        self.assertAlmostEqual(-5.086435604395839e-07, c41, 15)
        self.assertAlmostEqual(7.837454574045524e-08, c42, 15)
        self.assertAlmostEqual(5.9215017763966597e-08, c43, 15)
        self.assertAlmostEqual(-3.983204248731872e-09, c44, 15)


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
