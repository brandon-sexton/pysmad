from math import sqrt


class Eccentricity:
    """Class used to solve eccentricity of an ellipse

    .. note::

        * This class is intendend to be used as the alias found in :ref:`EquationsOfMotion <equations_of_motion>`.
        * Eccentricity is a measure of how much an ellipse deviates from a perfect circle.  It is often
          represented as :math:`e`
    """

    @staticmethod
    def from_a_c(a: float, c: float) -> float:
        r"""calculate eccentricity using equation 1-2 in :ref:`vallado`

        .. math::

           e = \frac{c}{a}

        :param a: semi-major axis in :math:`km`
        :param c: half the distance between focii in :math:`km`
        """
        return c / a

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        r"""calculate eccentricity using equation 1-6 in :ref:`vallado`

        .. math::

           e = \frac{\sqrt{a^2-b^2}}{a}

        :param a: semi-major axis in :math:`km`
        :param b: semi-minor axis in :math:`km`
        """
        return sqrt(a * a - b * b) / a

    @staticmethod
    def from_a_p(a: float, p: float) -> float:
        r"""calculate eccentricity using equation 2.62 in :ref:`orbits`

        .. math::

           e = \sqrt{1 - \frac{p}{a}}

        :param a: semi-major axis in :math:`km`
        :param p: semi-parameter in :math:`km`
        """
        return sqrt(1 - p / a)

    @staticmethod
    def from_f(f: float) -> float:
        r"""Calculate eccentricity using equation 1-8 in :ref:`vallado`

        .. math::

           e = \sqrt{1 - \left(1 -f\right)^2}

        :param f: flattening of the ellipse
        """
        return sqrt(1 - (1 - f) * (1 - f))

    @staticmethod
    def from_a_apoapsis(a: float, r: float) -> float:
        r"""Calculate eccentricity using equation 2-81 in :ref:`vallado`

        .. math::

           e = \frac{r_a - a}{a}

        :param a: semi-major axis in :math:`km`
        :param r: apoapsis in :math:`km`
        """
        return (r - a) / a

    @staticmethod
    def from_a_periapsis(a: float, r: float) -> float:
        r"""Calculate eccentricity using equation 2-81 in :ref:`vallado`

        .. math::

           e = \frac{a - r_p}{a}

        :param a: semi-major axis in :math:`km`
        :param r: periapsis in :math:`km`
        """
        return (a - r) / a

    @staticmethod
    def from_xi_h_mu(xi: float, h: float, mu: float) -> float:
        r"""Calculate eccentricity using equation 2-79 in :ref:`vallado`

        .. math::

            e = \sqrt{1 + \frac{2\xi h^2}{\mu^2}}

        :param xi: Specific mechanical energy
        :param h: areal velocity magnitude
        :param mu: gravitational constant times mass of central body
        """
        return sqrt(1 + 2 * xi * h * h / (mu * mu))
