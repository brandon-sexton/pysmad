import unittest

from pysmad.coordinates.positions import PositionConvert
from pysmad.math.linalg import Vector3D
from pysmad.time import Epoch


class TestPositionConvertGCRF(unittest.TestCase):
    START_POS: Vector3D = Vector3D(10000, 40000, -5000)
    EPOCH = Epoch.from_gregorian(2021, 12, 25, 4, 43, 51.608)

    def test_to_itrf(self):
        itrf: Vector3D = PositionConvert.gcrf.to_itrf(self.START_POS, self.EPOCH)
        self.assertAlmostEqual(itrf.x, 1173.544602365, 0)
        self.assertAlmostEqual(itrf.y, -41216.97127606, 0)
        self.assertAlmostEqual(itrf.z, -4978.360362079, 0)
