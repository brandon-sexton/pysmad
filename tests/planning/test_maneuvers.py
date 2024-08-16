import unittest

from pysmad.planning.maneuvers import Hohmann, VisViva


class TestVisViva(unittest.TestCase):
    def test_circular_velocity(self):
        self.assertAlmostEqual(VisViva.circular_velocity(42164), 3.074666284127684)

    def test_eccentric_velocity(self):
        self.assertAlmostEqual(VisViva.eccentric_velocity(42164, 42244), 3.077576247190643)


class TestHohmann(unittest.TestCase):
    PLANNER: Hohmann = Hohmann(42164, 42324)

    def test_planner(self):
        self.assertAlmostEqual(self.PLANNER.delta_v_1, 0.0029099630629589868)
        self.assertAlmostEqual(self.PLANNER.delta_v_2, 0.0029072089766200016)
