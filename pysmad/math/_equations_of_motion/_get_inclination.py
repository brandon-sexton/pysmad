from math import atan2, sqrt

from pysmad.coordinates import CartesianVector


class GetInclination:
    @staticmethod
    def from_w(w: CartesianVector) -> float:
        r"""calculate the inclination

        .. math::

           i = \arctan{
                \left(
                    \frac{
                        \sqrt{
                            \vec{w}_{x}^2 + \vec{w}_{y}^2
                        }
                    }{
                        \vec{w}_{z}
                    }
                \right)
            }

        :param w: normalized momentum vector :math:`\hat{h}` in :math:`\frac{km^2}{s}`
        :type w: Vector3D
        :return: inclination in :math:`rad` where :math:`0 \leq i < \pi`
        :rtype: float

        .. todo::

           document equation reference from Satellite Orbits
        """
        return atan2(sqrt(w.x * w.x + w.y * w.y), w.z)
