from math import cos, radians, sin, sqrt
from typing import List

from pyxis.math.constants import HOURS_IN_DAY, MINUTES_IN_DAY, MINUTES_IN_HOUR, SECONDS_IN_DAY, SECONDS_IN_HOUR


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


s3: float = sqrt(3)
s5: float = sqrt(5)
s7: float = sqrt(7)
s105: float = s3 * s5 * s7


class LegendrePolynomial:
    def __init__(self, phi: float) -> None:
        self.phi: float = phi
        cp: float = cos(phi)
        sp: float = sin(phi)
        cp2: float = cp * cp
        sp2: float = sp * sp

        self.p: List[List[float]] = [
            [1],
            [s3 * cp, s3 * sp],
            [s5 * (3 * cp2 - 1) * 0.5, s3 * s5 * sp * cp, s3 * s5 * sp * cp],
            [
                s7 * (5 * cp2 * cp - 3 * cp) * 0.5,
                s3 * s7 * (5 * cp2 - 1) * sp * 0.5,
                s105 * cp * sp2,
                s7 * s5 * sp2 * sp,
            ],
            [
                0.375 * (35 * cp2 * cp2 - 30 * cp2 + 3),
                0.75 * s5 * (7 * cp2 * cp - 3 * cp) * sp,
                s105 * (7 * cp2 - 1) * sp2 * 0.5,
                s105 * cp * sp2 * sp,
                3 * sp2 * sp2,
            ],
        ]
