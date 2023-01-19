from openspace.math.linalg import Vector3D, Vector6D
from openspace.time import Epoch


class State:
    def __init__(self, epoch: Epoch, r: Vector3D, v: Vector3D) -> None:
        """class used to perform operations for time-dependent states

        :param epoch: time for which the position and velocity are valid
        :type epoch: Epoch
        :param r: position of the state
        :type r: Vector3D
        :param v: velocity of the state
        :type v: Vector3D
        """
        #: time for which the position and velocity are valid
        self.epoch: Epoch = epoch.copy()

        #: position of the state
        self.position: Vector3D = r.copy()

        #: velocity of the state
        self.velocity: Vector3D = v.copy()

        #: state vector whose elements are equal to that of the position and velocity unpacked
        self.vector = Vector6D.from_position_and_velocity(self.position, self.velocity)


class GCRF(State):
    def __init__(self, epoch: Epoch, r: Vector3D, v: Vector3D) -> None:
        """class used to perform operations and modeling in the Geocentric Celestial Reference Frame

        :param epoch: time for which the position and velocity are valid
        :type epoch: Epoch
        :param r: position of the state
        :type r: Vector3D
        :param v: velocity of the state
        :type v: Vector3D
        """
        super().__init__(epoch, r, v)
