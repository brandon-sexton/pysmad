from math import radians, sin, cos

from pyxis.math.functions import Conversions
from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch

class Earth:

    """Class used to store Earth properties base on the WGS84 model"""

    MU:float = 398600.4418
    RADIUS:float = 6378.137
    FLATTENING:float = 1/298.257223563
    OBLIQUITY_OF_ECLIPTIC:float = radians(23.43929111)

    @staticmethod
    def obliquity_of_ecliptic_at_epoch(epoch:Epoch) -> float:
        #Equation 5.39
        t = epoch.julian_centuries_past_j2000()

        a = Conversions.dms_to_radians(0, 0, 46.815)
        b = Conversions.dms_to_radians(0, 0, .00059)
        c = Conversions.dms_to_radians(0, 0, .001813)

        #Equation 5.42
        return Earth.OBLIQUITY_OF_ECLIPTIC - a*t - b*t*t + c*t*t*t

class Sun:

    W_PLUS_W = radians(282.94)
    COS_OBLIQUITY = cos(Earth.OBLIQUITY_OF_ECLIPTIC)
    SIN_OBLIQUITY = sin(Earth.OBLIQUITY_OF_ECLIPTIC)
    MU = 1.327124400419e11
    RADIUS = 696.34e3
    P = 4.56e-6
    AU = 149597870.691

    def get_position(epoch: Epoch) -> Vector3D:
        a = Conversions.dms_to_radians(0, 0, 6892)
        b = Conversions.dms_to_radians(0, 0, 72)
        t = epoch.julian_centuries_past_j2000()

        ma = radians(357.5256 + 35999.049*t)

        sma = sin(ma)
        cma = cos(ma)
        c2ma = cos(2*ma)

        lam = Sun.W_PLUS_W + ma + a*sma + b*2*sma*cma
        r = (149.619 - 2.499*cma - .021*c2ma)*1e6

        x = r*cos(lam)

        slam = sin(lam)

        y = r*slam*Sun.COS_OBLIQUITY
        z = r*slam*Sun.SIN_OBLIQUITY

        return Vector3D(x, y, z)

class Moon:

    MU = 4902.800305555
    RADIUS = 1737.4000

    def get_position(epoch: Epoch) -> Vector3D:

        #Equation 3.47
        t = epoch.julian_centuries_past_j2000()
        l0 = radians(218.31617 + 481267.88088*t - 1.3972*t)
        l = radians(134.96292 + 477198.86753*t)
        lp = radians(357.52543 + 35999.04944*t)
        f = radians(93.27283 + 483202.01873*t)
        d = radians(297.85027 + 445267.11135*t)

        #Auxiliary variables to store the angles defined in seconds in equation 3.48
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

        #Equation 3.48
        lam = l0+a0*sin(l) + a1*sin(2*l) \
            -a2*sin(l-2.0*d) + a3*sin(2.0*d) \
            -a4*sin(lp) - a5*sin(2.0*f) \
            -a6*sin(2.0*l-2.0*d) - a7*sin(l+lp-2.0*d) \
            +a8*sin(l+2.0*d) - a9*sin(lp-2.0*d) \
            +a10*sin(l-lp) - a11*sin(d) \
            -a12*sin(l+lp) - a13*sin(2.0*f-2.0*d)

        #Redefined variables for angles in equation 3.49
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

        #Equation 3.49
        beta = a0*sin(f+lam-l0+a1*sin(2.0*f+a2*sin(lp))) \
            -a3*sin(f-2.0*d) + a4*sin(l+f-2.0*d) \
            -a5*sin(-l+f-2.0*d)-a6*sin(-2.0*l+f) \
            -a7*sin(lp+f-2.0*d) + a8*sin(-l+f) \
            +a9*sin(-lp+f-2.0*d)

        #Equation 3.50
        r = (385000.0-20905.0*cos(l)-3699.0*cos(2.0*d-l) \
            -2956.0*cos(2.0*d)-570.0*cos(2.0*l)+246.0*cos(2.0*l-2.0*d) \
            -205.0*cos(lp-2.0*d) - 171.0*cos(l+2.0*d) \
            -152.0*cos(l+lp-2.0*d))

        #Equation 3.51
        x = r*cos(lam)*cos(beta)
        y = r*sin(lam)*cos(beta)
        z = r*sin(beta)

        eps = Earth.OBLIQUITY_OF_ECLIPTIC

        return Vector3D(x, y, z).rotation_about_axis(Vector3D(1, 0, 0), eps)
