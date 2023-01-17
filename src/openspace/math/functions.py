from math import cos, pi, radians, sin, sqrt
from typing import List

from openspace.math.constants import HOURS_IN_DAY, MINUTES_IN_DAY, MINUTES_IN_HOUR, SECONDS_IN_DAY, SECONDS_IN_HOUR


class Conversions:
    """class used to perform various unit conversions

    :return: defined by each static method
    :rtype: defined by each static method
    """

    @staticmethod
    def hms_to_decimal_day(hr: float, m: float, s: float) -> float:
        """calculate the float value of the day given an hour, minute, second representation

        :param hr: hour of day
        :type hr: float
        :param m: minute of day
        :type m: float
        :param s: second of day
        :type s: float
        :return: the time in days
        :rtype: float
        """
        return hr / HOURS_IN_DAY + m / MINUTES_IN_DAY + s / SECONDS_IN_DAY

    @staticmethod
    def dms_to_radians(d: float, m: float, s: float) -> float:
        """calculate an angle in radians that has been defined in degrees, minutes, and seconds

        :param d: degrees in angle
        :type d: float
        :param m: minute of angle
        :type m: float
        :param s: second of angle
        :type s: float
        :return: angle in radians
        :rtype: float
        """
        return radians(d + m / MINUTES_IN_HOUR + s / SECONDS_IN_HOUR)


def sign(num: float) -> float:
    """function to determine if a value is positive or negative

    :param num: expression to be signed
    :type num: float
    :return: 1 if positive -1 if negative 0 if neither
    :rtype: float
    """
    val = 0
    if num > 0:
        val = 1
    elif num < 0:
        val = -1
    return val


class LegendrePolynomial:
    def __init__(self, phi: float) -> None:
        """stores the explicit solution to normalized legendre polynomials used in the geopotential calculations

        :param phi: geodetic latitude in radians
        :type phi: float
        """
        cos_phi: float = cos(phi)
        sin_phi: float = sin(phi)
        cos_phi_squared: float = cos_phi * cos_phi
        sin_phi_squared: float = sin_phi * sin_phi

        #: the polynomial list of lists with indices n, m
        self.p: List[List[float]] = [
            [1, 0],
            [sin_phi, cos_phi, 0],
            [
                (3 * sin_phi_squared - 1) * 0.5,
                3 * sin_phi * cos_phi,
                3 * cos_phi_squared,
                0,
            ],
            [
                sin_phi * (5 * sin_phi_squared - 3) * 0.5,
                (15 * sin_phi_squared - 3) * cos_phi * 0.5,
                15 * sin_phi * cos_phi_squared,
                15 * cos_phi_squared * cos_phi,
                0,
            ],
            [
                0.125 * (35 * sin_phi_squared * sin_phi_squared - 30 * sin_phi_squared + 3),
                2.5 * (7 * sin_phi_squared * sin_phi - 3 * sin_phi) * cos_phi,
                (7 * sin_phi_squared - 1) * cos_phi_squared * 7.5,
                105 * cos_phi * cos_phi_squared * sin_phi,
                105 * cos_phi_squared * cos_phi_squared,
                0,
            ],
        ]


class Eccentricity:
    """Class used to solve eccentricity of an ellipse (e)"""

    @staticmethod
    def from_a_c(a: float, c: float) -> float:
        """calculate eccentricity

        :param a: semi-major axis
        :type a: float
        :param c: half the distance between focii
        :type c: float
        :return: eccentricity
        :rtype: float
        """
        return c / a

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        """calculate eccentricity

        :param a: semi-major axis
        :type a: float
        :param b: semi-minor axis
        :type b: float
        :return: eccentricity
        :rtype: float
        """
        return sqrt(a * a - b * b) / a


class Flattening:
    """class used to solve flattening of an ellipse (f)"""

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        """calculate flattening

        :param a: semi-major axis
        :type a: float
        :param b: semi-minor axis
        :type b: float
        :return: flattening
        :rtype: float
        """
        return (a - b) / a


class SemiMajorAxis:
    """class used to solve semi-major axis of an ellipse (a)"""

    @staticmethod
    def from_mu_n(mu: float, n: float) -> float:
        """calculate semi-major axis

        :param mu: gravitational constant time mass of central body
        :type mu: float
        :param n: mean motion in radians/s
        :type n: float
        :return: semi-major axis
        :rtype: float
        """
        return (mu / (n * n)) ** (1 / 3)

    @staticmethod
    def from_mu_tau(mu: float, tau: float) -> float:
        """calculate semi-major axis

        :param mu: gravitational constant times mass of central body
        :type mu: float
        :param tau: period in seconds
        :type tau: float
        :return: semi-major axis
        :rtype: float
        """
        base: float = tau / (2 * pi)
        return (mu * base * base) ** (1 / 3)

    @staticmethod
    def from_mu_r_v(mu: float, r: float, v: float) -> float:
        """calculate the semi-major axis in km

        :param mu: gravitational constant times mass of central body
        :type mu: float
        :param r: magnitude of the position vector in km
        :type r: float
        :param v: magnitude of the velocity vector in km/s
        :type v: float
        :return: semi-major axis in km
        :rtype: float
        """
        return 1 / (2 / r - v * v / mu)


