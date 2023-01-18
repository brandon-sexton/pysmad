from openspace.coordinates.positions import Position
from openspace.coordinates.velocitites import Velocity
from openspace.time import Epoch


class State:
    def __init__(self, epoch: Epoch, r: Position, v: Velocity) -> None:
        """class used to perform operations for time-dependent states

        :param epoch: time for which the position and velocity are valid
        :type epoch: Epoch
        :param r: position of the state
        :type r: Position
        :param v: velocity of the state
        :type v: Velocity
        """
        #: time for which the position and velocity are valid
        self.epoch: Epoch = epoch.copy()

        #: position of the state
        self.position: Position = r.copy()

        #: velocity of the state
        self.velocity: Velocity = v.copy()
