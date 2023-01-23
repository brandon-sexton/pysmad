from math import atan2, cos, pi, radians, sin, sqrt
from typing import List

from openspace.math.constants import HOURS_IN_DAY, MINUTES_IN_DAY, MINUTES_IN_HOUR, SECONDS_IN_DAY, SECONDS_IN_HOUR
from openspace.math.linalg import Vector3D


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
    r"""Class used to solve eccentricity of an ellipse

    .. note::

       eccentricity will commonly be referenced as :math:`e` in documentation"""

    @staticmethod
    def from_a_c(a: float, c: float) -> float:
        r"""calculate eccentricity using equation 1-2 in :ref:`vallado`

        .. math::

           e = \frac{c}{a}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param c: half the distance between focii in :math:`km`
        :type c: float
        :return: eccentricity
        :rtype: float

        .. note::

           This method works any time :math:`a` and :math:`c` are input with common units,
           but :math:`km` is the preferred unit throughout this package to ensure computational
           consistency and accuracy.
        """
        return c / a

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        r"""calculate eccentricity using equation 1-6 in :ref:`vallado`

        .. math::

           e = \frac{\sqrt{a^2-b^2}}{a}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param b: semi-minor axis in :math:`km`
        :type b: float
        :return: eccentricity
        :rtype: float

        .. note::

           This method works any time :math:`a` and :math:`b` are input with common units,
           but :math:`km` is the preferred unit throughout this package to ensure computational
           consistency and accuracy.
        """
        return sqrt(a * a - b * b) / a

    @staticmethod
    def from_a_p(a: float, p: float) -> float:
        r"""calculate eccentricity using equation 2.62 in :ref:`orbits`

        .. math::

           e = \sqrt{1 - \frac{p}{a}}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param p: semi-parameter in :math:`km`
        :type p: float
        :return: eccentricity
        :rtype: float

        .. note::

           This method works any time :math:`a` and :math:`p` are input with common units,
           but :math:`km` is the preferred unit throughout this package to ensure computational
           consistency and accuracy.
        """
        return sqrt(1 - p / a)


class Flattening:
    r"""class used to solve flattening of an ellipse

    .. note::

       flattening will commonly be referenced as :math:`f` in documentation"""

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        r"""calculate flattening using equation 1-3 in :ref:`vallado`

        .. math::

           f = \frac{a-b}{a}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param b: semi-minor axis in :math:`km`
        :type b: float
        :return: flattening
        :rtype: float
        """
        return (a - b) / a


class SemiMajorAxis:
    """class used to solve semi-major axis of an ellipse

    .. note::

       the semi-major axis will commonly be referenced as :math:`a` in documentation
    """

    @staticmethod
    def from_mu_n(mu: float, n: float) -> float:
        r"""calculate semi-major axis using equation 1-29 in :ref:`vallado`

        .. math::

           a = \sqrt[3]{\frac{\mu}{n^2}}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param n: mean motion in :math:`\frac{rad}{s}`
        :type n: float
        :return: semi-major axis in :math:`km`
        :rtype: float
        """
        return (mu / (n * n)) ** (1 / 3)

    @staticmethod
    def from_mu_tau(mu: float, tau: float) -> float:
        r"""calculate semi-major axis using equation 1-27 in :ref:`vallado`

        .. math::

           n = \frac{2\pi}{\tau} = \sqrt{\frac{\mu}{a^3}}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param tau: period in :math:`s`
        :type tau: float
        :return: semi-major axis in :math:`km`
        :rtype: float
        """
        base: float = tau / (2 * pi)
        return (mu * base * base) ** (1 / 3)

    @staticmethod
    def from_mu_r_v(mu: float, r: float, v: float) -> float:
        r"""calculate the semi-major axis in km using equation 1-31 in :ref:`vallado`

        .. math::

           v = \sqrt{\frac{2\mu}{r}+\frac{\mu}{a}}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param r: magnitude of the position vector in :math:`km`
        :type r: float
        :param v: magnitude of the velocity vector in :math:`\frac{km}{s}`
        :type v: float
        :return: semi-major axis in :math:`km`
        :rtype: float
        """
        return 1 / (2 / r - v * v / mu)


