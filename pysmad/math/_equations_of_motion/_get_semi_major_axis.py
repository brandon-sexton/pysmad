from math import pi


class GetSemiMajorAxis:
    """class used to solve semi-major axis of an ellipse

    .. note::

       This class is intendend to be accessed from the alias found in :ref:`EquationsOfMotion <equations_of_motion>`.
    """

    @staticmethod
    def from_mu_n(mu: float, n: float) -> float:
        r"""calculate semi-major axis using equation 1-29 in :ref:`vallado`

        .. math::

           a = \sqrt[3]{\frac{\mu}{n^2}}

        :param mu: gravitational constant time mass of central body
        :param n: mean motion
        """
        return (mu / (n * n)) ** (1 / 3)

    @staticmethod
    def from_mu_tau(mu: float, tau: float) -> float:
        r"""calculate semi-major axis using equation 1-27 in :ref:`vallado`

        .. math::

           n = \frac{2\pi}{\tau} = \sqrt{\frac{\mu}{a^3}}

        :param mu: gravitational constant time mass of central body
        :param tau: period in :math:`s`
        """
        base: float = tau / (2 * pi)
        return (mu * base * base) ** (1 / 3)

    @staticmethod
    def from_mu_r_v(mu: float, r: float, v: float) -> float:
        r"""calculate the semi-major axis in km using equation 1-31 in :ref:`vallado`

        .. math::

           v = \sqrt{\frac{2\mu}{r}+\frac{\mu}{a}}

        :param mu: gravitational constant time mass of central body
        :param r: magnitude of the position vector
        :param v: magnitude of the velocity vector
        """
        return 1 / (2 / r - v * v / mu)

    @staticmethod
    def from_p_e(p: float, e: float) -> float:
        r"""calculate semi-major axis using equation 2.20 in :ref:`orbits`

        .. math::

           a = \frac{p}{1-e^2}

        :param p: semi-latus rectum
        :param e: eccentricity
        """
        return p / (1 - e * e)
