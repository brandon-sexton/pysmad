import matplotlib.pyplot as plt

from openspace.bodies.artificial import Spacecraft
from openspace.coordinates.states import GCRF
from openspace.math.linalg import Vector3D
from openspace.time import Epoch

# Create initial scenario epoch
start_epoch: Epoch = Epoch.from_gregorian(2022, 12, 20, 0, 0, 0)

# Create an ECI state for the spacecraft
passive_state: GCRF = GCRF(start_epoch, Vector3D(42164, 0, 0), Vector3D(0, 3.075, 0))

# Create a propagation end epoch after 2 days
end_epoch = start_epoch.plus_days(2)

# Load states
freeflight: Spacecraft = Spacecraft(passive_state)
maneuver: Spacecraft = Spacecraft(passive_state)

rk_r = []
rk_i = []
maneuver_complete: bool = False
maneuver_direction: Vector3D = Vector3D(0, 0.003, 0)

# Propagate
while freeflight.current_epoch().value < end_epoch.value:

    # Step vehicles and propagator
    freeflight.step()
    maneuver.step_to_epoch(freeflight.current_epoch())

    # Calculate the hill state of chase and target after RK4 propagation
    ric = freeflight.hill_position(maneuver)

    # Perform a maneuver after one day
    if freeflight.current_epoch().value > start_epoch.value + 1 and not maneuver_complete:
        maneuver.finite_maneuver(maneuver_direction)
        freeflight.step_to_epoch(maneuver.current_epoch())
        maneuver_complete = True

    # Store data
    rk_r.append(ric.x)
    rk_i.append(ric.y)

# Overlay RI points of RK4 and Hill
plt.plot(rk_i, rk_r)
plt.show()
