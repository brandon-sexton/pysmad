from math import cos, radians, sin
from pathlib import Path

from pysmad.bodies._geodetic_model import GeodeticModel
from pysmad.constants import ARC_SECONDS_TO_RADIANS, EARTH_MU, OBLIQUITY_OF_ECLIPTIC, SECONDS_IN_SIDEREAL_DAY
from pysmad.coordinates import CartesianVector
from pysmad.math import EquationsOfMotion
from pysmad.math.linalg import Matrix3D
from pysmad.time import Epoch


class Earth:
    """Class used to store Earth properties"""

    detic_model = GeodeticModel(Path(__file__).parent / "EGM96.potential")

    #: boolean identifying if gravity will be modeled as a point-source or with non-spherical methods
    USE_GEODETIC_MODEL = True

    @staticmethod
    def mu() -> float:
        return Earth.detic_model.mu

    @staticmethod
    def radius() -> float:
        return Earth.detic_model.radius

    @staticmethod
    def obliquity_of_ecliptic_at_epoch(epoch: Epoch) -> float:
        """calculate the true-of-date obliquity of ecliptic (epsilon) at a given epoch

        :param epoch: time of interest
        """
        # Equation 5.39
        t = Epoch.julian_centuries_past_j2000(epoch.ut1)

        a = 46.815 * ARC_SECONDS_TO_RADIANS
        b = 0.00059 * ARC_SECONDS_TO_RADIANS
        c = 0.001813 * ARC_SECONDS_TO_RADIANS

        # Equation 5.42
        return OBLIQUITY_OF_ECLIPTIC - a * t - b * t * t + c * t * t * t

    @staticmethod
    def geo_radius() -> float:
        """calculate the radius of an orbit with a period equal to that of Earth's rotation"""
        return EquationsOfMotion.semi_major_axis.from_mu_tau(EARTH_MU, SECONDS_IN_SIDEREAL_DAY)

    @staticmethod
    def rotation(epoch: Epoch) -> Matrix3D:
        """creates a matrix that can be used to transform an EFG position to TOD and vice versa

        :param epoch: valid time of the state
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
        return Matrix3D.rotation_matrix(CartesianVector.z_axis(), -gast)

    @staticmethod
    def precession(epoch: Epoch) -> Matrix3D:
        """creates a matrix that can be used to transform a TOD position to MOD and vice versa

        :param epoch: valid time of the state
        """
        t: float = Epoch.julian_centuries_past_j2000(epoch.ut1)
        a: float = 2306.2181 * ARC_SECONDS_TO_RADIANS
        b: float = 0.30188 * ARC_SECONDS_TO_RADIANS
        c: float = 0.017998 * ARC_SECONDS_TO_RADIANS
        x: float = a * t + b * t * t + c * t * t * t

        a = 2004.3109 * ARC_SECONDS_TO_RADIANS
        b = 0.42665 * ARC_SECONDS_TO_RADIANS
        c = 0.041833 * ARC_SECONDS_TO_RADIANS
        y: float = a * t - b * t * t - c * t * t * t

        a = 0.79280 * ARC_SECONDS_TO_RADIANS
        b = 0.000205 * ARC_SECONDS_TO_RADIANS
        z: float = x + a * t * t + b * t * t * t

        sz = sin(z)
        sy = sin(y)
        sx = sin(x)
        cz = cos(z)
        cy = cos(y)
        cx = cos(x)

        return Matrix3D(
            CartesianVector(-sz * sx + cz * cy * cx, -sz * cx - cz * cy * sx, -cz * sy),
            CartesianVector(cz * sx + sz * cy * cx, cz * cx - sz * cy * sx, -sz * sy),
            CartesianVector(sy * cx, -sy * sx, cy),
        )

    @staticmethod
    def nutation(epoch: Epoch) -> Matrix3D:
        """creates a matrix that can be used to transform a MOD position to J2000 and vice versa

        :param epoch: valid time of the state
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
            CartesianVector(1.0, -dpsi * ce, -dpsi * se),
            CartesianVector(dpsi * ce, 1.0, -deps),
            CartesianVector(dpsi * se, deps, 1.0),
        )
