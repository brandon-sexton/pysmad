from math import pi


class GetArgumentOfPerigee:
    r"""static class used to solve argument of perigee

    .. note::

       argument of perigee will commonly be referenced as :math:`\omega` in documentation
    """

    @staticmethod
    def from_u_nu(u: float, nu: float) -> float:
        r"""calculate the argument of perigee

        :param u: argument of latitude in :math:`rads`
        :type u: float
        :param nu: true anomaly in :math:`rads`
        :type nu: float
        :return: argument of perigee in :math:`rads`
        :rtype: float

        .. todo::

           find equation reference
        """
        w: float = u - nu
        if w < 0:
            w += 2 * pi
        return w
