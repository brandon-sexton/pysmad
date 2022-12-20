import matplotlib.pyplot as plt
import sys
import os

import time

sys.path.append(os.getcwd())

from pyxis.astro.propagators.inertial import RK4
from pyxis.astro.coordinates import GCRFstate
from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch

start_epoch = Epoch.from_gregorian(2022, 12, 20, 0, 0, 0)
start_position = Vector3D(42160, 0, 0)
start_velocity = Vector3D(0, 3.075, 0)
end_epoch = start_epoch.plus_days(1)
propagator = RK4(GCRFstate(start_epoch, start_position, start_velocity))
times = []
radii = []

while propagator.state.epoch.value < end_epoch.value:
    propagator.step()
    times.append(propagator.state.epoch.value)
    radii.append(propagator.state.position.magnitude())

plt.plot(times, radii)
plt.show()