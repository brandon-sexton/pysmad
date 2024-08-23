from math import cos, radians, sin, sqrt

from pysmad.constants import SECONDS_IN_SIDEREAL_DAY
from pysmad.math.functions import Conversions, EquationsOfMotion
from pysmad.math.linalg import Matrix3D, Vector3D
from pysmad.time import Epoch


class Earth:
    """Class used to store Earth properties"""

    #: normalized c coefficients used for geopotential calculation
    C: list[list[float]] = [
        [1],
        [0, 0],
        [-0.484165143790815e-3 / sqrt(0.2), -0.206615509074176e-9 / sqrt(0.6), 0.243938357328313e-5 / sqrt(2.4)],
        [
            0.957161207093473e-6 / sqrt(1 / 7),
            0.203046201047864e-5 / sqrt(6 / 7),
            0.904787894809528e-6 / sqrt(60 / 7),
            0.721321757121568e-6 / sqrt(360 / 7),
        ],
        [
            0.539965866638991e-6 / sqrt(24 / 216),
            -0.536157389388867e-6 / sqrt(10 / 9),
            0.350501623962649e-6 / sqrt(20),
            0.990856766672321e-6 / sqrt(280),
            -0.188519633023033e-6 / sqrt(2240),
        ],
    ]

    #: normalized s coefficients used for geopotential calculation
    S: list[list[float]] = [
        [0],
        [0, 0],
        [0, 0.138441389137979e-8 / sqrt(0.6), -0.140027370385934e-5 / sqrt(2.4)],
        [
            0,
            0.248200415856872e-6 / sqrt(6 / 7),
            -0.619005475177618e-6 / sqrt(60 / 7),
            0.141434926192941e-5 / sqrt(360 / 7),
        ],
        [
            0,
            -0.473567346518086e-6 / sqrt(10 / 9),
            0.662480026275829e-6 / sqrt(20),
            -0.200956723567452e-6 / sqrt(280),
            0.308803882149194e-6 / sqrt(2240),
        ],
    ]

    #: the number of zonal and tesseral terms to be used in the gravity calculation
    DEGREE_AND_ORDER: int = len(S)

    #: G*M given in km^3/s^2
    MU: float = 398600.4418

    #: distance from earth center to surface at the equator in km
    RADIUS: float = 6378.137

    #: value defining the ellipsoid of an oblate earth
    FLATTENING: float = 1 / 298.2572235

    #: inclination of ecliptic relative to earth equator in radians
    OBLIQUITY_OF_ECLIPTIC: float = radians(23.43929111)

    #: boolean identifying if gravity will be modeled as a point-source or with non-spherical methods
    USE_GEODETIC_MODEL = True

    @staticmethod
    def obliquity_of_ecliptic_at_epoch(epoch: Epoch) -> float:
        """calculate the obliquity of ecliptic (epsilon) at a given epoch

        :param epoch: time of interest
        :type epoch: Epoch
        :return: true-of-date epsilon
        :rtype: float
        """
        # Equation 5.39
        t = Epoch.julian_centuries_past_j2000(epoch.ut1)

        a = Conversions.dms_to_radians(0, 0, 46.815)
        b = Conversions.dms_to_radians(0, 0, 0.00059)
        c = Conversions.dms_to_radians(0, 0, 0.001813)

        # Equation 5.42
        return Earth.OBLIQUITY_OF_ECLIPTIC - a * t - b * t * t + c * t * t * t

    @staticmethod
    def geo_radius() -> float:
        """calculate the radius of an orbit with a period equal to that of Earth's rotation

        :return: geosynchronous radius in km
        :rtype: float
        """
        return EquationsOfMotion.A.from_mu_tau(Earth.MU, SECONDS_IN_SIDEREAL_DAY)

    @staticmethod
    def rotation(epoch: Epoch) -> Matrix3D:
        """creates a matrix that can be used to transform an itrf position to tod and vice versa

        :param epoch: valid time of the state
        :type epoch: Epoch
        :return: transformation matrix
        :rtype: Matrix3D
        """
        d: float = Epoch.days_past_j2000(epoch.tt)
        arg1: float = radians(125.0 - 0.05295 * d)
        arg2: float = radians(200.9 + 1.97129 * d)
        a: float = radians(-0.0048)
        b: float = radians(0.0004)
        dpsi: float = a * sin(arg1) - b * sin(arg2)
        eps: float = Earth.obliquity_of_ecliptic_at_epoch(epoch)
        gmst: float = epoch.greenwich_hour_angle()
        gast: float = dpsi * cos(eps) + gmst
        return Vector3D.rotation_matrix(Vector3D(0, 0, 1), -gast)

    @staticmethod
    def precession(epoch: Epoch) -> Matrix3D:
        """creates a matrix that can be used to transform a tod position to mod and vice versa

        :param epoch: valid time of the state
        :type epoch: Epoch
        :return: transformation matrix
        :rtype: Matrix3D
        """
        t: float = Epoch.julian_centuries_past_j2000(epoch.ut1)
        a: float = Conversions.dms_to_radians(0, 0, 2306.2181)
        b: float = Conversions.dms_to_radians(0, 0, 0.30188)
        c: float = Conversions.dms_to_radians(0, 0, 0.017998)
        x: float = a * t + b * t * t + c * t * t * t

        a = Conversions.dms_to_radians(0, 0, 2004.3109)
        b = Conversions.dms_to_radians(0, 0, 0.42665)
        c = Conversions.dms_to_radians(0, 0, 0.041833)
        y: float = a * t - b * t * t - c * t * t * t

        a = Conversions.dms_to_radians(0, 0, 0.7928)
        b = Conversions.dms_to_radians(0, 0, 0.000205)
        z: float = x + a * t * t + b * t * t * t

        sz = sin(z)
        sy = sin(y)
        sx = sin(x)
        cz = cos(z)
        cy = cos(y)
        cx = cos(x)

        return Matrix3D(
            Vector3D(-sz * sx + cz * cy * cx, -sz * cx - cz * cy * sx, -cz * sy),
            Vector3D(cz * sx + sz * cy * cx, cz * cx - sz * cy * sx, -sz * sy),
            Vector3D(sy * cx, -sy * sx, cy),
        )

    @staticmethod
    def nutation(epoch: Epoch) -> Matrix3D:
        """creates a matrix that can be used to transform a mod position to gcrf and vice versa

        :param epoch: valid time of the state
        :type epoch: Epoch
        :return: transformation matrix
        :rtype: Matrix3D
        """
        d = Epoch.days_past_j2000(epoch.tt)
        arg1 = radians(125.0 - 0.05295 * d)
        arg2 = radians(200.9 + 1.97129 * d)
        a = radians(-0.0048)
        b = radians(0.0004)
        dpsi = a * sin(arg1) - b * sin(arg2)
        a = radians(0.0026)
        b = radians(0.0002)
        deps = a * cos(arg1) + b * cos(arg2)
        eps = Earth.obliquity_of_ecliptic_at_epoch(epoch)

        ce = cos(eps)
        se = sin(eps)

        return Matrix3D(
            Vector3D(1.0, -dpsi * ce, -dpsi * se),
            Vector3D(dpsi * ce, 1.0, -deps),
            Vector3D(dpsi * se, deps, 1.0),
        )
