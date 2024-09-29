from math import atan, atan2, sqrt

from pysmad.coordinates._cartesian_vector import CartesianVector
from pysmad.coordinates._spherical_vector import SphericalVector


class GetSphericalCoordinates:
    @staticmethod
    def from_cartesian(vec: CartesianVector) -> SphericalVector:
        """calculates the spherical representation of the vector

        :param vec: vector to convert
        :type vec: Vector3D
        :return: spherical representation of the vector
        :rtype: SphericalVector
        """

        r = vec.magnitude
        dec = atan(vec.z / sqrt(vec.x**2 + vec.y**2))
        ra = atan2(vec.y, vec.x)

        return SphericalVector(ra, dec, r)
