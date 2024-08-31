from math import cos, radians, sin

from pysmad.constants import ARC_SECONDS_TO_RADIANS, OBLIQUITY_OF_ECLIPTIC
from pysmad.coordinates import CartesianVector
from pysmad.math.linalg import Matrix3D
from pysmad.time import Epoch


class Moon:
    """class used to store properties of the moon to be used in force modeling"""

    @staticmethod
    def get_position(epoch: Epoch) -> CartesianVector:
        """calculate J2000 ECI position in :math:`km` of the Moon at a given epoch

        :param epoch: time of calculated position vector
        """
        # Equation 3.47
        t = Epoch.julian_centuries_past_j2000(epoch.tt)
        l0 = radians(218.31617 + 481267.88088 * t - 1.3972 * t)
        l = radians(134.96292 + 477198.86753 * t)
        lp = radians(357.52543 + 35999.04944 * t)
        f = radians(93.27283 + 483202.01873 * t)
        d = radians(297.85027 + 445267.11135 * t)

        # Auxiliary variables to store the angles defined in seconds in equation 3.48
        a0: float = 22640.0 * ARC_SECONDS_TO_RADIANS
        a1: float = 769.0 * ARC_SECONDS_TO_RADIANS
        a2: float = 4586.0 * ARC_SECONDS_TO_RADIANS
        a3: float = 2370.0 * ARC_SECONDS_TO_RADIANS
        a4: float = 668.0 * ARC_SECONDS_TO_RADIANS
        a5: float = 412.0 * ARC_SECONDS_TO_RADIANS
        a6: float = 212.0 * ARC_SECONDS_TO_RADIANS
        a7: float = 206.0 * ARC_SECONDS_TO_RADIANS
        a8: float = 192.0 * ARC_SECONDS_TO_RADIANS
        a9: float = 165.0 * ARC_SECONDS_TO_RADIANS
        a10: float = 148.0 * ARC_SECONDS_TO_RADIANS
        a11: float = 125.0 * ARC_SECONDS_TO_RADIANS
        a12: float = 110.0 * ARC_SECONDS_TO_RADIANS
        a13: float = 55.0 * ARC_SECONDS_TO_RADIANS

        # Equation 3.48
        lam = (
            l0
            + a0 * sin(l)
            + a1 * sin(2 * l)
            - a2 * sin(l - 2.0 * d)
            + a3 * sin(2.0 * d)
            - a4 * sin(lp)
            - a5 * sin(2.0 * f)
            - a6 * sin(2.0 * l - 2.0 * d)
            - a7 * sin(l + lp - 2.0 * d)
            + a8 * sin(l + 2.0 * d)
            - a9 * sin(lp - 2.0 * d)
            + a10 * sin(l - lp)
            - a11 * sin(d)
            - a12 * sin(l + lp)
            - a13 * sin(2.0 * f - 2.0 * d)
        )

        # Redefined variables for angles in equation 3.49
        a0 = 18520.0 * ARC_SECONDS_TO_RADIANS
        a1 = 412.0 * ARC_SECONDS_TO_RADIANS
        a2 = 541.0 * ARC_SECONDS_TO_RADIANS
        a3 = 526.0 * ARC_SECONDS_TO_RADIANS
        a4 = 44.0 * ARC_SECONDS_TO_RADIANS
        a5 = 31.0 * ARC_SECONDS_TO_RADIANS
        a6 = 25.0 * ARC_SECONDS_TO_RADIANS
        a7 = 23.0 * ARC_SECONDS_TO_RADIANS
        a8 = 21.0 * ARC_SECONDS_TO_RADIANS
        a9 = 11.0 * ARC_SECONDS_TO_RADIANS

        # Equation 3.49
        beta = (
            a0 * sin(f + lam - l0 + a1 * sin(2.0 * f + a2 * sin(lp)))
            - a3 * sin(f - 2.0 * d)
            + a4 * sin(l + f - 2.0 * d)
            - a5 * sin(-l + f - 2.0 * d)
            - a6 * sin(-2.0 * l + f)
            - a7 * sin(lp + f - 2.0 * d)
            + a8 * sin(-l + f)
            + a9 * sin(-lp + f - 2.0 * d)
        )

        # Equation 3.50
        r = (
            385000.0
            - 20905.0 * cos(l)
            - 3699.0 * cos(2.0 * d - l)
            - 2956.0 * cos(2.0 * d)
            - 570.0 * cos(2.0 * l)
            + 246.0 * cos(2.0 * l - 2.0 * d)
            - 205.0 * cos(lp - 2.0 * d)
            - 171.0 * cos(l + 2.0 * d)
            - 152.0 * cos(l + lp - 2.0 * d)
        )

        # Equation 3.51
        x = r * cos(lam) * cos(beta)
        y = r * sin(lam) * cos(beta)
        z = r * sin(beta)

        eps = OBLIQUITY_OF_ECLIPTIC

        return Matrix3D.rotation_matrix(CartesianVector.x_axis(), eps).multiply_vector(CartesianVector(x, y, z))
