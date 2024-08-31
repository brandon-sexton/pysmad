from math import atan2, cos, pi, sin, sqrt


class EccentricAnomaly:
    r"""class used to solve eccentric anomaly

    .. note::

       eccentric anomaly will commonly be referenced as :math:`E` in documentation"""

    #: the tolerance used to stop the recursive solutions of Kepler's equation
    TOLERANCE: float = 1e-12

    @staticmethod
    def from_ma_e(ma: float, e: float) -> float:
        r"""calculate the eccentric anomaly using algorithm 2 in :ref:`vallado`

        .. math::

           E_{n+1} = E_n + \left(\frac{M-E_n+e\sin{(E_n)}}{1-e\cos{(E_n)}}\right)

        .. note::

           :math:`E_0 = M - e` for :math:`-\pi<M<0` or :math:`M>\pi`
           otherwise :math:`E_0 = M + e`

           looping continues until :math:`\vert E_{n+1} - E_n\vert < tolerance`

        :param ma: mean anomaly in :math:`rads`
        :type ma: float
        :param e: eccentricity
        :type e: float
        :return: eccentric anomaly in :math:`rads`
        :rtype: float
        """
        converged: bool = False
        ea0: float = ma

        if (ma > -pi and ma < 0) or ma > pi:
            ea0 -= e
        else:
            ea0 += e

        while not converged:
            ean = ea0 + (ma - ea0 + e * sin(ea0)) / (1 - e * cos(ea0))
            if abs(ean - ea0) < EccentricAnomaly.TOLERANCE:
                converged = True
            else:
                ea0 = ean

        if ean < 0:
            ean += 2 * pi
        return ean

    @staticmethod
    def from_rdv_r_a_n(r_dot_v: float, r: float, a: float, n: float) -> float:
        r"""calculate eccentric anomaly

        :param r_dot_v: dot product of position and velocity
        :type r_dot_v: float
        :param r: magnitude of position in :math:`km`
        :type r: float
        :param a: semi-major axis in :math:`km`
        :type a: float
        :param n: mean motion in :math:`\frac{rad}{s}`
        :type n: float
        :return: eccentric anomaly in :math:`rads`
        :rtype: float

        .. todo::

           find equation reference
        """
        ea: float = atan2(r_dot_v / (a * a * n), 1 - r / a)
        if ea < 0:
            ea += 2 * pi
        return ea

    @staticmethod
    def from_e_nu(e: float, nu: float) -> float:
        r"""calculate eccentric anomaly

        :param e: eccentricity
        :type e: float
        :param nu: true anomaly in :math:`rads`
        :type nu: float
        :return: eccentric anomaly in :math:`rads`
        :rtype: float
        """
        cnu = cos(nu)
        den = 1 / (1 + e * cnu)
        sin_ea = sin(nu) * sqrt(1 - e * e) * den
        cos_ea = (e + cnu) * den
        return atan2(sin_ea, cos_ea)
