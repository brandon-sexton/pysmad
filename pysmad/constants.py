from math import pi

#: number of seconds in one solar day in :math:`\frac{sec}{day}`
DAYS_TO_SECONDS: float = 86400

#: seconds to days conversion factor
SECONDS_TO_DAYS: float = 1 / DAYS_TO_SECONDS

#: number of hours in one solar day in :math:`\frac{hr}{day}`
HOURS_IN_DAY: float = 24

#: number of minutes equal to one solar day in :math:`\frac{min}{day}`
MINUTES_IN_DAY: float = 1440

#: number of minutes equal to one hour in :math:`\frac{min}{hr}`
MINUTES_IN_HOUR: float = 60

#: number of seconds equal to one hour in :math:`\frac{sec}{hr}`
SECONDS_IN_HOUR: float = 3600

#: number of seconds equal to one minute in :math:`\frac{sec}{min}`
SECONDS_IN_MINUTE: float = 60

#: number of degrees equal to one hour in :math:`\frac{\deg}{hr}`
DEGREES_IN_HOUR: float = 15

#: gravity at sea level in :math:`\frac{km}{sec^2}`
SEA_LEVEL_G: float = 0.00981

#: number of base units in a kilo in :math:`\frac{(base)}{kilo(base)}`
KILO_TO_BASE: float = 1000

#: milli to base conversion factor
MILLI_TO_BASE: float = 1e-3

#: number of seconds for Earth to complete one rotation in :math:`sec` (found on page 31 of Vallado 4th Edition)
SECONDS_IN_SIDEREAL_DAY: float = 86164.090518

#: julian value acting as the MJD start
MJD_ZERO_JULIAN_DATE = 2400000.5

#: number of days in a julian century
DAYS_IN_JULIAN_CENTURY = 36525

#: julian value for the j2000 epoch
J2000_JULIAN_DATE = 2451545.0

#: degrees to arc seconds conversion factor
DEGREES_TO_ARC_SECONDS: float = 3600

#: arc seconds to degrees conversion factor
ARC_SECONDS_TO_DEGREES: float = 1 / DEGREES_TO_ARC_SECONDS

#: arc seconds to radians conversion factor
ARC_SECONDS_TO_RADIANS: float = pi / 648000

#: TAI to TT conversion factor
TAI_TO_TT: float = 32.184 * SECONDS_TO_DAYS

#: julian century to days conversion factor
JULIAN_CENTURY_TO_DAYS: float = 36525

#: days to julian century conversion factor
DAYS_TO_JULIAN_CENTURY: float = 1 / JULIAN_CENTURY_TO_DAYS