class SemiMinorAxis:
    """class used to solve semi-minor axis of an ellipse

    .. note::

    the semi-minor axis will commonly be referenced as :math:`b` in documentation"""

    @staticmethod
    def from_a_e(a: float, e: float) -> float:
        r"""calculate semi-minor axis using equation 1-4 in :ref:`vallado`

        .. math::

           b = a\sqrt{1-e^2}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param e: eccentricity
        :type e: float
        :return: semi-minor axis in :math:`km`
        :rtype: float
        """
        return a * sqrt(1 - e * e)


class SemiParameter:
    """class used to solve the semi-parameter of an ellipse

    .. note::

    the semi-parameter will commonly be referenced as :math:`p` in documentation"""

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        r"""calculate the semi-parameter using equation 1-9 in :ref:`vallado`

        .. math::

           p = \frac{b^2}{a}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param b: semi-minor axis in :math:`km`
        :type b: float
        :return: semi-parameter in :math:`km`
        :rtype: float
        """
        return b * b / a

    @staticmethod
    def from_a_e(a: float, e: float) -> float:
        r"""calculate the semi-parameter using equation 1-10 in :ref:`vallado`

        .. math::

           p = a(1-e^2)

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param e: eccentricity
        :type e: float
        :return: semi-parameter in :math:`km`
        :rtype: float
        """
        return a * (1 - e * e)

    @staticmethod
    def from_mu_h(mu: float, h: float) -> float:
        r"""calculate the semi-parameter using equation 1-19 in :ref:`vallado`

        .. math::

           p = \frac{h^2}{\mu}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param h: areal velocity magnitude in :math:`\frac{km^2}{s}`
        :type h: float
        :return: semi-parameter in :math:`km`
        :rtype: float
        """
        return h * h / mu


class ArealVelocity:
    r"""class used to calculate areal velocities of an orbit

    .. note::
       The term areal velocity is used synonymously for the momentum of an orbit
       and will commonly be referenced as :math:`h` in documentation

    """

    @staticmethod
    def from_r_v_phi(r: float, v: float, phi: float) -> float:
        r"""calculate the areal velocity using equation 1-16 in :ref:`vallado`

        .. math::

           h = rv\cos{(\phi_{fpa})}

        :param r: magnitude of the position vector in :math:`km`
        :type r: float
        :param v: magnitude of the velocity vector in :math:`\frac{km}{s}`
        :type v: float
        :param phi: flight path angle :math:`\frac{\pi}{2} - \measuredangle\vec{r}\vec{v}`
        :type phi: float
        :return: areal velocity in :math:`\frac{km^2}{s}`
        :rtype: float
        """
        return r * v * cos(phi)

    @staticmethod
    def from_mu_p(mu: float, p: float) -> float:
        r"""calculate the areal velocity using equation 1-19 in :ref:`vallado`

        .. math::

           h = \sqrt{{\mu}p}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param p: semi-parameter in :math:`km`
        :type p: float
        :return: areal velocity in :math:`\frac{km^2}{s}`
        :rtype: float
        """
        return sqrt(mu * p)

    @staticmethod
    def from_r_v(r: Vector3D, v: Vector3D) -> Vector3D:
        r"""calculate the momentum vector using equation 1-15 in :ref:`vallado`

        .. math::

           \vec{h} = \vec{r} \times \vec{v}

        :param r: position vector in :math:`km`
        :type r: Vector3D
        :param v: velocity vector in :math:`\frac{km}{s}`
        :type v: Vector3D
        :return: areal velocity vector in :math:`\frac{km^2}{s}`
        :rtype: Vector3D
        """
        return r.cross(v)


class RAAN:
    r"""static class used to solve right ascension of ascending node (RAAN)

    .. note::

       RAAN will commonly be referenced as :math:`\Omega` in documentation
    """

    @staticmethod
    def from_w(w: Vector3D) -> float:
        r"""calculate the right ascension of the ascending node

        .. math::

           \Omega = \arctan{(-\frac{\vec{w}_{x}}{\vec{w}_{y}})}

        :param w: normalized momentum vector in :math:`\frac{km^2}{s}`
        :type w: Vector3D
        :return: right ascension of the ascending node in :math:`rad` where :math:`0 \leq \Omega < 2\pi`
        :rtype: float

        .. todo::

           document equation reference from Satellite Orbits
        """
        return (atan2(w.x, -w.y) + 2 * pi) % (2 * pi)


