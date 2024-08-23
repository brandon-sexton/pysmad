from math import cos, radians, sin

from pysmad.bodies._earth import Earth
from pysmad.math.functions import Conversions
from pysmad.math.linalg import Vector3D
from pysmad.time import Epoch


class Sun:
    """class used to store properties of the sun for a force model"""

    #: RAAN + argument of periapsis in radians
    W_PLUS_W = radians(282.94)

    #: cosine of obliquity of ecliptic
    COS_OBLIQUITY = cos(Earth.OBLIQUITY_OF_ECLIPTIC)

    #: sine of obliquity of ecliptic
    SIN_OBLIQUITY = sin(Earth.OBLIQUITY_OF_ECLIPTIC)

    #: G*M in km^3/s^
    MU = 1.327124400419e11

    #: Estimate of srp
    P = 4.56e-6

    #: Distance to earth in km
    AU = 149597870.691

    @staticmethod
    def get_position(epoch: Epoch) -> Vector3D:
        """calculate the ECI position at a given epoch

        :param epoch: time of calculated position vector
        :type epoch: Epoch
        :return: ECI position in km
        :rtype: Vector3D
        """
        a = Conversions.dms_to_radians(0, 0, 6892)
        b = Conversions.dms_to_radians(0, 0, 72)
        t = Epoch.julian_centuries_past_j2000(epoch.tt)

        ma = radians(357.5256 + 35999.049 * t)

        sma = sin(ma)
        cma = cos(ma)
        c2ma = cos(2 * ma)

        lam = Sun.W_PLUS_W + ma + a * sma + b * 2 * sma * cma
        r = (149.619 - 2.499 * cma - 0.021 * c2ma) * 1e6

        x = r * cos(lam)

        slam = sin(lam)

        y = r * slam * Sun.COS_OBLIQUITY
        z = r * slam * Sun.SIN_OBLIQUITY

        return Vector3D(x, y, z)
