from math import atan2, pi

from pysmad.coordinates import CartesianVector


class GetArgumentOfLatitude:
    """static class used to solve argument of latitude

    .. note::

       argument of latitude will commonly be referenced as :math:`u` in documentation
    """

    @staticmethod
    def from_r_w(r: CartesianVector, w: CartesianVector) -> float:
        r"""calculate the argument of latitude

        :param r: position vector in :math:`km`
        :type r: Vector3D
        :param w: normalized areal velocity vector in :math:`\frac{km^2}{s}`
        :type w: Vector3D
        :return: argument of latitude in :math:`rads`
        :rtype: float

        .. todo::

           find equation reference
        """
        u: float = atan2(r.z, -r.x * w.y + r.y * w.x)
        if u < 0:
            u += 2 * pi
        return u
