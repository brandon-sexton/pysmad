import unittest
from math import degrees

from pyxis.time import Epoch


class TestEpoch(unittest.TestCase):

    EPOCH = Epoch.from_gregorian(2022, 12, 19, 12, 1, 9.184)

    def test_julian_value(self):
        self.assertAlmostEqual(self.EPOCH.julian_value(), 2459933.00080074)

    def test_greenwich_hour_angle(self):
        self.assertAlmostEqual(degrees(self.EPOCH.greenwich_hour_angle()), 268.0707472726, 5)
