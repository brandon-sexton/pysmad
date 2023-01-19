from math import asin, atan2, cos, pi, sin, sqrt

from openspace.bodies.celestial import Earth
from openspace.coordinates.positions import LLA
from openspace.coordinates.states import GCRF, Hill
from openspace.math.functions import sign
from openspace.math.linalg import Matrix3D, Vector3D
from openspace.time import Epoch


class _PositionConvertGCRF:
    @staticmethod
    def to_itrf(pos: Vector3D, epoch: Epoch) -> Vector3D:
        return Earth.rotation(epoch).multiply_vector(_PositionConvertGCRF.to_tod(pos, epoch))

    @staticmethod
    def to_tod(pos: Vector3D, epoch: Epoch) -> Vector3D:
        return Earth.nutation(epoch).multiply_vector(_PositionConvertGCRF.to_mod(pos, epoch))

    @staticmethod
    def to_mod(pos: Vector3D, epoch: Epoch) -> Vector3D:
        return Earth.precession(epoch).multiply_vector(pos)


class _PositionConvertITRF:
    @staticmethod
    def to_gcrf(pos: Vector3D, epoch: Epoch) -> Vector3D:
        return Earth.precession(epoch).transpose().multiply_vector(_PositionConvertITRF.to_mod(pos, epoch))

    @staticmethod
    def to_tod(pos: Vector3D, epoch: Epoch) -> Vector3D:
        return Earth.rotation(epoch).transpose().multiply_vector(pos)

    @staticmethod
    def to_mod(pos: Vector3D, epoch: Epoch) -> Vector3D:
        return Earth.nutation(epoch).transpose().multiply_vector(_PositionConvertITRF.to_tod(pos, epoch))

    @staticmethod
    def to_lla(pos: Vector3D) -> LLA:
        x: float = pos.x
        y: float = pos.y
        z: float = pos.z

        # Equation 2.77a
        a: float = Earth.RADIUS
        a2: float = a * a
        f: float = Earth.FLATTENING
        b: float = a - f * a
        b2: float = b * b
        e2: float = 1 - b2 / a2
        eps2: float = a2 / b2 - 1.0
        rho: float = sqrt(x * x + y * y)

        # Equation 2.77b
        p: float = abs(z) / eps2
        s: float = rho * rho / (e2 * eps2)
        q: float = p * p - b2 + s

        # Equation 2.77c
        u: float = p / sqrt(q)
        v: float = b2 * u * u / q
        cap_p: float = 27.0 * v * s / q
        cap_q: float = (sqrt(cap_p + 1) + sqrt(cap_p)) ** (2.0 / 3.0)

        # Equation 2.77d
        t: float = (1.0 + cap_q + 1.0 / cap_q) / 6.0
        c: float = sqrt(u * u - 1.0 + 2.0 * t)
        w: float = (c - u) / 2.0

        # Equation 2.77e
        base: float = sqrt(t * t + v) - u * w - t / 2.0 - 0.25
        if base < 0:
            base = 0
        arg: float = w + sqrt(base)
        d: float = sign(z) * sqrt(q) * arg

        # Equation 2.77f
        n: float = a * sqrt(1.0 + eps2 * d * d / b2)
        arg = (eps2 + 1.0) * (d / n)
        lamb: float = asin(arg)

        # Equation 2.77g
        h: float = rho * cos(lamb) + z * sin(lamb) - a2 / n
        phi: float = atan2(y, x)
        if phi < 0:
            phi += pi * 2.0

        return LLA(lamb, phi, h)


class _PositionConvertLLA:
    @staticmethod
    def to_itrf(lla: LLA):
        lat: float = lla.latitude
        longitude: float = lla.longitude
        alt: float = lla.altitude

        f: float = Earth.FLATTENING
        e: float = sqrt(f * (2 - f))
        slat: float = sin(lat)
        clat: float = cos(lat)
        n: float = Earth.RADIUS / sqrt(1 - e * e * slat * slat)

        return Vector3D(
            (n + alt) * clat * cos(longitude), (n + alt) * clat * sin(longitude), (n * (1.0 - e * e) + alt) * slat
        )


class PositionConvert:

    gcrf = _PositionConvertGCRF
    itrf = _PositionConvertITRF
    lla = _PositionConvertLLA


