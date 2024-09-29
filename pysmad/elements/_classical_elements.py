from math import cos, sin, sqrt

from pysmad.bodies import Earth
from pysmad.coordinates import CartesianVector
from pysmad.math import EquationsOfMotion
from pysmad.math.linalg import Matrix3D


class ClassicalElements:
    def __init__(self, a: float, e: float, i: float, raan: float, arg_per: float, ma: float) -> None:
        """used to perform calculations with the classical orbital elements

        :param epoch: epoch for which the elements are valid
        :type epoch: Epoch
        :param a: semi-major axis in km
        :type a: float
        :param e: eccentricity
        :type e: float
        :param i: inclination in radians
        :type i: float
        :param raan: right ascension of the ascending node in radians
        :type raan: float
        :param arg_per: argument of perigee in radians
        :type arg_per: float
        :param ma: mean anomaly in radians
        :type ma: float
        """

        #: semi-major axis in km
        self.semimajor_axis: float = a

        #: eccentricity
        self.eccentricity: float = e

        #: inclination in radians
        self.inclination: float = i

        #: right ascension of the ascending node in radians
        self.raan: float = raan

        #: argument of perigee in radians
        self.argument_of_perigee: float = arg_per

        #: mean anomaly in radians
        self.mean_anomaly: float = ma

    @property
    def true_anomaly(self) -> float:
        return EquationsOfMotion.true_anomaly.from_e_ea(self.eccentricity, self.eccentric_anomaly)

    @property
    def eccentric_anomaly(self) -> float:
        return EquationsOfMotion.eccentric_anomaly.from_ma_e(self.mean_anomaly, self.eccentricity)

    @property
    def pqw_matrix(self) -> Matrix3D:
        p = self.p_vector
        q = self.q_vector
        w = self.w_vector
        row_1 = CartesianVector(p.x, q.x, w.x)
        row_2 = CartesianVector(p.y, q.y, w.y)
        row_3 = CartesianVector(p.z, q.z, w.z)
        return Matrix3D(row_1, row_2, row_3)

    @property
    def pqw_position(self) -> CartesianVector:
        a = self.semimajor_axis
        e = self.eccentricity
        ea = self.eccentric_anomaly

        return CartesianVector(a * (cos(ea) - e), a * sqrt(1 - e * e) * sin(ea), 0)

    @property
    def pqw_velocity(self) -> CartesianVector:
        a = self.semimajor_axis
        e = self.eccentricity
        ea = self.eccentric_anomaly
        a_edot = sqrt(Earth.mu() * a) / self.pqw_position.magnitude
        return CartesianVector(-sin(ea) * a_edot, sqrt(1 - e * e) * cos(ea) * a_edot, 0)

    @property
    def p_vector(self) -> CartesianVector:
        """calculate the vector pointing from the focus to the lowest point in the orbit

        :return: vector from origin to perigee
        :rtype: CartesianVector
        """
        cw: float = cos(self.argument_of_perigee)
        c0: float = cos(self.raan)
        sw: float = sin(self.argument_of_perigee)
        s0: float = sin(self.raan)
        ci: float = cos(self.inclination)
        return CartesianVector(cw * c0 - sw * ci * s0, cw * s0 + sw * ci * c0, sw * sin(self.inclination)).normalized()

    @property
    def q_vector(self) -> CartesianVector:
        """calculate the vector from the focus to the point 90 degrees off of the perigee vector

        :param epoch: _description_
        :type epoch: Epoch
        :return: semi-latus rectum vector
        :rtype: CartesianVector
        """
        cw: float = cos(self.argument_of_perigee)
        c0: float = cos(self.raan)
        sw: float = sin(self.argument_of_perigee)
        s0: float = sin(self.raan)
        ci: float = cos(self.inclination)
        return CartesianVector(
            -sw * c0 - cw * ci * s0, -sw * s0 + cw * ci * c0, cw * sin(self.inclination)
        ).normalized()

    @property
    def w_vector(self) -> CartesianVector:
        """calculate the angular momentum vector

        :return: vector normal to the orbital plane and parallel to the cross product of position and velocity vectors
        """
        si = sin(self.inclination)
        return CartesianVector(si * sin(self.raan), -si * cos(self.raan), cos(self.inclination)).normalized()
