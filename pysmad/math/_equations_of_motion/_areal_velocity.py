from math import cos, sqrt

from pysmad.coordinates import CartesianVector


class ArealVelocity:
    r"""class used to calculate areal velocities of an orbit

    .. note::

        * This class is intendend to be used as the alias found in :ref:`EquationsOfMotion <equations_of_motion>`.
        * The term areal velocity is used synonymously for the momentum of an orbit and will commonly be referenced
          as :math:`h` in documentation.

    """

    @staticmethod
    def from_r_v_phi(r: float, v: float, phi: float) -> float:
        r"""calculate the areal velocity using equation 1-16 in :ref:`vallado`

        .. math::

           h = rv\cos{(\phi_{fpa})}

        :param r: magnitude of the position vector
        :param v: magnitude of the velocity vector
        :param phi: flight path angle :math:`\frac{\pi}{2} - \measuredangle\vec{r}\vec{v}`
        """
        return r * v * cos(phi)

    @staticmethod
    def from_mu_p(mu: float, p: float) -> float:
        r"""calculate the areal velocity using equation 1-19 in :ref:`vallado`

        .. math::

           h = \sqrt{{\mu}p}

        :param mu: gravitational constant time mass of central body
        :param p: semi-parameter
        """
        return sqrt(mu * p)

    @staticmethod
    def from_r_v(r: CartesianVector, v: CartesianVector) -> CartesianVector:
        r"""calculate the momentum vector using equation 1-15 in :ref:`vallado`

        .. math::

           \vec{h} = \vec{r} \times \vec{v}

        :param r: position vector
        :param v: velocity vector
        """
        return r.cross(v)
