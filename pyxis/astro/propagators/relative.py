from math import sin, cos, sqrt

from pyxis.astro.coordinates import HillState
from pyxis.astro.bodies.celestial import Earth
from pyxis.math.linalg import Matrix6D, Vector6D, Vector3D

class Hill:
    
    DEFAULT_STEP_SIZE:float = 600

    def __init__(self, state:HillState, sma:float) -> None:
        self.state:HillState = state.copy()
        self.sma:float = sma
        self.n:float = sqrt(Earth.MU/(sma*sma*sma))
        self.step_size = Hill.DEFAULT_STEP_SIZE

    def system_matrix(self, t:float) -> Matrix6D:
        n = self.n
        n_inv = 1/n
        sn = sin(n*t)
        cs = cos(n*t)
		
		#define system matrix of x, y, z, x_dot, y_dot, z_dot equations
        sys_mat = Matrix6D(
			Vector6D(4-3*cs, 0, 0, sn*n_inv, 2*(1-cs)*n_inv, 0),
			Vector6D(6*(sn-n*t), 1, 0, -2*(1-cs)*n_inv, (4*sn-3*n*t)*n_inv, 0),
			Vector6D(0, 0, cs, 0, 0, sn*n_inv),
			Vector6D(3*n*sn, 0, 0, cs, 2*sn, 0),
			Vector6D(-6*n*(1-cs), 0, 0, -2*sn, 4*cs-3, 0),
			Vector6D(0, 0, -n*sn, 0, 0, cs)
		)
					
        return sys_mat

    def step_by_seconds(self, t:float) -> None:
        self.state = HillState.from_state_vector(self.system_matrix(t).multiply_vector(self.state.vector))

    def step(self) -> None:
        self.step_by_seconds(self.step_size)
