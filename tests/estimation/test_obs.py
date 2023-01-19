import unittest
from math import radians

from openspace.bodies.terrestrial import GroundSite
from openspace.coordinates.states import ITRF
from openspace.estimation.obs import GroundObservation
from openspace.math.linalg import Vector3D
from openspace.time import Epoch


class TestGroundObservation(unittest.TestCase):
    SITE: GroundSite = GroundSite.from_itrf_position(Vector3D(1344.143, 6068.601, 1429.311))

    def test_ijk_position(self):
        state_1: ITRF = ITRF.from_fixed(Epoch.from_gregorian(1999, 4, 2, 0, 31, 9.184), self.SITE.itrf_position)
        ob_1: GroundObservation = GroundObservation.from_angles_and_range(
            state_1, radians(132.67), radians(32.44), 16945.45, 0, 0
        )
        ijk_1: Vector3D = ob_1.ijk_position()
        self.assertAlmostEqual(ijk_1.x, 11959.977742417275)
        self.assertAlmostEqual(ijk_1.y, -16289.477980186362)
        self.assertAlmostEqual(ijk_1.z, -5963.827409736864)

    def test_site_itrf_position(self):
        self.assertAlmostEqual(self.SITE.itrf_position.x, 1344.143)
        self.assertAlmostEqual(self.SITE.itrf_position.y, 6068.601)
        self.assertAlmostEqual(self.SITE.itrf_position.z, 1429.311)

    def test_site_ijk_position(self):
        gmst: float = Epoch.from_gregorian(1999, 4, 2, 0, 31, 9.184).greenwich_hour_angle()
        ijk: Vector3D = self.SITE.itrf_position.rotation_about_axis(Vector3D(0, 0, 1), gmst)
        self.assertAlmostEqual(ijk.x, 534.388240046999)
        self.assertAlmostEqual(ijk.y, -6192.662408903832)
        self.assertAlmostEqual(ijk.z, 1429.3110)
