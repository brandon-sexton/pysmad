from pyxis.time import Epoch
from pyxis.math.linalg import Vector3D

class PositionOb:
    def __init__(self, epoch:Epoch, position:Vector3D, error:float) -> None:
        self.epoch:Epoch = epoch.copy()
        self.position:Vector3D = position.copy()
        self.error:float = error
        