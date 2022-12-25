from typing import List
from math import cos, sin, asin, atan2, radians

from pyxis.math.linalg import Vector3D, Vector6D, Matrix3D
from pyxis.time import Epoch
from pyxis.astro.bodies.celestial import Sun, Earth, Moon
from pyxis.math.functions import Conversions

class HillState:
    def __init__(self, position:Vector3D, velocity:Vector3D) -> None:
        self.position:Vector3D = position.copy()
        self.velocity:Vector3D = velocity.copy()
        self.vector = Vector6D.from_position_and_velocity(self.position, self.velocity)

    @classmethod
    def from_state_vector(cls, state:Vector6D) -> "HillState":
        return cls(Vector3D(state.x, state.y, state.z), Vector3D(state.vx, state.vy, state.vz))

    @classmethod
    def from_gcrf(cls, state: "GCRFstate", origin: "GCRFstate") -> "HillState":
        magrtgt = origin.position.magnitude()
        magrint = state.position.magnitude()
        rot_eci_rsw = HillState.frame_matrix(origin)
        vtgtrsw = rot_eci_rsw.multiply_vector(origin.velocity)
        rintrsw = rot_eci_rsw.multiply_vector(state.position)
        vintrsw = rot_eci_rsw.multiply_vector(state.velocity)

        sinphiint = rintrsw.z / magrint
        phiint = asin(sinphiint)
        cosphiint = cos(phiint)
        lambdaint = atan2(rintrsw.y, rintrsw.x)
        sinlambdaint = sin(lambdaint)
        coslambdaint = cos(lambdaint)
        lambdadottgt = vtgtrsw.y / magrtgt

        rhill = Vector3D(magrint - magrtgt, lambdaint * magrtgt, phiint * magrtgt)

        rot_rsw_sez = Matrix3D(
            Vector3D(sinphiint * coslambdaint, sinphiint * sinlambdaint, -cosphiint),
            Vector3D(-sinlambdaint, coslambdaint, 0),
            Vector3D(cosphiint * coslambdaint, cosphiint * sinlambdaint, sinphiint),
        )

        vintsez = rot_rsw_sez.multiply_vector(vintrsw)
        phidotint = -vintsez.x / magrint
        lambdadotint = vintsez.y / (magrint * cosphiint)

        vhill = Vector3D(
            vintsez.z - vtgtrsw.x,
            magrtgt * (lambdadotint - lambdadottgt),
            magrtgt * phidotint,
        )

        return cls(rhill, vhill)

    @staticmethod
    def frame_matrix(origin:"GCRFstate") -> Matrix3D:
        r = origin.position.normalized()
        c = origin.position.cross(origin.velocity).normalized()
        i = c.cross(r)
        return Matrix3D(r, i, c)

    def copy(self) -> "HillState":
        return HillState(self.position, self.velocity)

    def to_gcrf(self, origin: "GCRFstate") -> "GCRFstate":
        magrtgt = origin.position.magnitude()
        magrint = magrtgt + self.position.x
        rot_eci_rsw = HillState.frame_matrix(origin)
        vtgtrsw = rot_eci_rsw.multiply_vector(origin.velocity)

        lambdadottgt = vtgtrsw.y / magrtgt
        lambdaint = self.position.y / magrtgt
        phiint = self.position.z / magrtgt
        sinphiint = sin(phiint)
        cosphiint = cos(phiint)
        sinlambdaint = sin(lambdaint)
        coslambdaint = cos(lambdaint)

        rot_rsw_sez = Matrix3D(
            Vector3D(sinphiint * coslambdaint, sinphiint * sinlambdaint, -cosphiint),
            Vector3D(-sinlambdaint, coslambdaint, 0),
            Vector3D(cosphiint * coslambdaint, cosphiint * sinlambdaint, sinphiint),
        )

        rdotint = self.velocity.x + vtgtrsw.x
        lambdadotint = self.velocity.y / magrtgt + lambdadottgt
        phidotint = self.velocity.z / magrtgt
        vintsez = Vector3D(
            -magrint * phidotint, magrint * lambdadotint * cosphiint, rdotint
        )
        vintrsw = rot_rsw_sez.transpose().multiply_vector(vintsez)
        vinteci = rot_eci_rsw.transpose().multiply_vector(vintrsw)

        rintrsw = Vector3D(
            cosphiint * magrint * coslambdaint,
            cosphiint * magrint * sinlambdaint,
            sinphiint * magrint,
        )

        rinteci = rot_eci_rsw.transpose().multiply_vector(rintrsw)

        return GCRFstate(origin.epoch, rinteci, vinteci)

