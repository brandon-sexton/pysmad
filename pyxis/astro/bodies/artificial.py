from pyxis.astro.coordinates import GCRFstate
from pyxis.astro.propagators.inertial import RK4
from pyxis.time import Epoch
from pyxis.math.linalg import Vector3D

class Spacecraft:
    def __init__(self, state:GCRFstate):
        self.state:GCRFstate = state.copy()
        self.propagator:RK4 = RK4(self.state)

    def step(self) -> None:
        self.propagator.step()

    def step_to_epoch(self, epoch:Epoch) -> None:
        self.propagator.step_to_epoch(epoch)

    def sun_vector(self) -> Vector3D:
        return self.propagator.state.sun_vector()

    def moon_vector(self) -> Vector3D:
        return self.propagator.state.moon_vector()

    def earth_vector(self) -> Vector3D:
        return self.propagator.state.position.scaled(-1)

    def target_vector(self, target:"Spacecraft") -> Vector3D:
        return target.propagator.state.position.minus(self.propagator.state.position)