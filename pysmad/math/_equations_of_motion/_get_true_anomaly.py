from math import atan2, cos, pi, sin, sqrt


class GetTrueAnomaly:
    r"""static class used to solve true anomaly

    .. note::

       true anomaly will commonly be referenced as :math:`\nu` in documentation
    """

    @staticmethod
    def from_e_ea(e: float, ea: float) -> float:
        """calculate true anomaly

        :param e: eccentricity
        :type e: float
        :param ea: eccentric anomaly in :math:`rads`
        :type ea: float
        :return: true anomaly in :math:`rads`
        :rtype: float

        .. todo::

           find equation reference
        """
        ta: float = atan2(sqrt(1 - e * e) * sin(ea), cos(ea) - e)
        if ta < 0:
            ta += 2 * pi
        return ta
