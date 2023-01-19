import unittest

from openspace.coordinates.elements import ClassicalElements
from openspace.coordinates.states import IJK
from openspace.math.linalg import Vector3D
from openspace.time import Epoch


class TestClassicalElements(unittest.TestCase):
    EPOCH: Epoch = Epoch(0)
    POSITION: Vector3D = Vector3D(10000, 40000, -5000)
    VELOCITY: Vector3D = Vector3D(-1.5, 1, -0.1)
    GEO_SMA: float = 42164
    GEO_PERIOD: float = 86163.57055057827
    IJK_STATE: IJK = IJK(EPOCH, POSITION, VELOCITY)

    def test_from_r_v(self):
        coes: ClassicalElements = ClassicalElements.from_ijk(self.IJK_STATE)
        self.assertAlmostEqual(coes.semimajor_axis, 25015.18101846454)
        self.assertAlmostEqual(coes.eccentricity, 0.707977170873199)
        self.assertAlmostEqual(coes.inclination, 0.12166217595729033)
        self.assertAlmostEqual(coes.raan, 3.024483909022929)
        self.assertAlmostEqual(
            coes.argument_of_perigee,
            1.597899323919623,
        )
        self.assertAlmostEqual(coes.mean_anomaly, 2.5172009599614285)
