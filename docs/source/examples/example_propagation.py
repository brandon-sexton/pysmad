import matplotlib.pyplot as plt

from pysmad.bodies.artificial import Spacecraft
from pysmad.coordinates.states import GCRF, HCW, StateConvert
from pysmad.math.linalg import Vector3D, Vector6D
from pysmad.propagators.relative import Hill
from pysmad.time import Epoch

# Create initial scenario epoch
start_epoch: Epoch = Epoch.from_gregorian(2022, 12, 20, 0, 0, 0)

# Create a desired relative state for the chase vehicle
rel_chase_state = HCW.from_state_vector(Vector6D(-11, 0, 0, 0, 0.0016, 0))

# Create an ECI state for the target to act as the origin
target_state: GCRF = GCRF(start_epoch, Vector3D(42164, 0, 0), Vector3D(0, 3.075, 0))

# Create an ECI state for the chase vehicle using the target ECI state as the origin
chase_state: GCRF = StateConvert.hcw.to_gcrf(rel_chase_state, target_state)

# Create a propagation end epoch after 5 days
end_epoch = start_epoch.plus_days(5)

# Load states for chase and target
chase: Spacecraft = Spacecraft(chase_state)
target: Spacecraft = Spacecraft(target_state)

# Create a Hill propagator to compare RK4 results
rel = Hill(rel_chase_state, target.sma())

hill_r = []
hill_i = []
rk_r = []
rk_i = []

# Propagate
while chase.current_epoch().value < end_epoch.value:

    # Step vehicles and propagator
    chase.step()
    target.step_to_epoch(chase.current_epoch())
    rel.step_by_seconds(chase.propagator.step_size)

    # Calculate the hill state of chase and target after RK4 propagation
    ric = target.hill_position(chase)

    # Store data
    rk_r.append(ric.x)
    rk_i.append(ric.y)
    hill_r.append(rel.state.position.x)
    hill_i.append(rel.state.position.y)

# Overlay RI points of RK4 and Hill
plt.plot(hill_i, hill_r)
plt.plot(rk_i, rk_r)
plt.show()
