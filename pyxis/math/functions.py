from math import radians

from pyxis.math.constants import *

class Conversions:

    def hms_to_decimal_day(hr:float, m:float, s:float) -> float:
        return hr/HOURS_IN_DAY + m/MINUTES_IN_DAY + s/SECONDS_IN_DAY

    def dms_to_radians(d:float, m:float, s:float) -> float:
        return radians(d + m/MINUTES_IN_HOUR + s/SECONDS_IN_HOUR)
