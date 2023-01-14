import unittest

from openspace.astro.coordinates import GCRFstate
from openspace.astro.propagators.inertial import RK4
from openspace.math.linalg import Vector3D
from openspace.time import Epoch


class TestRK4(unittest.TestCase):

    EPOCH: Epoch = Epoch.from_gregorian(2022, 12, 20, 0, 1, 9.184)
    POSITION: Vector3D = Vector3D(42164, 0, 0)
    VELOCITY: Vector3D = Vector3D(0, 3.07375, 0)
    STATE: GCRFstate = GCRFstate(EPOCH, POSITION, VELOCITY)
    PROPAGATOR: RK4 = RK4(STATE)

    def test_step_to_epoch(self):
        end_epoch: Epoch = Epoch.from_gregorian(2022, 12, 20, 19, 1, 9.184)
        self.PROPAGATOR.step_to_epoch(end_epoch)
        self.assertAlmostEqual(self.PROPAGATOR.state.position.x, 11701.163084, -1)
        self.assertAlmostEqual(self.PROPAGATOR.state.position.y, -40487.016256, -1)
        self.assertAlmostEqual(self.PROPAGATOR.state.position.z, -2.099302, -1)
        self.assertAlmostEqual(self.PROPAGATOR.state.velocity.x, 2.954853, 4)
        self.assertAlmostEqual(self.PROPAGATOR.state.velocity.y, 0.851923, 4)
        self.assertAlmostEqual(self.PROPAGATOR.state.velocity.z, -0.000141, 4)
