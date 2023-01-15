import unittest

from openspace.coordinates import ClassicalElements, GCRFstate, ITRFstate, Nutation, Precession
from openspace.math.linalg import Vector3D
from openspace.time import Epoch


class TestClassicalElements(unittest.TestCase):
    POSITION: Vector3D = Vector3D(10000, 40000, -5000)
    VELOCITY: Vector3D = Vector3D(-1.5, 1, -0.1)
    GEO_SMA: float = 42164
    GEO_PERIOD: float = 86163.57055057827

    def test_sma_from_r_and_v(self):
        sma: float = ClassicalElements.sma_from_r_and_v(self.POSITION.magnitude(), self.VELOCITY.magnitude())
        self.assertAlmostEqual(sma, 25015.18101846454)

    def test_period_from_sma(self):
        period: float = ClassicalElements.period_from_sma(self.GEO_SMA)
        self.assertAlmostEqual(period, 86163.57055057827)

    def test_mean_motion_from_sma(self):
        m: float = ClassicalElements.mean_motion_from_sma(self.GEO_SMA)
        self.assertAlmostEqual(m, 7.292159861796045e-05)

    def test_areal_velocity_from_r_and_v(self):
        h: Vector3D = ClassicalElements.areal_velocity_from_r_and_v(self.POSITION, self.VELOCITY)
        self.assertAlmostEqual(h.magnitude(), 70521.27338612087)
        self.assertAlmostEqual(h.x, 1000)
        self.assertAlmostEqual(h.y, 8500)
        self.assertAlmostEqual(h.z, 70000)

    def test_semilatus_rectum_from_h(self):
        h: Vector3D = ClassicalElements.areal_velocity_from_r_and_v(self.POSITION, self.VELOCITY)
        self.assertAlmostEqual(ClassicalElements.semilatus_rectum_from_h(h.magnitude()), 12476.779949218813)


class TestGCRFstate(unittest.TestCase):

    EPOCH = Epoch.from_gregorian(2021, 12, 25, 4, 43, 51.608)
    GCRF: GCRFstate = GCRFstate(EPOCH, Vector3D(10000, 40000, -5000), Vector3D(0, 0, 0))
    EARTH_SURFACE: GCRFstate = GCRFstate(EPOCH, Vector3D(6378, 0, 0), Vector3D(0, 0, 0))

    def test_itrf_position(self):
        itrf: Vector3D = self.GCRF.itrf_position()
        self.assertAlmostEqual(itrf.x, 1173.544602365, 0)
        self.assertAlmostEqual(itrf.y, -41216.97127606, 0)
        self.assertAlmostEqual(itrf.z, -4978.360362079, 0)

    def test_total_acceleration_from_earth(self):
        a = self.EARTH_SURFACE.acceleration_from_gravity().plus(self.EARTH_SURFACE.acceleration_from_earth())
        self.assertAlmostEqual(0.009814696076649412, a.magnitude())

    def test_acceleration_from_gravity(self):
        a = self.EARTH_SURFACE.acceleration_from_gravity()
        self.assertAlmostEqual(1.5990836818112354e-05, a.magnitude())

    def test_acceleration_from_earth(self):
        a = self.EARTH_SURFACE.acceleration_from_earth()
        self.assertAlmostEqual(0.00979870641977297, a.magnitude())


class TestPrecession(unittest.TestCase):
    EPOCH = Epoch.from_gregorian(2021, 12, 25, 4, 43, 51.608)

    GCRF: GCRFstate = GCRFstate(EPOCH, Vector3D(10000, 40000, -5000), Vector3D(0, 0, 0))

    def test_matrix(self):
        mod = Precession.matrix(self.EPOCH).multiply_vector(self.GCRF.position)
        self.assertAlmostEqual(mod.x, 9813.907183667, 3)
        self.assertAlmostEqual(mod.y, 40048.700077099, 3)
        self.assertAlmostEqual(mod.z, -4978.840018011, 3)


class TestNutation(unittest.TestCase):
    EPOCH = Epoch.from_gregorian(2021, 12, 25, 4, 43, 51.608)
    MOD: Vector3D = Vector3D(9813.907183667, 40048.700077099, -4978.840018011)

    def test_matrix(self):
        mod = Nutation.matrix(self.EPOCH).multiply_vector(self.MOD)
        self.assertAlmostEqual(mod.x, 9816.34413386, 1)
        self.assertAlmostEqual(mod.y, 40048.169137333, 1)
        self.assertAlmostEqual(mod.z, -4978.306598902, 1)


class TestITRFstate(unittest.TestCase):
    EPOCH = Epoch.from_gregorian(2021, 12, 25, 4, 43, 51.608)
    ITRF: ITRFstate = ITRFstate(
        EPOCH,
        Vector3D(1173.544602365, -41216.97127606, -4978.360362079),
        Vector3D(0, 0, 0),
    )

    def test_gcrf_position(self):
        gcrf: GCRFstate = self.ITRF.gcrf_position()
        self.assertAlmostEqual(gcrf.x, 10000, 0)
        self.assertAlmostEqual(gcrf.y, 40000, 0)
        self.assertAlmostEqual(gcrf.z, -5000, 0)
