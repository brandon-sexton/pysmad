from math import cos, sin

from pysmad.coordinates._cartesian_vector import CartesianVector
from pysmad.coordinates._spherical_vector import SphericalVector


class GetCartesianCoordinates:
    @staticmethod
    def from_spherical(sphr: SphericalVector) -> CartesianVector:
        c_dec = cos(sphr.declination)
        x = sphr.radius * c_dec * cos(sphr.right_ascension)
        y = sphr.radius * c_dec * sin(sphr.right_ascension)
        z = sphr.radius * sin(sphr.declination)
        return CartesianVector(x, y, z)
