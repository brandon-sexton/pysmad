from math import radians

from pyxis.math.constants import HOURS_IN_DAY, MINUTES_IN_DAY, MINUTES_IN_HOUR, SECONDS_IN_DAY, SECONDS_IN_HOUR


class Conversions:
    @staticmethod
    def hms_to_decimal_day(hr: float, m: float, s: float) -> float:
        return hr / HOURS_IN_DAY + m / MINUTES_IN_DAY + s / SECONDS_IN_DAY

    @staticmethod
    def dms_to_radians(d: float, m: float, s: float) -> float:
        return radians(d + m / MINUTES_IN_HOUR + s / SECONDS_IN_HOUR)
