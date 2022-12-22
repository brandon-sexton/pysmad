import matplotlib.pyplot as plt
import sys
import os

from math import degrees

sys.path.append(os.getcwd())

from pyxis.astro.coordinates import GCRFstate, HillState
from pyxis.astro.bodies.artificial import Spacecraft
from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch

start_epoch:Epoch = Epoch.from_gregorian(2022, 12, 20, 0, 0, 0)
target_state:GCRFstate = GCRFstate(start_epoch, Vector3D(42164, 0, 0), Vector3D(0, 3.075, 0))
target:Spacecraft = Spacecraft(target_state)
target.step_to_epoch(start_epoch.plus_days(.25))

end_epoch = target.current_epoch().plus_days(1)

rel_chase_state = HillState(Vector3D(-11, 0, 0), Vector3D(0, .0016, 0))
chase_state:GCRFstate = GCRFstate.from_hill(target.current_state(), rel_chase_state)
chase:Spacecraft = Spacecraft(chase_state)

times, detections, resolutions = [], [], []
chase.track_state(target)
while chase.current_epoch().value < end_epoch.value:
    chase.step()
    target.step_to_epoch(chase.current_epoch())

    times.append(chase.current_epoch().value)
    resolutions.append(chase.nfov.resolution(chase.range(target))*1e5)
    if chase.detect(target):
        detections.append(1)
    else:
        detections.append(0)

plt.plot(times, detections)
plt.plot(times, resolutions)
plt.show()