class Inclination:
    r"""static class used to solve inclination

    .. note::

       inclination will commonly be referenced as :math:`i` in documentation
    """

    @staticmethod
    def from_w(w: Vector3D) -> float:
        r"""calculate the inclination

        .. math::

           i = \arctan{
                \left(
                    \frac{
                        \sqrt{
                            \vec{w}_{x}^2 + \vec{w}_{y}^2
                        }
                    }{
                        \vec{w}_{z}
                    }
                \right)
            }

        :param w: normalized momentum vector :math:`\hat{h}` in :math:`\frac{km^2}{s}`
        :type w: Vector3D
        :return: inclination in :math:`rad` where :math:`0 \leq i < \pi`
        :rtype: float

        .. todo::

           document equation reference from Satellite Orbits
        """
        return atan2(sqrt(w.x * w.x + w.y * w.y), w.z)


class Radius:
    r"""static class used to solve the radius of an orbit

    .. note::

       radius will commonly be referenced as :math:`r` or :math:`R` in documentation
    """

    @staticmethod
    def from_p_e_nu(p: float, e: float, nu: float) -> float:
        r"""calculate the radius of an orbit using equation 1-24 in :ref:`vallado`

        .. math::

           r = \frac{p}{1+e\cos{(\nu)}}

        :param p: semi-parameter in :math:`km`
        :type p: float
        :param e: eccentricity
        :type e: float
        :param nu: true anomaly in :math:`rads`
        :type nu: float
        :return: radius in :math:`km`
        :rtype: float
        """
        return p / (1 + e * cos(nu))


class SpecificMechanicalEnergy:
    r"""static class used to solve specific mechanical energy

    .. note::

       SME will commonly be referenced as :math:`\xi` in documentation
    """

    @staticmethod
    def from_mu_r_v(mu: float, r: float, v: float) -> float:
        r"""calculate the specific mechanical energy using equation 1-20 in :ref:`vallado`

        .. math::

           \xi = \frac{v^2}{2} - \frac{\mu}{r}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param r: distance from center of central body in :math:`km`
        :type r: float
        :param v: magnitude of velocity vector in :math:`\frac{km}{s}`
        :type v: float
        :return: specific mechanical energy in :math:`\frac{km^2}{s^2}`
        :rtype: float
        """
        return v * v * 0.5 - mu / r

    @staticmethod
    def from_mu_a(mu: float, a: float) -> float:
        r"""calculate specific mechanical energy using equation 1-21 in :ref:`vallado`

        .. math::

           \xi = -\frac{\mu}{2a}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param a: semi-major axis in :math:`km`
        :type a: float
        :return: specific mechanical energy :math:`\frac{km^2}{s^2}`
        :rtype: float
        """
        return -0.5 * mu / a


class VisVivaVelocity:
    r"""class used to calculate the velocity of an orbit

    .. note::

       velocity will commonly be referenced as :math:`v` in documentation
    """

    @staticmethod
    def from_a_mu_r(a: float, mu: float, r: float) -> float:
        r"""calculate magnitude of velocity using equation 1-22 in :ref:`vallado`

        .. math::

           v^2 = \mu\left(\frac{2}{r} - \frac{1}{a}\right)

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param r: distance from center of central body in :math:`km`
        :type r: float
        :return: velocity magnitude in :math:`\frac{km}{s}`
        :rtype: float
        """
        return sqrt(mu * (2 / r - 1 / a))

    @staticmethod
    def from_mu_r_xi(mu: float, r: float, xi: float) -> float:
        r"""calculate the magnitude of velocity using equation 1-30 in :ref:`vallado`

        .. math::
           v = \sqrt{2\left(\frac{\mu}{r}+\xi\right)}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param r: distance from center of central body in :math:`km`
        :type r: float
        :param xi: specific mechanical energy in :math:`\frac{km^2}{s^2}`
        :type xi: float
        :return: velocity in :math:`\frac{km}{s}`
        :rtype: float
        """
        return sqrt(2 * (mu / r + xi))

    @staticmethod
    def from_mu_r_e_nu(mu: float, r: float, e: float, nu: float) -> float:
        r"""calculate the magnitude of velocity using equation 1-32 in :ref:`vallado`

        .. math::

           v = \sqrt{\frac{\mu}{r}\left(2 - \frac{1-e^2}{1+e\cos{\nu}}\right)}

        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :param r: distance from center of central body in :math:`km`
        :type r: float
        :param e: eccentricity
        :type e: float
        :param nu: true anomaly in :math:`rads`
        :type nu: float
        :return: velocity in :math:`\frac{km}{s}`
        :rtype: float
        """
        return sqrt((mu / r) * (2 - (1 - e * e) / (1 + e * cos(nu))))


