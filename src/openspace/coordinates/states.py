from math import cos, sin, sqrt, tan
from typing import List

from openspace.bodies.celestial import Earth, Moon, Sun
from openspace.coordinates.positions import SphericalPosition
from openspace.coordinates.transforms import PositionConvert
from openspace.math.constants import BASE_IN_KILO
from openspace.math.functions import LegendrePolynomial
from openspace.math.linalg import Matrix3D, Vector3D, Vector6D
from openspace.time import Epoch


class State:
    def __init__(self, epoch: Epoch, r: Vector3D, v: Vector3D) -> None:
        """class used to perform operations for time-dependent states

        :param epoch: time for which the position and velocity are valid
        :type epoch: Epoch
        :param r: position of the state
        :type r: Vector3D
        :param v: velocity of the state
        :type v: Vector3D
        """
        #: time for which the position and velocity are valid
        self.epoch: Epoch = epoch.copy()

        #: position of the state
        self.position: Vector3D = r.copy()

        #: velocity of the state
        self.velocity: Vector3D = v.copy()

        #: state vector whose elements are equal to that of the position and velocity unpacked
        self.vector = Vector6D.from_position_and_velocity(self.position, self.velocity)


class Hill(State):
    def __init__(self, epoch: Epoch, r: Vector3D, v: Vector3D) -> None:
        """class used to perform operations and modeling in the Hill Frame

        :param epoch: time for which the position and velocity are valid
        :type epoch: Epoch
        :param r: position of the state
        :type r: Vector3D
        :param v: velocity of the state
        :type v: Vector3D
        """
        super().__init__(epoch, r, v)

    @staticmethod
    def frame_matrix(origin: "GCRF") -> Matrix3D:
        """create a radial, in-track, cross-track axes matrix

        :param origin: inertial state that acts as the origin for the RIC frame
        :type origin: GCRF
        :return: matrix with rows of radial, in-track, and cross-track
        :rtype: Matrix3D
        """
        r: Vector3D = origin.position.normalized()
        c: Vector3D = origin.position.cross(origin.velocity).normalized()
        i: Vector3D = c.cross(r)
        return Matrix3D(r, i, c)


