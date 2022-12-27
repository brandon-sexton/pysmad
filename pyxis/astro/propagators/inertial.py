from math import ceil
from typing import List

from pyxis.astro.coordinates import GCRFstate
from pyxis.math.constants import SECONDS_IN_DAY
from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch


class RK4:

    #: Largest step to be taken by the integrator
    MAX_STEP = 300

    def __init__(self, state: GCRFstate) -> None:
        """class used to propagate a satellite state

        :param state: ECI state of the satellite to be propagated
        :type state: GCRFstate
        """
        self.state: GCRFstate = state.copy()
        self.step_size: float = RK4.MAX_STEP

    def step(self) -> None:
        """advance the propagator state by the stored time step"""
        h = self.step_size

        epoch_0: Epoch = self.state.epoch.copy()

        y: List[Vector3D] = self.state.vector_list()

        k1: List[Vector3D] = self.state.derivative()

        dsecs: float = h / 2
        ddays: float = dsecs / SECONDS_IN_DAY
        epoch_1 = epoch_0.plus_days(ddays)
        y1: GCRFstate = GCRFstate(epoch_1, y[0].plus(k1[0].scaled(dsecs)), y[1].plus(k1[1].scaled(dsecs)))
        k2: List[Vector3D] = y1.derivative()

        y2: GCRFstate = GCRFstate(epoch_1, y[0].plus(k2[0].scaled(dsecs)), y[1].plus(k2[1].scaled(dsecs)))
        k3: List[Vector3D] = y2.derivative()

        epoch_2 = epoch_1.plus_days(ddays)
        y3: GCRFstate = GCRFstate(epoch_2, y[0].plus(k3[0].scaled(h)), y[1].plus(k3[1].scaled(h)))
        k4: List[Vector3D] = y3.derivative()

        coeff: float = 1 / 6
        dv: Vector3D = k1[0].plus(k2[0].scaled(2).plus(k3[0].scaled(2).plus(k4[0]))).scaled(coeff)
        da: Vector3D = k1[1].plus(k2[1].scaled(2).plus(k3[1].scaled(2).plus(k4[1]))).scaled(coeff)

        self.state = GCRFstate(
            epoch_2,
            self.state.position.plus(dv.scaled(h)),
            self.state.velocity.plus(da.scaled(h)),
        )

    def step_to_epoch(self, epoch: Epoch) -> None:
        """advance the propagator state to the argument epoch

        :param epoch: time of state to be calculated
        :type epoch: Epoch
        """

        # Calculate time delta in seconds
        dt = (epoch.value - self.state.epoch.value) * SECONDS_IN_DAY

        # Determine number of steps required to meet new epoch while staying below the maximum step
        num_steps = ceil(abs(dt / self.MAX_STEP))

        # Store current step size
        old_step = self.step_size

        # Temporarily set step size to calculated dt
        if num_steps > 0:
            self.step_size = dt / num_steps

        # Step until desired epoch is achieved
        step_n = 0
        while step_n < num_steps:
            self.step()
            step_n += 1

        # Reset step size
        self.step_size = old_step
