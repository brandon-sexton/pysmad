import matplotlib.pyplot as plt

from pysmad.bodies.artificial import Spacecraft
from pysmad.coordinates.states import GCRF, HCW, StateConvert
from pysmad.math.linalg import Vector3D, Vector6D
from pysmad.time import Epoch

# Create scenario start epoch
start_epoch: Epoch = Epoch.from_gregorian(2022, 12, 20, 0, 0, 0)

# Create ECI state for target
target_state: GCRF = GCRF(start_epoch, Vector3D(42164, 0, 0), Vector3D(0, 3.075, 0))
target: Spacecraft = Spacecraft(target_state)

# Step target forward 6 hours
target.step_to_epoch(start_epoch.plus_days(0.25))

# Define propagation end of 1 day after current target epoch
end_epoch = target.current_epoch().plus_days(1)

# Create chase state relative to target
rel_chase_state = HCW.from_state_vector(Vector6D(-11, 0, 0, 0, 0.0016, 0))
chase_state: GCRF = StateConvert.hcw.to_gcrf(rel_chase_state, target.current_state())
chase: Spacecraft = Spacecraft(chase_state)

# Create empty data lists
times, detections, resolutions = [], [], []

# Place chase in target-tracking attitude
chase.track_state(target)

# Propagate
while chase.current_epoch().value < end_epoch.value:

    # Step vehicles and sync epochs
    chase.step()
    target.step_to_epoch(chase.current_epoch())

    # Store epochs
    times.append(chase.current_epoch().value)

    # Store resolutions
    resolutions.append(chase.nfov.resolution(chase.range(target)) * 1e5)

    # Use binary reference of visible (1) or not (0)
    if chase.detect(target):
        detections.append(1)
    else:
        detections.append(0)

# Plot data
plt.plot(times, detections)
plt.plot(times, resolutions)
plt.show()
