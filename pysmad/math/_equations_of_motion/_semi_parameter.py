class SemiParameter:
    """class used to solve the semi-parameter of an ellipse

    .. note::

     This class is intendend to be used as the alias found in :ref:`EquationsOfMotion <equations_of_motion>`.
    """

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        r"""calculate the semi-parameter using equation 1-9 in :ref:`vallado`

        .. math::

           p = \frac{b^2}{a}

        :param a: semi-major axis
        :param b: semi-minor axis
        """
        return b * b / a

    @staticmethod
    def from_a_e(a: float, e: float) -> float:
        r"""calculate the semi-parameter using equation 1-10 in :ref:`vallado`

        .. math::

           p = a(1-e^2)

        :param a: semi-major axis
        :param e: eccentricity
        """
        return a * (1 - e * e)

    @staticmethod
    def from_mu_h(mu: float, h: float) -> float:
        r"""calculate the semi-parameter using equation 1-19 in :ref:`vallado`

        .. math::

           p = \frac{h^2}{\mu}

        :param mu: gravitational constant times mass of central body
        :param h: areal velocity magnitude
        """
        return h * h / mu
