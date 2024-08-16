import unittest
from math import radians

from pysmad.bodies.terrestrial import GroundSite
from pysmad.coordinates.elements import ClassicalElements
from pysmad.coordinates.states import ITRF
from pysmad.estimation.iod import Gauss
from pysmad.estimation.obs import GroundObservation
from pysmad.math.linalg import Vector3D
from pysmad.time import Epoch


class TestGauss(unittest.TestCase):
    SITE: GroundSite = GroundSite.from_itrf_position(Vector3D(1344.143, 6068.601, 1429.311))

    def test_coes_from_positions(self):
        state_1: ITRF = ITRF(Epoch.from_gregorian(1999, 4, 2, 0, 31, 9.184), self.SITE.itrf_position, Vector3D(0, 0, 0))
        ob_1: GroundObservation = GroundObservation.from_angles_and_range(
            state_1, radians(132.67), radians(32.44), 16945.45, 0, 0
        )
        state_2: ITRF = ITRF(Epoch.from_gregorian(1999, 4, 2, 3, 1, 9.184), self.SITE.itrf_position, Vector3D(0, 0, 0))
        ob_2: GroundObservation = GroundObservation.from_angles_and_range(
            state_2, radians(123.08), radians(50.06), 37350.34, 0, 0
        )

        coes: ClassicalElements = Gauss.coes_from_positions(ob_1, ob_2)

        self.assertAlmostEqual(coes.semimajor_axis, 28196.77578363615)
        self.assertAlmostEqual(coes.eccentricity, 0.7679436)
        self.assertAlmostEqual(coes.inclination, 0.3545688111634284)
        self.assertAlmostEqual(coes.raan, 6.268254918583486)
        self.assertAlmostEqual(coes.argument_of_perigee, 3.1315625245621277)
        self.assertAlmostEqual(coes.mean_anomaly, 0.5102678870735644)

    def test_site_itrf_position(self):
        self.assertAlmostEqual(self.SITE.itrf_position.x, 1344.143)
        self.assertAlmostEqual(self.SITE.itrf_position.y, 6068.601)
        self.assertAlmostEqual(self.SITE.itrf_position.z, 1429.311)

    def test_site_eci_position(self):
        gmst: float = Epoch.from_gregorian(1999, 4, 2, 0, 31, 9.184).greenwich_hour_angle()
        eci: Vector3D = self.SITE.itrf_position.rotation_about_axis(Vector3D(0, 0, 1), gmst)
        self.assertAlmostEqual(eci.x, 534.388240046999)
        self.assertAlmostEqual(eci.y, -6192.662408903832)
        self.assertAlmostEqual(eci.z, 1429.3110)
