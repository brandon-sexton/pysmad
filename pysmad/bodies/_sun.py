from math import cos, radians, sin

from pysmad.constants import ARC_SECONDS_TO_RADIANS, COS_OBLIQUITY, SIN_OBLIQUITY, SUN_TRUE_LONGITUDE
from pysmad.coordinates import CartesianVector
from pysmad.time import Epoch


class Sun:
    """class used to store properties of the sun for a force model"""

    @staticmethod
    def get_position(epoch: Epoch) -> CartesianVector:
        """calculate the ECI position in :math:`km` at a given epoch

        :param epoch: time of calculated position vector
        """
        a: float = 6892.0 * ARC_SECONDS_TO_RADIANS
        b: float = 72.0 * ARC_SECONDS_TO_RADIANS
        t = Epoch.julian_centuries_past_j2000(epoch.tt)

        ma = radians(357.5256 + 35999.049 * t)

        sma = sin(ma)
        cma = cos(ma)
        c2ma = cos(2 * ma)

        lam = SUN_TRUE_LONGITUDE + ma + a * sma + b * 2 * sma * cma
        r = (149.619 - 2.499 * cma - 0.021 * c2ma) * 1e6

        x = r * cos(lam)

        slam = sin(lam)

        y = r * slam * COS_OBLIQUITY
        z = r * slam * SIN_OBLIQUITY

        return CartesianVector(x, y, z)
