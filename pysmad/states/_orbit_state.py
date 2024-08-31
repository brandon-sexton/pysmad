from pysmad.elements import CartesianElements
from pysmad.time import Epoch


class OrbitState:
    def __init__(self, epoch: Epoch, elements: CartesianElements) -> None:
        self.epoch = epoch
        self.vector = elements
