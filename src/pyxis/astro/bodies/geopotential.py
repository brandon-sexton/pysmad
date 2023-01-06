from typing import List


class EGM2008:
    """class used to store the normalized coefficients of the EGM2008 model"""

    #: normalized c coefficients used for geopotential calculation
    C: List[List[float]] = [
        [1],
        [0, 0],
        [-0.484165143790815e-3, -0.206615509074176e-9, 0.243938357328313e-5],
        [0.957161207093473e-6, 0.203046201047864e-5, 0.904787894809528e-6, 0.721321757121568e-6],
        [
            0.539965866638991e-6,
            -0.536157389388867e-6,
            0.350501623962649e-6,
            0.990856766672321e-6,
            -0.188519633023033e-6,
        ],
    ]

    #: normalized s coefficients used for geopotential calculation
    S: List[List[float]] = [
        [0],
        [0, 0],
        [0, 0.138441389137979e-8, -0.140027370385934e-5],
        [0, 0.248200415856872e-6, -0.619005475177618e-6, 0.141434926192941e-5],
        [0, -0.473567346518086e-6, 0.662480026275829e-6, -0.200956723567452e-6, 0.308803882149194e-6],
    ]

    #: G*M given in km^3/s^2
    MU: float = 398600.4418

    #: distance from earth center to surface at the equator in km
    RADIUS: float = 6378.137

    #: value defining the ellipsoid of an oblate earth
    FLATTENING: float = 1 / 298.2572235