class Period:
    r"""class used to calculate the period of an orbit

    .. note::

       period will commonly be referenced as :math:`\tau` in documentation"""

    @staticmethod
    def from_a_mu(a: float, mu: float) -> float:
        r"""calculate the period using equation 1-26 in :ref:`vallado`

        .. math::

           \tau = 2\pi\sqrt{\frac{a^3}{\mu}}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :return: period in :math:`s`
        :rtype: float
        """
        return 2 * pi * sqrt(a * a * a / mu)


class MeanMotion:
    r"""class used to calculate mean motion of an orbit

    .. note::

       mean motion will commonly be referenced as :math:`n` in documentation"""

    @staticmethod
    def from_a_mu(a: float, mu: float) -> float:
        r"""calculate the mean motion using equation 1-27 in :ref:`vallado`

        .. math::

           n = \frac{2\pi}{\tau} = \sqrt{\frac{\mu}{a^3}}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :return: mean motion in :math:`\frac{rad}{s}`
        :rtype: float
        """
        return sqrt(mu / (a * a * a))

    @staticmethod
    def from_tau(tau: float) -> float:
        r"""calculate mean motion using equation 1-27 in :ref:`vallado`

        .. math::

           n = \frac{2\pi}{\tau} = \sqrt{\frac{\mu}{a^3}}

        :param tau: period of orbit in :math:`s`
        :type tau: float
        :return: mean motion in :math:`\frac{rad}{s}`
        :rtype: float
        """
        return 2 * pi / tau


class EccentricAnomaly:
    r"""class used to solve eccentric anomaly

    .. note::

       eccentric anomaly will commonly be referenced as :math:`E` in documentation"""

    #: the tolerance used to stop the recursive solutions of Kepler's equation
    TOLERANCE: float = 1e-12

    @staticmethod
    def from_ma_e(ma: float, e: float) -> float:
        r"""calculate the eccentric anomaly using algorithm 2 in :ref:`vallado`

        .. math::

           E_{n+1} = E_n + \left(\frac{M-E_n+e\sin{(E_n)}}{1-e\cos{(E_n)}}\right)

        .. note::

           :math:`E_0 = M - e` for :math:`-\pi<M<0` or :math:`M>\pi`
           otherwise :math:`E_0 = M + e`

           looping continues until :math:`\vertE_{n+1} - E_n\vert < tolerance`

        :param ma: mean anomaly in :math:`rads`
        :type ma: float
        :param e: eccentricity
        :type e: float
        :return: eccentric anomaly in :math:`rads`
        :rtype: float
        """
        converged: bool = False
        ea0: float = ma
        num: float
        den: float

        if (ma > -pi and ma < 0) or ma > pi:
            ea0 -= e
        else:
            ea0 += e

        while not converged:
            ean = ea0 + (ma - ea0 + e * sin(ea0)) / (1 - e * cos(ea0))
            if abs(ean - ea0) < EccentricAnomaly.TOLERANCE:
                converged = True
            else:
                ea0 = ean

        return (ean + 2 * pi) % (2 * pi)

    @staticmethod
    def from_rdv_r_a_n(r_dot_v: float, r: float, a: float, n: float) -> float:
        r"""calculate eccentric anomaly

        :param r_dot_v: dot product of position and velocity
        :type r_dot_v: float
        :param r: magnitude of position in :math:`km`
        :type r: float
        :param a: semi-major axis in :math:`km`
        :type a: float
        :param n: mean motion in :math:`\frac{rad}{s}`
        :type n: float
        :return: eccentric anomaly in :math:`rads`
        :rtype: float

        .. todo::

           find equation reference
        """
        return (atan2(r_dot_v / (a * a * n), 1 - r / a) + 2 * pi) % (2 * pi)


