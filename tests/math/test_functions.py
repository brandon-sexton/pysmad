import unittest

from openspace.math.constants import SECONDS_IN_SIDEREAL_DAY
from openspace.math.functions import EquationsOfMotion, LegendrePolynomial
from openspace.math.linalg import Vector3D

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

    def test_from_a_p(self):
        self.assertAlmostEqual(EquationsOfMotion.E.from_a_p(GEO_RADIUS, P), 0.024329248415869805)


class TestFlattening(unittest.TestCase):
    def test_from_a_b(self):
        self.assertAlmostEqual(EquationsOfMotion.F.from_a_b(A, B), 0.1339745962155614)


class TestSemiParameter(unittest.TestCase):
    def test_from_mu_h(self):
        self.assertAlmostEqual(EquationsOfMotion.P.from_mu_h(MU, H), P)

    def test_from_a_b(self):
        self.assertAlmostEqual(EquationsOfMotion.P.from_a_b(A, B), 1.5)

    def test_from_a_e(self):
        self.assertAlmostEqual(EquationsOfMotion.P.from_a_e(GEO_RADIUS, 0.024329248415869805), P)


class TestArealVelocity(unittest.TestCase):
    def test_from_mu_p(self):
        self.assertAlmostEqual(EquationsOfMotion.H.from_mu_p(MU, P), H)

    def test_from_r_v_phi(self):
        self.assertAlmostEqual(EquationsOfMotion.H.from_r_v_phi(R, V, PHI), H)

    def test_from_r_v(self):
        h = EquationsOfMotion.H.from_r_v(Vector3D(1, 2, 3), Vector3D(4, 2, 42))
        self.assertAlmostEqual(h.x, 78)
        self.assertAlmostEqual(h.y, -30)
        self.assertAlmostEqual(h.z, -6)


class TestPeriod(unittest.TestCase):
    def test_from_a_mu(self):
        self.assertAlmostEqual(EquationsOfMotion.TAU.from_a_mu(GEO_RADIUS, MU), SECONDS_IN_SIDEREAL_DAY)


class TestVisVivaVelocity(unittest.TestCase):
    def test_from_a_mu_r(self):
        self.assertAlmostEqual(EquationsOfMotion.V.from_a_mu_r(GEO_RADIUS, MU, GEO_RADIUS), 3.07466009930248)

    def test_from_mu_r_e_nu(self):
        self.assertAlmostEqual(EquationsOfMotion.V.from_mu_r_e_nu(MU, GEO_RADIUS, 0, 0), 3.07466009930248)

    def test_from_mu_r_xi(self):
        self.assertAlmostEqual(EquationsOfMotion.V.from_mu_r_xi(MU, R, -4.72956519499274), V)


class TestSpecificMechanicalEnergy(unittest.TestCase):
    def test_from_mu_r_v(self):
        self.assertAlmostEqual(EquationsOfMotion.XI.from_mu_r_v(MU, R, V), -4.72956519499274)

    def test_from_mu_a(self):
        self.assertAlmostEqual(EquationsOfMotion.XI.from_mu_a(MU, A), -99650.11045)


class TestTrueAnomaly(unittest.TestCase):
    def test_from_e_ea(self):
        self.assertAlmostEqual(EquationsOfMotion.NU.from_e_ea(0.025, 0.1), 0.10252766708805071)


class TestEccentricAnomaly(unittest.TestCase):
    def test_from_ma_e(self):
        self.assertAlmostEqual(EquationsOfMotion.EA.from_ma_e(1, 0.2), 1.1853242038613385)

    def test_from_rdv_r_a_n(self):
        self.assertAlmostEqual(EquationsOfMotion.EA.from_rdv_r_a_n(0, GEO_RADIUS, GEO_RADIUS, GEO_NU), 0)


class TestInclination(unittest.TestCase):
    def test_from_w(self):
        self.assertAlmostEqual(EquationsOfMotion.I.from_w(Vector3D(1, 1, 1)), 0.9553166181245093)


class TestMeanAnomaly(unittest.TestCase):
    def test_from_ea_e(self):
        self.assertAlmostEqual(EquationsOfMotion.MA.from_ea_e(1, 0.2), 0.8317058030384207)


class TestArgumentOfPerigee(unittest.TestCase):
    def test_from_u_nu(self):
        self.assertAlmostEqual(EquationsOfMotion.W.from_u_nu(1, 2), 5.283185307179586)


class TestArgumentOfLatitude(unittest.TestCase):
    def test_from_r_w(self):
        self.assertAlmostEqual(EquationsOfMotion.U.from_r_w(Vector3D(1, 2, 3), Vector3D(4, 2, 42)), 0.4636476090008061)


class TestRAAN(unittest.TestCase):
    def test_from_w(self):
        self.assertAlmostEqual(EquationsOfMotion.RAAN.from_w(Vector3D(1, 1, 1)), 2.356194490192345)


class TestLegendrePolynomial(unittest.TestCase):
    def test_p(self):
        p = LegendrePolynomial(1).p
        self.assertAlmostEqual(p[0][0], 1)
        self.assertAlmostEqual(p[1][0], 0.8414709848078965)
        self.assertAlmostEqual(p[1][1], 0.5403023058681398)
        self.assertAlmostEqual(p[2][0], 0.5621101274103568)
        self.assertAlmostEqual(p[2][1], 1.3639461402385225)
        self.assertAlmostEqual(p[2][2], 0.8757797451792866)
        self.assertAlmostEqual(p[3][0], 0.2273516142655441)
        self.assertAlmostEqual(p[3][1], 2.0588492958263878)
        self.assertAlmostEqual(p[3][2], 3.6847162232541146)
        self.assertAlmostEqual(p[3][3], 2.365929078764902)
        self.assertAlmostEqual(p[4][0], -0.08679046873880569)
        self.assertAlmostEqual(p[4][1], 2.2238163502521444)
        self.assertAlmostEqual(p[4][2], 8.66258689896924)
        self.assertAlmostEqual(p[4][3], 13.936024703257592)
        self.assertAlmostEqual(p[4][4], 8.948218557440123)
