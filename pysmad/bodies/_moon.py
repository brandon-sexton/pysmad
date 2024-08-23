from math import cos, radians, sin

from pysmad.bodies._earth import Earth
from pysmad.math.functions import Conversions
from pysmad.math.linalg import Vector3D
from pysmad.time import Epoch


class Moon:
    """class used to store properties of the moon to be used in force modeling"""

    #: G*M in km^3/s^2
    MU = 4902.800305555

    #: distance from center of moon to surface in km
    RADIUS = 1737.4000

    @staticmethod
    def get_position(epoch: Epoch) -> Vector3D:
        """calculate ECI position of moon

        :param epoch: time of calculated position vector
        :type epoch: Epoch
        :return: ECI position in km
        :rtype: Vector3D
        """
        # Equation 3.47
        t = Epoch.julian_centuries_past_j2000(epoch.tt)
        l0 = radians(218.31617 + 481267.88088 * t - 1.3972 * t)
        l = radians(134.96292 + 477198.86753 * t)
        lp = radians(357.52543 + 35999.04944 * t)
        f = radians(93.27283 + 483202.01873 * t)
        d = radians(297.85027 + 445267.11135 * t)

        # Auxiliary variables to store the angles defined in seconds in equation 3.48
        a0 = Conversions.dms_to_radians(0, 0, 22640.0)
        a1 = Conversions.dms_to_radians(0, 0, 769.0)
        a2 = Conversions.dms_to_radians(0, 0, 4586.0)
        a3 = Conversions.dms_to_radians(0, 0, 2370.0)
        a4 = Conversions.dms_to_radians(0, 0, 668.0)
        a5 = Conversions.dms_to_radians(0, 0, 412.0)
        a6 = Conversions.dms_to_radians(0, 0, 212.0)
        a7 = Conversions.dms_to_radians(0, 0, 206.0)
        a8 = Conversions.dms_to_radians(0, 0, 192.0)
        a9 = Conversions.dms_to_radians(0, 0, 165.0)
        a10 = Conversions.dms_to_radians(0, 0, 148.0)
        a11 = Conversions.dms_to_radians(0, 0, 125.0)
        a12 = Conversions.dms_to_radians(0, 0, 110.0)
        a13 = Conversions.dms_to_radians(0, 0, 55.0)

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
        a0 = Conversions.dms_to_radians(0, 0, 18520.0)
        a1 = Conversions.dms_to_radians(0, 0, 412.0)
        a2 = Conversions.dms_to_radians(0, 0, 541.0)
        a3 = Conversions.dms_to_radians(0, 0, 526.0)
        a4 = Conversions.dms_to_radians(0, 0, 44.0)
        a5 = Conversions.dms_to_radians(0, 0, 31.0)
        a6 = Conversions.dms_to_radians(0, 0, 25.0)
        a7 = Conversions.dms_to_radians(0, 0, 23.0)
        a8 = Conversions.dms_to_radians(0, 0, 21.0)
        a9 = Conversions.dms_to_radians(0, 0, 11.0)

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

        eps = Earth.OBLIQUITY_OF_ECLIPTIC

        return Vector3D(x, y, z).rotation_about_axis(Vector3D(1, 0, 0), eps)
