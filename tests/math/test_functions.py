import unittest

from openspace.math.constants import SECONDS_IN_SIDEREAL_DAY
from openspace.math.functions import EquationsOfMotion

MU: float = 398600.4418
GEO_RADIUS: float = 42164.16962995827
GEO_NU: float = 7.292115856392646e-05
A: float = 2
B: float = 1.7320508075688772
E: float = 0.5
P: float = 42139.21213813413
R: float = 42164.16962995827
V: float = 3.07375
PHI: float = 1e-6
H: float = 129602.11640001943


class TestSemiMajorAxis(unittest.TestCase):
    def test_from_mu_n(self):
        self.assertAlmostEqual(EquationsOfMotion.A.from_mu_n(MU, GEO_NU), GEO_RADIUS)

    def test_from_mu_tau(self):
        self.assertAlmostEqual(EquationsOfMotion.A.from_mu_tau(MU, SECONDS_IN_SIDEREAL_DAY), GEO_RADIUS)

    def test_from_mu_r_v(self):
        self.assertAlmostEqual(EquationsOfMotion.A.from_mu_r_v(MU, R, V), 42139.22690208438)


class TestMeanMotion(unittest.TestCase):
    def test_from_a_mu(self):
        self.assertAlmostEqual(EquationsOfMotion.N.from_a_mu(GEO_RADIUS, MU), GEO_NU)

    def test_from_tau(self):
        self.assertAlmostEqual(EquationsOfMotion.N.from_tau(SECONDS_IN_SIDEREAL_DAY), GEO_NU)


class TestSemiMinorAxis(unittest.TestCase):
    def test_from_a_e(self):
        self.assertAlmostEqual(EquationsOfMotion.B.from_a_e(A, E), B)


class TestEccentricity(unittest.TestCase):
    def test_from_a_b(self):
        self.assertAlmostEqual(EquationsOfMotion.E.from_a_b(A, B), E)

    def test_from_a_c(self):
        self.assertAlmostEqual(EquationsOfMotion.E.from_a_c(A, 1), E)


class TestFlattening(unittest.TestCase):
    def test_from_a_b(self):
        self.assertAlmostEqual(EquationsOfMotion.F.from_a_b(A, B), 0.1339745962155614)


class TestSemiParameter(unittest.TestCase):
    def test_from_mu_h(self):
        self.assertAlmostEqual(EquationsOfMotion.P.from_mu_h(MU, H), P)

    def test_from_a_b(self):
        self.assertAlmostEqual(EquationsOfMotion.P.from_a_b(A, B), 1.5)


class TestArealVelocity(unittest.TestCase):
    def test_from_mu_p(self):
        self.assertAlmostEqual(EquationsOfMotion.H.from_mu_p(MU, P), H)

    def test_from_r_v_phi(self):
        self.assertAlmostEqual(EquationsOfMotion.H.from_r_v_phi(R, V, PHI), H)


class TestPeriod(unittest.TestCase):
    def test_from_a_mu(self):
        self.assertAlmostEqual(EquationsOfMotion.TAU.from_a_mu(GEO_RADIUS, MU), SECONDS_IN_SIDEREAL_DAY)


class TestVisVivaVelocity(unittest.TestCase):
    def test_from_a_mu_r(self):
        self.assertAlmostEqual(EquationsOfMotion.V.from_a_mu_r(GEO_RADIUS, MU, GEO_RADIUS), 3.07466009930248)


class TestSpecificMechanicalEnergy(unittest.TestCase):
    def test_(self):
        self.assertAlmostEqual(EquationsOfMotion.XI.from_mu_r_v_r(MU, R, V, 6378), 57.76658435031927)
