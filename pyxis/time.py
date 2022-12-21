from math import floor, radians

from pyxis.math.functions import Conversions
from pyxis.math.constants import SECONDS_IN_DAY

class Epoch:
    
    """Class used to represent time.  Default inputs are referenced in Terrestrial Dynamic Time (TDT)"""

    MJD_ZERO = 2400000.5
    JULIAN_CENTURY = 36525
    J2000_JULIAN_DATE = 2451545
    UTC_TDT_OFFSET = 69.184/SECONDS_IN_DAY

    def __init__(self, value:float) -> None:
        self.value = value

    def copy(self) -> "Epoch":
        return Epoch(self.value)

    @classmethod
    def from_gregorian(cls, year:int, month:int, day:int, hour:int, minute:int, sec:float) -> "Epoch":

        y = year
        m = month
        d = day

        if m <= 2:
            y-=1
            m+=12

        b = floor(y/400) - floor(y/100) + floor(y/4)
        mjd = 365*y - 679004 + b + floor(30.6001*(m+1)) + d

        return cls(mjd + Conversions.hms_to_decimal_day(hour, minute, sec))

    def julian_value(self) -> float:
        return self.value + self.MJD_ZERO

    def julian_centuries_past_j2000(self) -> float:
        return (self.julian_value() - self.J2000_JULIAN_DATE)/self.JULIAN_CENTURY

    def plus_days(self, t:float) -> "Epoch":
        return Epoch(self.value + t)

    def greenwich_hour_angle(self) -> float:

        #solve for julian centuries since j2000 using equation 2.7
        utc = Epoch(self.value - Epoch.UTC_TDT_OFFSET)
        dec_day = utc.value % 1
        j0 = utc.julian_value() - dec_day
        j = (j0 - Epoch.J2000_JULIAN_DATE)/Epoch.JULIAN_CENTURY

        #solve for theta0 using equation 2.6
        theta0 = 100.4606184 + 36000.77004*j + .000387933*j*j
        
        #solve for gmst using equation 2.8
        total_deg = theta0 + 360.98564724*dec_day
        return radians(total_deg % 360)