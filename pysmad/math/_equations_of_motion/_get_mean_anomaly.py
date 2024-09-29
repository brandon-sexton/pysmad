from math import pi, sin


class GetMeanAnomaly:
    """static class used to solve mean anomaly

    .. note::

       mean anomaly will commonly be referenced as :math:`M` in documentation
    """

    @staticmethod
    def from_ea_e(ea: float, e: float) -> float:
        r"""calculate mean anomaly using equation 2-4 in :ref:`vallado`

        .. math::

           M = E - e\sin{(E)}

        :param ea: eccentric anomaly in :math:`rads`
        :type ea: float
        :param e: eccentricity
        :type e: float
        :return: mean anomaly in :math:`rads`
        :rtype: float
        """
        ma: float = ea - e * sin(ea)
        if ma < 0:
            ma += 2 * pi
        return ma