class GCRF(State):
    def __init__(self, epoch: Epoch, r: Vector3D, v: Vector3D) -> None:
        """class used to perform operations and modeling in the Geocentric Celestial Reference Frame

        :param epoch: time for which the position and velocity are valid
        :type epoch: Epoch
        :param r: position of the state
        :type r: Vector3D
        :param v: velocity of the state
        :type v: Vector3D
        """
        super().__init__(epoch, r, v)

        #: acceleration due to thrust
        self.thrust: Vector3D = Vector3D(0, 0, 0)

        #: scalar used for srp acceleration calculations
        self.srp_scalar: float = 0

    def copy(self) -> "GCRF":
        """create a replica of the calling state

        :return: state with attributes equal to the calling state
        :rtype: GCRF
        """
        return GCRF(self.epoch, self.position, self.velocity)

    def vector_list(self) -> List[Vector3D]:
        """create a list with elements of 0 == position and 1 == velocity

        :return: list of position and velocity
        :rtype: List[Vector3D]
        """
        return [self.position.copy(), self.velocity.copy()]

    def acceleration_from_gravity(self) -> Vector3D:
        """calculates the gravity due to a nonspherical earth

        :return: vector representing the acceleration due to gravity
        :rtype: Vector3D
        """
        ecef: Vector3D = PositionConvert.gcrf.to_itrf(self.position, self.epoch)
        sphr_pos: SphericalPosition = SphericalPosition.from_cartesian(ecef)
        p: List[List[float]] = LegendrePolynomial(sphr_pos.declination).p

        m: int = 0
        n: int = 2

        partial_r: float = 0
        partial_phi: float = 0
        partial_lamb: float = 0
        recip_r: float = 1 / self.position.magnitude()
        mu_over_r: float = Earth.MU * recip_r
        r_over_r: float = Earth.RADIUS * recip_r
        r_exponent: float = 0
        clam: float = 0
        slam: float = 0
        recip_root: float = 1 / sqrt(ecef.x * ecef.x + ecef.y * ecef.y)
        rz_over_root: float = ecef.z * recip_r * recip_r * recip_root
        while n < Earth.DEGREE_AND_ORDER:
            m = 0
            r_exponent = r_over_r**n
            while m <= n:
                clam = cos(m * sphr_pos.right_ascension)
                slam = sin(m * sphr_pos.right_ascension)
                partial_r += r_exponent * (n + 1) * p[n][m] * (Earth.C[n][m] * clam + Earth.S[n][m] * slam)
                partial_phi += (
                    r_exponent
                    * (p[n][m + 1] - m * tan(sphr_pos.declination) * p[n][m])
                    * (Earth.C[n][m] * clam + Earth.S[n][m] * slam)
                )
                partial_lamb += r_exponent * m * p[n][m] * (Earth.S[n][m] * clam - Earth.C[n][m] * slam)

                m += 1

            n += 1

        partial_r *= -recip_r * mu_over_r
        partial_phi *= mu_over_r
        partial_lamb *= mu_over_r

        return PositionConvert.itrf.to_gcrf(
            Vector3D(
                (recip_r * partial_r - rz_over_root * partial_phi) * ecef.x
                - (recip_root * recip_root * partial_lamb) * ecef.y,
                (recip_r * partial_r - rz_over_root * partial_phi) * ecef.y
                + (recip_root * recip_root * partial_lamb) * ecef.x,
                recip_r * partial_r * ecef.z + (1 / recip_root) * recip_r * recip_r * partial_phi,
            ),
            self.epoch,
        )

    def acceleration_from_earth(self) -> Vector3D:
        """calculate the acceleration on the state due to earth's gravity

        :return: vector representing the acceleration from earth
        :rtype: Vector3D
        """
        r_mag: float = self.position.magnitude()

        return self.position.scaled(-Earth.MU / (r_mag * r_mag * r_mag))

    def acceleration_from_moon(self) -> Vector3D:
        """calculate the acceleration on the state due to the moon

        :return: vector representing the acceleration from the moon
        :rtype: Vector3D
        """
        s: Vector3D = Moon.get_position(self.epoch)
        r: Vector3D = s.minus(self.position)
        r_mag: float = r.magnitude()
        s_mag: float = s.magnitude()
        vec_1: Vector3D = r.scaled(1 / (r_mag * r_mag * r_mag))
        vec_2: Vector3D = s.scaled(1 / (s_mag * s_mag * s_mag))
        return vec_1.minus(vec_2).scaled(Moon.MU)

    def acceleration_from_sun(self) -> Vector3D:
        """calculate the acceleration on the state due to the sun

        :return: vector representing the acceleration from the sun
        :rtype: Vector3D
        """
        s: Vector3D = Sun.get_position(self.epoch)
        r: Vector3D = s.minus(self.position)
        r_mag: float = r.magnitude()
        s_mag: float = s.magnitude()
        vec_1: Vector3D = r.scaled(1 / (r_mag * r_mag * r_mag))
        vec_2: Vector3D = s.scaled(1 / (s_mag * s_mag * s_mag))
        return vec_1.minus(vec_2).scaled(Sun.MU)

    def acceleration_from_srp(self) -> Vector3D:
        """calculate the acceleration on the state from solar radiation pressure

        :return: vector representing the acceleration from srp
        :rtype: Vector3D
        """
        sun_vec: Vector3D = self.sun_vector().normalized()
        s_mag: float = sun_vec.magnitude()
        return sun_vec.scaled(-Sun.P * self.srp_scalar / (s_mag * s_mag * BASE_IN_KILO))

    def acceleration_from_thrust(self) -> Vector3D:
        """retrieve the stored acceleration to be applied from thrusters

        :return: the current acceleration vector in the GCRF frame
        :rtype: Vector3D
        """
        return self.thrust.copy()

    def derivative(self) -> List[Vector3D]:
        """create a list with elements 0 == velocity and 1 == acceleration

        :return: list of velocity and acceleration
        :rtype: List[Vector3D]
        """
        net_0: Vector3D = self.acceleration_from_thrust()
        net_1: Vector3D = net_0.plus(self.acceleration_from_moon())
        net_2: Vector3D = net_1.plus(self.acceleration_from_sun())
        net_3: Vector3D = net_2.plus(self.acceleration_from_srp())
        net_4: Vector3D = net_3.plus(self.acceleration_from_gravity())
        net_a: Vector3D = net_4.plus(self.acceleration_from_earth())
        return [self.velocity.copy(), net_a]

    def sun_vector(self) -> Vector3D:
        """create a vector pointing from the calling state to the sun

        :return: vector originating at the calling state and terminating at the sun
        :rtype: Vector3D
        """
        return Sun.get_position(self.epoch).minus(self.position)

    def moon_vector(self) -> Vector3D:
        """create a vector pointing from the calling state to the moon

        :return: vector originating at the calling state and terminating at the moon
        :rtype: Vector3D
        """
        return Moon.get_position(self.epoch).minus(self.position)


class IJK(State):
    def __init__(self, epoch: Epoch, r: Vector3D, v: Vector3D) -> None:
        """class used to perform operations and modeling in the Geocentric Equatorial Coordinate System

        :param epoch: time for which the position and velocity are valid
        :type epoch: Epoch
        :param r: position of the state
        :type r: Vector3D
        :param v: velocity of the state
        :type v: Vector3D
        """
        super().__init__(epoch, r, v)
