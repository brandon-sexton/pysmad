import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.getcwd())

from pyxis.astro.propagators.inertial import RK4
from pyxis.astro.propagators.relative import Hill
from pyxis.astro.coordinates import GCRFstate, HillState
from pyxis.astro.bodies.artificial import Spacecraft
from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch

start_epoch:Epoch = Epoch.from_gregorian(2022, 12, 20, 0, 0, 0)
rel_chase_state = HillState(Vector3D(-11, 0, 0), Vector3D(0, .0016, 0))
target_state:GCRFstate = GCRFstate(start_epoch, Vector3D(42164, 0, 0), Vector3D(0, 3.075, 0))
seed:Spacecraft = Spacecraft(GCRFstate(start_epoch, Vector3D(42164.5, .5, .5), Vector3D(0, 3.074, 0)))
chase_state:GCRFstate = GCRFstate.from_hill(target_state, rel_chase_state)
end_epoch = start_epoch.plus_days(2)

chase:Spacecraft = Spacecraft(chase_state)
target:Spacecraft = Spacecraft(target_state)

rel = Hill(rel_chase_state, 42164)

hill_r = []
hill_i = []
rk_r = []
rk_i = []
times = []
err = []

chase.acquire(seed)
while chase.current_epoch().value < end_epoch.value:
    
    chase.step()
    target.step_to_epoch(chase.current_epoch())
    chase.track_state(target)
    chase.process_wfov(target)
    rel.step_by_seconds(chase.propagator.step_size)

    ric = chase.hill_position(target)
    nav = chase.filter.propagator.state.position
    rk_r.append(ric.x)
    rk_i.append(ric.y)
    hill_r.append(rel.state.position.x)
    hill_i.append(rel.state.position.y)
    times.append(chase.current_epoch().value)
    err.append(abs(nav.magnitude() - ric.magnitude()))

plt.plot(times, err)
plt.show()
