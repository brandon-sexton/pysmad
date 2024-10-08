import unittest
from math import radians

from pysmad.bodies import Earth
from pysmad.bodies._ground_site import GroundSite
from pysmad.bodies._satellite import Satellite
from pysmad.constants import DAYS_TO_SECONDS
from pysmad.coordinates.elements import ClassicalElements
from pysmad.coordinates.positions import SphericalPosition
from pysmad.coordinates.states import GCRF, IJK
from pysmad.estimation.obs import GroundObservation
from pysmad.time import Epoch


class TestGroundSite(unittest.TestCase):

    spherical: SphericalPosition = SphericalPosition(Earth.RADIUS, radians(11), radians(48))
    SITE: GroundSite = GroundSite.from_itrf_position(spherical.to_cartesian())
    COES: ClassicalElements = ClassicalElements(Epoch(50449), Earth.RADIUS + 960, 0, radians(97), radians(130.7), 0, 0)
    IJK_STATE: IJK = COES.to_ijk()
    SAT: Satellite = Satellite(GCRF(IJK_STATE.epoch, IJK_STATE.position, IJK_STATE.velocity))

    def test_angles_and_range(self):
        self.SAT.step_to_epoch(self.SAT.current_epoch().plus_days(600 / DAYS_TO_SECONDS))
        az_el_range: GroundObservation = self.SITE.angles_and_range(self.SAT)
        self.assertAlmostEqual(az_el_range.azimuth, 2.4905857059239622)
        self.assertAlmostEqual(az_el_range.elevation, 0.3057319222804495)
        self.assertAlmostEqual(az_el_range.range, 2174.186500131194)
