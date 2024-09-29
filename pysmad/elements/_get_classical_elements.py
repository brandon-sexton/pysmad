from pysmad.bodies import Earth
from pysmad.elements._cartesian_elements import CartesianElements
from pysmad.elements._classical_elements import ClassicalElements
from pysmad.math import EquationsOfMotion


class GetClassicalElements:
    @staticmethod
    def from_cartesian(els: CartesianElements) -> ClassicalElements:
        r = els.position.magnitude
        v = els.velocity.magnitude
        rdv = els.position.dot(els.velocity)

        h = EquationsOfMotion.areal_velocity.from_r_v(els.position, els.velocity)
        w = h.normalized()
        i = EquationsOfMotion.inclination.from_w(w)
        raan = EquationsOfMotion.raan.from_w(w)
        a = EquationsOfMotion.semi_major_axis.from_mu_r_v(Earth.mu(), r, v)
        p = EquationsOfMotion.semi_parameter.from_mu_h(Earth.mu(), h.magnitude)
        e = EquationsOfMotion.eccentricity.from_a_p(a, p)
        n = EquationsOfMotion.mean_motion.from_a_mu(a, Earth.mu())
        ea = EquationsOfMotion.eccentric_anomaly.from_rdv_r_a_n(rdv, r, a, n)
        ma = EquationsOfMotion.mean_anomaly.from_ea_e(ea, e)
        u = EquationsOfMotion.argument_of_latitude.from_r_w(els.position, w)
        nu = EquationsOfMotion.true_anomaly.from_e_ea(e, ea)
        aop = EquationsOfMotion.argument_of_perigee.from_u_nu(u, nu)
        return ClassicalElements(a, e, i, raan, aop, ma)