class GCRFstate:
    def __init__(self, epoch:Epoch, position:Vector3D, velocity:Vector3D) -> None:
        self.epoch:Epoch = epoch.copy()
        self.position:Vector3D = position.copy()
        self.velocity:Vector3D = velocity.copy()

    @classmethod
    def from_hill(cls, origin:"GCRFstate", state:HillState) -> "GCRFstate":
        return state.to_gcrf(origin)

    def copy(self) -> "GCRFstate":
        return GCRFstate(self.epoch, self.position, self.velocity)

    def vector_list(self) -> List[Vector3D]:
        return [self.position.copy(), self.velocity.copy()]

    def acceleration_from_earth(self) -> Vector3D:
        r_mag:float = self.position.magnitude()
        return self.position.scaled(-Earth.MU/(r_mag*r_mag*r_mag))

    def acceleration_from_moon(self) -> Vector3D:
        s:Vector3D = Moon.get_position(self.epoch)
        r:Vector3D = s.minus(self.position)
        r_mag:float = r.magnitude()
        s_mag:float = s.magnitude()
        vec_1:Vector3D = r.scaled(1/(r_mag*r_mag*r_mag))
        vec_2:Vector3D = s.scaled(1/(s_mag*s_mag*s_mag))
        return vec_1.minus(vec_2).scaled(Moon.MU)

    def acceleration_from_sun(self) -> Vector3D:
        s:Vector3D = Sun.get_position(self.epoch)
        r:Vector3D = s.minus(self.position)
        r_mag:float = r.magnitude()
        s_mag:float = s.magnitude()
        vec_1:Vector3D = r.scaled(1/(r_mag*r_mag*r_mag))
        vec_2:Vector3D = s.scaled(1/(s_mag*s_mag*s_mag))
        return vec_1.minus(vec_2).scaled(Sun.MU)

    def acceleration_from_srp(self) -> Vector3D:
        sun_vec:Vector3D = self.sun_vector().normalized()
        return sun_vec.scaled(-Sun.P*3.6e-5)

    def derivative(self) -> List[Vector3D]:
        net_0 = Vector3D(0, 0, 0)
        net_1 = net_0.plus(self.acceleration_from_moon())
        net_2 = net_1.plus(self.acceleration_from_sun())
        net_3 = net_2.plus(self.acceleration_from_srp())
        net_a = net_3.plus(self.acceleration_from_earth())
        return [self.velocity.copy(), net_a]

    def sun_vector(self) -> Vector3D:
        return Sun.get_position(self.epoch).minus(self.position)

    def moon_vector(self) -> Vector3D:
        return Moon.get_position(self.epoch).minus(self.position)

    def itrf_position(self) -> Vector3D:

        mod = Precession.matrix(self.epoch).multiply_vector(self.position)
        tod = Nutation.matrix(self.epoch).multiply_vector(mod)
        return Rotation.matrix(self.epoch).multiply_vector(tod)

class Rotation:

    @staticmethod
    def matrix(epoch:Epoch) -> Matrix3D:
        d = epoch.julian_value() - Epoch.J2000_JULIAN_DATE
        arg1 = radians(125.0 - .05295*d)
        arg2 = radians(200.9 + 1.97129*d)
        a = radians(-.0048)
        b = radians(.0004)
        dpsi = a*sin(arg1) - b*sin(arg2)
        eps = Earth.obliquity_of_ecliptic_at_epoch(epoch)
        gmst = epoch.greenwich_hour_angle()
        gast = dpsi*cos(eps) + gmst
        return Vector3D.rotation_matrix(Vector3D(0, 0, 1), -gast)

class Precession:

    @staticmethod
    def matrix(epoch:Epoch) -> Matrix3D:
        t = epoch.julian_centuries_past_j2000()
        a = Conversions.dms_to_radians(0, 0, 2306.2181)
        b = Conversions.dms_to_radians(0, 0, .30188)
        c = Conversions.dms_to_radians(0, 0, .017998)
        x = a*t + b*t*t + c*t*t*t

        a = Conversions.dms_to_radians(0, 0, 2004.3109)
        b = Conversions.dms_to_radians(0, 0, .42665)
        c = Conversions.dms_to_radians(0, 0, .041833)
        y = a*t - b*t*t - c*t*t*t

        a = Conversions.dms_to_radians(0, 0, .7928)
        b = Conversions.dms_to_radians(0, 0, .000205)
        z = x + a*t*t + b*t*t*t

        sz = sin(z)
        sy = sin(y)
        sx = sin(x)
        cz = cos(z)
        cy = cos(y)
        cx = cos(x)

        p11 = -sz*sx + cz*cy*cx
        p21 = cz*sx + sz*cy*cx
        p31 = sy*cx

        p12 = -sz*cx - cz*cy*sx
        p22 = cz*cx - sz*cy*sx
        p32 = -sy*sx

        p13 = -cz*sy
        p23 = -sz*sy
        p33 = cy

        return Matrix3D(Vector3D(p11, p12, p13), Vector3D(p21, p22, p23), Vector3D(p31, p32, p33))

class Nutation:

    @staticmethod
    def matrix(epoch:Epoch) -> Matrix3D:
        d = epoch.julian_value() - Epoch.J2000_JULIAN_DATE
        arg1 = radians(125.0 - .05295*d)
        arg2 = radians(200.9 + 1.97129*d)
        a = radians(-.0048)
        b = radians(.0004)
        dpsi = a*sin(arg1) - b*sin(arg2)
        a = radians(.0026)
        b = radians(.0002)
        deps = a*cos(arg1) + b*cos(arg2)
        eps = Earth.obliquity_of_ecliptic_at_epoch(epoch)

        ce = cos(eps)
        se = sin(eps)

        return Matrix3D(Vector3D(1.0, -dpsi*ce, -dpsi*se), Vector3D(dpsi*ce, 1.0, -deps), Vector3D(dpsi*se, deps, 1.0))

class ITRFstate:
    def __init__(self, epoch:Epoch, position:Vector3D, velocity:Vector3D) -> None:
        self.epoch:Epoch = epoch.copy()
        self.position:Vector3D = position.copy()
        self.velocity:Vector3D = velocity.copy()

    def gcrf_position(self) -> Vector3D:
        tod:Vector3D = Rotation.matrix(self.epoch).transpose().multiply_vector(self.position)
        mod:Vector3D = Nutation.matrix(self.epoch).transpose().multiply_vector(tod)
        return Precession.matrix(self.epoch).transpose().multiply_vector(mod)
