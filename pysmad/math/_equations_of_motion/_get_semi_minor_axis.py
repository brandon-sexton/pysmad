from math import sqrt


class GetSemiMinorAxis:
    """class used to solve semi-minor axis of an ellipse

    .. note::

    This class is intendend to be used as the alias found in :ref:`EquationsOfMotion <equations_of_motion>`.
    """

    @staticmethod
    def from_a_e(a: float, e: float) -> float:
        r"""calculate semi-minor axis using equation 1-4 in :ref:`vallado`

        .. math::

           b = a\sqrt{1-e^2}

        :param a: semi-major axis in :math:`km`
        :param e: eccentricity
        """
        return a * sqrt(1 - e * e)
