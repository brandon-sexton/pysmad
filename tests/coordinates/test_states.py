import unittest

from openspace.coordinates.states import GCRF
from openspace.math.linalg import Vector3D
from openspace.time import Epoch


class TestGCRFstate(unittest.TestCase):

    EPOCH = Epoch.from_gregorian(2021, 12, 25, 4, 43, 51.608)
    STATE: GCRF = GCRF(EPOCH, Vector3D(10000, 40000, -5000), Vector3D(0, 0, 0))
    EARTH_SURFACE: GCRF = GCRF(EPOCH, Vector3D(6378, 0, 0), Vector3D(0, 0, 0))

    def test_total_acceleration_from_earth(self):
        a = self.EARTH_SURFACE.acceleration_from_gravity().plus(self.EARTH_SURFACE.acceleration_from_earth())
        self.assertAlmostEqual(0.009814696076649412, a.magnitude())

    def test_acceleration_from_gravity(self):
        a = self.EARTH_SURFACE.acceleration_from_gravity()
        self.assertAlmostEqual(1.5990836818112354e-05, a.magnitude(), 15)

    def test_acceleration_from_earth(self):
        a = self.EARTH_SURFACE.acceleration_from_earth()
        self.assertAlmostEqual(0.00979870641977297, a.magnitude(), 15)

    def test_acceleration_from_sun(self):
        a = self.STATE.acceleration_from_sun()
        self.assertAlmostEqual(3.00696687920662e-9, a.magnitude(), 15)

    def test_acceleration_from_moon(self):
        a = self.STATE.acceleration_from_moon()
        self.assertAlmostEqual(3.4064259486775476e-9, a.magnitude(), 15)
