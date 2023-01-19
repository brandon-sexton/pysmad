import matplotlib.pyplot as plt

from openspace.bodies.artificial import Spacecraft
from openspace.coordinates.states import GCRF, HCW, StateConvert
from openspace.math.linalg import Vector3D, Vector6D
from openspace.time import Epoch

# Define the initial time reference
start_epoch: Epoch = Epoch.from_gregorian(2022, 12, 20, 0, 0, 0)

# Create a desired relative state for the chase vehicle
rel_chase_state = HCW.from_state_vector(Vector6D(-11, 0, 0, 0, 0, 0))

# Create an inertial state for the target vehicle
target_state: GCRF = GCRF(start_epoch, Vector3D(42164, 0, 0), Vector3D(0, 3.075, 0))

# Create a spacecraft to act as an estimated state of the target spacecraft which will be used to initialize the filter
seed: Spacecraft = Spacecraft(GCRF(start_epoch, Vector3D(42164.5, 0.5, 0.5), Vector3D(0, 3.075, 0)))

# Create the chase vehicle's inertial state using the target state as the origin
chase_state: GCRF = StateConvert.hcw.to_gcrf(rel_chase_state, target_state)

# Define a propagation epoch of one day
end_epoch = start_epoch.plus_days(1)

# Create the target and chase spacecraft
chase: Spacecraft = Spacecraft(chase_state)
target: Spacecraft = Spacecraft(target_state)

# Create empty lists to store data
times, err = [], []

# Initialize the kalman filter with the estimated state
chase.acquire(seed)

# Propagate
while chase.current_epoch().value < end_epoch.value:

    # Increment the epochs of the spacecraft
    chase.step()
    target.step_to_epoch(chase.current_epoch())

    # Update chase attitude to point payloads at target
    chase.track_state(target)

    # Create a simulated ob and feed it to the filter
    chase.process_wfov(target)

    # Get the relative truth state
    ric = chase.hill_position(target)

    # Get the relative estimate from the chase solution
    nav = chase.filter.propagator.state.position

    # Store data
    times.append(chase.current_epoch().value)
    err.append(abs(nav.magnitude() - ric.magnitude()))

# Plot results
plt.plot(times, err)
plt.show()