class _StateConvertGCRF:
    @staticmethod
    def to_hill(origin: GCRF, state: GCRF) -> Hill:
        magrtgt: float = origin.position.magnitude()
        magrint: float = state.position.magnitude()
        rot_eci_rsw: Matrix3D = Hill.frame_matrix(origin)
        vtgtrsw: Vector3D = rot_eci_rsw.multiply_vector(origin.velocity)
        rintrsw: Vector3D = rot_eci_rsw.multiply_vector(state.position)
        vintrsw: Vector3D = rot_eci_rsw.multiply_vector(state.velocity)

        sinphiint: float = rintrsw.z / magrint
        phiint: float = asin(sinphiint)
        cosphiint: float = cos(phiint)
        lambdaint: float = atan2(rintrsw.y, rintrsw.x)
        sinlambdaint: float = sin(lambdaint)
        coslambdaint: float = cos(lambdaint)
        lambdadottgt: float = vtgtrsw.y / magrtgt

        rhill: Vector3D = Vector3D(magrint - magrtgt, lambdaint * magrtgt, phiint * magrtgt)

        rot_rsw_sez: Matrix3D = Matrix3D(
            Vector3D(sinphiint * coslambdaint, sinphiint * sinlambdaint, -cosphiint),
            Vector3D(-sinlambdaint, coslambdaint, 0),
            Vector3D(cosphiint * coslambdaint, cosphiint * sinlambdaint, sinphiint),
        )

        vintsez: Vector3D = rot_rsw_sez.multiply_vector(vintrsw)
        phidotint: float = -vintsez.x / magrint
        lambdadotint: float = vintsez.y / (magrint * cosphiint)

        vhill: Vector3D = Vector3D(
            vintsez.z - vtgtrsw.x,
            magrtgt * (lambdadotint - lambdadottgt),
            magrtgt * phidotint,
        )

        return Hill(origin.epoch, rhill, vhill)


class _StateConvertHill:
    @staticmethod
    def to_gcrf(state: Hill, origin: GCRF) -> GCRF:
        """create an inertial state for the calling state

        :param origin: inertial state that acts as the origin for the relative state
        :type origin: GCRFstate
        :return: inertial state of the relative spacecraft
        :rtype: GCRFstate
        """
        magrtgt: float = origin.position.magnitude()
        magrint: float = magrtgt + state.position.x
        rot_eci_rsw: Matrix3D = Hill.frame_matrix(origin)
        vtgtrsw: Vector3D = rot_eci_rsw.multiply_vector(origin.velocity)

        lambdadottgt: float = vtgtrsw.y / magrtgt
        lambdaint: float = state.position.y / magrtgt
        phiint: float = state.position.z / magrtgt
        sinphiint: float = sin(phiint)
        cosphiint: float = cos(phiint)
        sinlambdaint: float = sin(lambdaint)
        coslambdaint: float = cos(lambdaint)

        rot_rsw_sez: Matrix3D = Matrix3D(
            Vector3D(sinphiint * coslambdaint, sinphiint * sinlambdaint, -cosphiint),
            Vector3D(-sinlambdaint, coslambdaint, 0),
            Vector3D(cosphiint * coslambdaint, cosphiint * sinlambdaint, sinphiint),
        )

        rdotint: float = state.velocity.x + vtgtrsw.x
        lambdadotint: float = state.velocity.y / magrtgt + lambdadottgt
        phidotint: float = state.velocity.z / magrtgt
        vintsez: Vector3D = Vector3D(-magrint * phidotint, magrint * lambdadotint * cosphiint, rdotint)
        vintrsw: Vector3D = rot_rsw_sez.transpose().multiply_vector(vintsez)
        vinteci: Vector3D = rot_eci_rsw.transpose().multiply_vector(vintrsw)

        rintrsw: Vector3D = Vector3D(
            cosphiint * magrint * coslambdaint,
            cosphiint * magrint * sinlambdaint,
            sinphiint * magrint,
        )

        rinteci: Vector3D = rot_eci_rsw.transpose().multiply_vector(rintrsw)

        return GCRF(origin.epoch, rinteci, vinteci)


class StateConvert:
    hill = _StateConvertHill
    gcrf = _StateConvertGCRF
