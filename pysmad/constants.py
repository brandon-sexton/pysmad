from math import cos, pi, radians, sin

#: number of seconds in one solar day in :math:`\frac{sec}{day}`
DAYS_TO_SECONDS: float = 86400

#: seconds to days conversion factor
SECONDS_TO_DAYS: float = 1 / DAYS_TO_SECONDS

DAYS_TO_HOURS: float = 24

HOURS_TO_DAYS: float = 1 / DAYS_TO_HOURS
#: number of minutes equal to one solar day in :math:`\frac{min}{day}`
DAYS_TO_MINUTES: float = 1440

MINUTES_TO_DAYS: float = 1 / DAYS_TO_MINUTES

#: number of minutes equal to one hour in :math:`\frac{min}{hr}`
HOURS_TO_MINUTES: float = 60

MINUTES_TO_HOURS: float = 1 / HOURS_TO_MINUTES

#: number of seconds equal to one hour in :math:`\frac{sec}{hr}`
HOURS_TO_SECONDS: float = 3600

SECONDS_TO_HOURS: float = 1 / HOURS_TO_SECONDS

#: number of seconds equal to one minute in :math:`\frac{sec}{min}`
MINUTES_TO_SECONDS: float = 60

SECONDS_TO_MINUTES: float = 1 / MINUTES_TO_SECONDS

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

#: :math:`\mu` value for the moon in :math:`\frac{km^3}{s^2}`
MOON_MU = 4902.800305555

#: distance from center of moon to surface in :math:`km`
MOON_RADIUS = 1737.4

#: inclination of ecliptic relative to earth equator in radians
OBLIQUITY_OF_ECLIPTIC: float = radians(23.43929111)

#: G*M given in :math:`\frac{km^3}{s^2}`
EARTH_MU: float = 398600.4418

#: distance from earth center to surface at the equator in :math:`km`
EARTH_RADIUS: float = 6378.137

#: value defining the ellipsoid of an oblate earth
EARTH_FLATTENING: float = 1 / 298.2572235

#: cosine of obliquity of ecliptic
COS_OBLIQUITY = cos(OBLIQUITY_OF_ECLIPTIC)

#: sine of obliquity of ecliptic
SIN_OBLIQUITY = sin(OBLIQUITY_OF_ECLIPTIC)

#: Distance to earth in km
AU_TO_KM = 149597870.691

#: RAAN + argument of periapsis in radians
SUN_TRUE_LONGITUDE = radians(282.94)

#: G*M in km^3/s^
SUN_MU = 1.327124400419e11

#: Estimate of srp
SUN_P = 4.56e-6
