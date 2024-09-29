from math import sqrt


class GetFlattening:
    """class used to solve flattening of an ellipse

    .. note::

       * This class is intendend to be accessed from the alias found in :ref:`EquationsOfMotion <equations_of_motion>`.
       * Flattening is a measure of how much an ellipsoid deviates from a perfect sphere.  It is often
         represented as :math:`f`
    """

    @staticmethod
    def from_a_b(a: float, b: float) -> float:
        """calculate flattening using equation 1-3 in :ref:`vallado`

        .. math::

           f = \frac{a-b}{a}

        :param a: semi-major axis
        :param b: semi-minor axis
        """
        return (a - b) / a

    @staticmethod
    def from_e(e: float) -> float:
        r"""Calculate the flattening using equation 1-8 in :ref:`vallado`

        .. math::

            f = 1 - \sqrt{1 - e^2}

        :param e: eccentricity
        """
        return 1 - sqrt(1 - e * e)
