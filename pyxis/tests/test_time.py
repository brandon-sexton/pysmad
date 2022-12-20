import unittest

from pyxis.time import Epoch

class TestGregorian(unittest.TestCase):

    EPOCH = Epoch.from_gregorian(2022, 12, 19, 12, 0, 0)

    def test_julian_value(self):
        self.assertAlmostEqual(self.EPOCH.julian_value(), 2459932.99999999)
