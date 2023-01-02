from math import cos, sin

from pyxis.astro.coordinates import LLAstate
from pyxis.math.linalg import Matrix3D, Vector3D


class GroundSite:
    def __init__(self, lla: LLAstate) -> None:
        """used for operations that require modeling of a terrestrial location

        :param lla: state that holds the latitude, longitude, and altitude of the ground station
        :type lla: LLAstate
        """
        self.lla: LLAstate = lla.copy()
        self.itrf_position: Vector3D = self.lla.itrf_position()
        slamb: float = sin(self.lla.longitude)
        clamb: float = cos(self.lla.longitude)
        spsi: float = sin(self.lla.latitude)
        cpsi: float = cos(self.lla.latitude)
        self.enz_matrix: Matrix3D = Matrix3D(
            Vector3D(-slamb, clamb, 0.0),
            Vector3D(-spsi * clamb, -spsi * slamb, cpsi),
            Vector3D(cpsi * clamb, cpsi * slamb, spsi),
        )

    def enz_position(self, obj_itrf: Vector3D) -> Vector3D:
        """calculates the east-north-zenith coordinates of the argument position

        :param obj_itrf: itrf position of the object of interest
        :type obj_itrf: Vector3D
        :return: transformation of the argument itrf position to the east-north-zenith frame
        :rtype: Vector3D
        """
        return self.enz_matrix.multiply_vector(obj_itrf.minus(self.itrf_position))
