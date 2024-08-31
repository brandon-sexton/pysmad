from math import atan2, pi

from pysmad.coordinates import CartesianVector


class RAAN:
    r"""static class used to solve right ascension of ascending node (RAAN)

    .. note::

        * This class is intendend to be used as the alias found in :ref:`EquationsOfMotion <equations_of_motion>`.
        * RAAN is the angle between the vernal equinox and the point where the orbit crosses the equatorial plane from
        south to north and is often represented as :math:`\Omega`
    """

    @staticmethod
    def from_w(w: CartesianVector) -> float:
        r"""calculate the right ascension of the ascending node

        .. math::

           \Omega = \arctan{\left(-\frac{\vec{w}_{x}}{\vec{w}_{y}}\right)}

        :param w: normalized momentum vector
        """
        raan: float = atan2(w.x, -w.y)
        if raan < 0:
            raan += 2 * pi
        return raan
