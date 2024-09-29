from math import pi, sqrt


class GetMeanMotion:
    r"""class used to calculate mean motion of an orbit

    .. note::

       mean motion will commonly be referenced as :math:`n` in documentation"""

    @staticmethod
    def from_a_mu(a: float, mu: float) -> float:
        r"""calculate the mean motion using equation 1-27 in :ref:`vallado`

        .. math::

           n = \frac{2\pi}{\tau} = \sqrt{\frac{\mu}{a^3}}

        :param a: semi-major axis in :math:`km`
        :type a: float
        :param mu: gravitational constant time mass of central body combined units of :math:`\frac{km^3}{s^2}`
        :type mu: float
        :return: mean motion in :math:`\frac{rad}{s}`
        :rtype: float
        """
        return sqrt(mu / (a * a * a))

    @staticmethod
    def from_tau(tau: float) -> float:
        r"""calculate mean motion using equation 1-27 in :ref:`vallado`

        .. math::

           n = \frac{2\pi}{\tau} = \sqrt{\frac{\mu}{a^3}}

        :param tau: period of orbit in :math:`s`
        :type tau: float
        :return: mean motion in :math:`\frac{rad}{s}`
        :rtype: float
        """
        return 2 * pi / tau