class TrueAnomaly:
    r"""static class used to solve true anomaly

    .. note::

       true anomaly will commonly be referenced as :math:`\nu` in documentation
    """

    @staticmethod
    def from_e_ea(e: float, ea: float) -> float:
        """calculate true anomaly

        :param e: eccentricity
        :type e: float
        :param ea: eccentric anomaly in :math:`rads`
        :type ea: float
        :return: true anomaly in :math:`rads`
        :rtype: float

        .. todo::

           find equation reference
        """
        ta: float = atan2(sqrt(1 - e * e) * sin(ea), cos(ea) - e)
        if ta < 0:
            ta += 2 * pi
        return ta


class ArgumentOfPerigee:
    r"""static class used to solve argument of perigee

    .. note::

       argument of perigee will commonly be referenced as :math:`\omega` in documentation
    """

    @staticmethod
    def from_u_nu(u: float, nu: float) -> float:
        r"""calculate the argument of perigee

        :param u: argument of latitude in :math:`rads`
        :type u: float
        :param nu: true anomaly in :math:`rads`
        :type nu: float
        :return: argument of perigee in :math:`rads`
        :rtype: float

        .. todo::

           find equation reference
        """
        return (u - nu + 2 * pi) % (2 * pi)


class ArgumentOfLatitude:
    """static class used to solve argument of latitude

    .. note::

       argument of latitude will commonly be referenced as :math:`u` in documentation
    """

    @staticmethod
    def from_r_w(r: Vector3D, w: Vector3D) -> float:
        r"""calculate the argument of latitude

        :param r: position vector in :math:`km`
        :type r: Vector3D
        :param w: normalized areal velocity vector in :math:`\frac{km^2}{s}`
        :type w: Vector3D
        :return: argument of latitude in :math:`rads`
        :rtype: float

        .. todo::

           find equation reference
        """
        return (atan2(r.z, -r.x * w.y + r.y * w.x) + 2 * pi) % (2 * pi)


class MeanAnomaly:
    """static class used to solve mean anomaly

    .. note::

       mean anomaly will commonly be referenced as :math:`M` in documentation
    """

    @staticmethod
    def from_ea_e(ea: float, e: float) -> float:
        r"""calculate mean anomaly using equation 2-4 in :ref:`vallado`

        .. math::

           M = E - e\sin{(E)}

        :param ea: eccentric anomaly in :math:`rads`
        :type ea: float
        :param e: eccentricity
        :type e: float
        :return: mean anomaly in :math:`rads`
        :rtype: float
        """
        return (ea - e * sin(ea) + 2 * pi) % (2 * pi)


class EquationsOfMotion:
    """class used to solve equations of motion"""

    #: used to solve semi-major axis :math:`a`
    A = SemiMajorAxis

    #: used to solve semi-minor axis :math:`b`
    B = SemiMinorAxis

    #: used to solve semi-parameter :math:`p`
    P = SemiParameter

    #: used to solve eccentricity :math:`e`
    E = Eccentricity

    #: used to solve period :math:`tau`
    TAU = Period

    #: used to solve mean motion :math:`n`
    N = MeanMotion

    #: used to solve velocity :math:`v`
    V = VisVivaVelocity

    #: used to solve specific mechanical energy :math:`\xi`
    XI = SpecificMechanicalEnergy

    #: used to solve areal velocity :math:`h`
    H = ArealVelocity

    #: used to solve flattening :math:`f`
    F = Flattening

    #: used to solve eccentric anomaly :math:`E`
    EA = EccentricAnomaly

    #: used to solve inclination :math:`i`
    I = Inclination

    #: used to solve raan :math:`\Omega`
    RAAN = RAAN

    #: used to solve true anomaly :math:`\nu`
    NU = TrueAnomaly

    #: used to solve argument of perigee :math:`\omega`
    W = ArgumentOfPerigee

    #: used to solve argument of latitude :math:`u`
    U = ArgumentOfLatitude

    #: used to solve mean anomaly :math:`M`
    MA = MeanAnomaly
