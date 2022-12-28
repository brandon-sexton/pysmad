from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch


class PositionOb:
    def __init__(self, epoch: Epoch, position: Vector3D, error: float) -> None:
        """class used to store an observation that contains position only

        :param epoch: time of the observation
        :type epoch: Epoch
        :param position: observed position vector in km
        :type position: Vector3D
        :param error: error associated with the magnitude of the observed position vector in km
        :type error: float
        """
        #: time of the observation
        self.epoch: Epoch = epoch.copy()

        #: observed position in km
        self.position: Vector3D = position.copy()

        #: error in km of the observed position magnitude
        self.error: float = error