class SemiMinorAxis:
    """class used to solve semi-minor axis of an ellipse (b)" """

    @staticmethod
    def from_a_e(a: float, e: float) -> float:
        """calculate semi-minor axis

        :param a: semi-major axis
        :type a: float
        :param e: eccentricity
        :type e: float
        :return: semi-minor axis
        :rtype: float
        """
        return a * sqrt(1 - e * e)


class SemiParameter:
    """class used to solve the semi-parameter of an ellipse (p)"""

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        """calculate the semi-parameter

        :param a: semi-major axis
        :type a: float
        :param b: semi-minor axis
        :type b: float
        :return: semi-parameter
        :rtype: float
        """
        return b * b / a

    @staticmethod
    def from_a_e(a: float, e: float) -> float:
        """calculate the semi-parameter

        :param a: semi-major axis
        :type a: float
        :param e: eccentricity
        :type e: float
        :return: semi-parameter
        :rtype: float
        """
        return a * (1 - e * e)

    @staticmethod
    def from_mu_h(mu: float, h: float) -> float:
        """calculate the semi-parameter

        :param mu: gravitational constant time mass of central body
        :type mu: float
        :param h: areal velocity
        :type h: float
        :return: semi-parameter
        :rtype: float
        """
        return h * h / mu


class ArealVelocity:
    """class used to calculate areal velocities of an orbit (h)"""

    @staticmethod
    def from_r_v_phi(r: float, v: float, phi: float) -> float:
        """calculate the areal velocity

        :param r: magnitude of the position vector
        :type r: float
        :param v: magnitude of the velocity vector
        :type v: float
        :param phi: flight path angle (90 - angle between r and v)
        :type phi: float
        :return: areal velocity
        :rtype: float
        """
        return r * v * cos(phi)

    @staticmethod
    def from_mu_p(mu: float, p: float) -> float:
        """calculate the areal velocity

        :param mu: gravitational constant times mass of central body
        :type mu: float
        :param p: semi-parameter
        :type p: float
        :return: areal velocity
        :rtype: float
        """
        return sqrt(mu * p)


class SpecificMechanicalEnergy:
    """class used to solve specific mechanical energy (Xi)"""

    @staticmethod
    def from_mu_r_v_r(mu: float, r: float, v: float, body_r: float) -> float:
        """calculate the specific mechanical energy

        :param mu: gravitational constant times mass of central body
        :type mu: float
        :param r: distance from center of central body
        :type r: float
        :param v: magnitude of velocity vector
        :type v: float
        :param body_r: radius of central body
        :type body_r: float
        :return: specific mechanical energy
        :rtype: float
        """
        return v * v * 0.5 - mu / r + mu / body_r


class VisVivaVelocity:
    """class used to calculate the velocity of an orbit (v)"""

    @staticmethod
    def from_a_mu_r(a: float, mu: float, r: float) -> float:
        """calculate magnitude of velocity

        :param a: semi-major axis
        :type a: float
        :param mu: gravitational constant times mass
        :type mu: float
        :param r: distance from center of central body
        :type r: float
        :return: velocity magnitude
        :rtype: float
        """
        return sqrt(mu * (2 / r - 1 / a))


class Period:
    """class used to calculate the period of an orbit (tau)"""

    @staticmethod
    def from_a_mu(a: float, mu: float) -> float:
        """calculate the number of seconds required for a satellite to complete one revolution

        :param a: semi-major axis
        :type a: float
        :param mu: gravitational constant times mass of central body
        :type mu: float
        :return: period
        :rtype: float
        """
        return 2 * pi * sqrt(a * a * a / mu)


class MeanMotion:
    """class used to calculate mean motion of an orbit (n)"""

    @staticmethod
    def from_a_mu(a: float, mu: float) -> float:
        """calculate the mean motion

        :param a: semi-major axis
        :type a: float
        :param mu: gravitational constant times mass of central body
        :type mu: float
        :return: mean motion in radians/s
        :rtype: float
        """
        return sqrt(mu / (a * a * a))

    @staticmethod
    def from_tau(tau: float) -> float:
        """calculate mean motion

        :param tau: period of orbit in seconds
        :type tau: float
        :return: mean motion in radians/s
        :rtype: float
        """
        return 2 * pi / tau


class EOM:
    """class used to solve equations of motion"""

    #: used to solve semi-major axis
    A = SemiMajorAxis

    #: used to solve semi-minor axis
    B = SemiMinorAxis

    #: used to solve semi-parameter
    P = SemiParameter

    #: used to solve eccentricity
    E = Eccentricity

    #: used to solve period
    TAU = Period

    #: used to solve mean motion
    N = MeanMotion

    #: used to solve velocity
    V = VisVivaVelocity

    #: used to solve specific mechanical energy
    XI = SpecificMechanicalEnergy

    #: used to solve areal velocity
    H = ArealVelocity

    #: used to solve flattening
    F = Flattening
