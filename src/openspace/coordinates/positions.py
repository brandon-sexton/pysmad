from math import atan2, cos, pi, sin, sqrt

from openspace.math.linalg import Vector3D


class SphericalPosition:
    def __init__(self, r: float, ra: float, dec: float) -> None:
        """class used to perform spherical transformations

        :param r: magnitude of the vector
        :type r: float
        :param ra: right ascension of the vector (radians)
        :type ra: float
        :param dec: declination of the vector (radians)
        :type dec: float
        """
        #: magnitude of the vector
        self.radius: float = r

        #: right ascension of the vector in radians
        self.right_ascension: float = ra

        #: declination of the vector in radians
        self.declination: float = dec

    @classmethod
    def from_cartesian(cls, pos: Vector3D) -> "SphericalPosition":
        """create a spherical vector using cartesian components

        :param pos: cartesian vector
        :type pos: Vector3D
        :return: position represented with spherical components
        :rtype: SphericalPosition
        """
        ra: float = atan2(pos.y, pos.x)
        if ra < 0:
            ra += 2 * pi
        dec: float = atan2(pos.z, sqrt(pos.x * pos.x + pos.y * pos.y))
        return cls(pos.magnitude(), ra, dec)

    def to_cartesian(self) -> Vector3D:
        """calculate the vector as represented by x, y, and z

        :return: vector of equal magnitude in direction but in cartesian coordinates
        :rtype: Vector3D
        """
        cd: float = cos(self.declination)
        return Vector3D(cd * cos(self.right_ascension), cd * sin(self.right_ascension), sin(self.declination)).scaled(
            self.radius
        )


class LLA:
    def __init__(self, lat: float, longit: float, alt: float) -> None:
        """used to perform operations for a state in an oblate earth frame

        :param lat: geodetic latitude in radians
        :type lat: float
        :param long: geodetic longitude in radians
        :type long: float
        :param alt: altitude above the surface in km
        :type alt: float
        """
        #: geodetic latitude in radians
        self.latitude: float = lat

        #: geodetic longitude in radians
        self.longitude: float = longit

        #: altitude above the surface in km
        self.altitude: float = alt

    def copy(self) -> "LLA":
        """creates a duplicate of the calling state

        :return: state with properties that match that of the calling state
        :rtype: LLA
        """
        return LLA(self.latitude, self.longitude, self.altitude)
