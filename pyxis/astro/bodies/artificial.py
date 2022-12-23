from typing import List
from math import pi, sin, cos, log10, radians

from pyxis.astro.coordinates import GCRFstate, HillState
from pyxis.astro.propagators.inertial import RK4
from pyxis.time import Epoch
from pyxis.math.linalg import Vector3D
from pyxis.hardware.payloads import Camera
from pyxis.math.constants import SECONDS_IN_DAY
from pyxis.astro.bodies.celestial import Earth

class Spacecraft:

    DEFAULT_RADIUS = .005
    DEFAULT_ALBEDO = .3
    STEERING_MODES = ["lvlh", "solar", "target"]
    DEFAULT_SLEW_RATE = radians(.5)*SECONDS_IN_DAY

    def __init__(self, state:GCRFstate):
        self.initial_state:GCRFstate = state.copy()
        self.propagator:RK4 = RK4(self.initial_state)
        self.albedo:float = Spacecraft.DEFAULT_ALBEDO
        self.body_radius:float = Spacecraft.DEFAULT_RADIUS
        self.wfov:Camera = Camera.wfov()
        self.nfov:Camera = Camera.nfov()
        self.steering:str = Spacecraft.STEERING_MODES[0]
        self.tracked_target:Spacecraft = None
        self.slewing:bool = False
        self.slew_stop:Epoch = None
        self.slew_rate:float = Spacecraft.DEFAULT_SLEW_RATE
        self.update_attitude()
    
    def sma(self):
        r = self.position().magnitude()
        v = self.velocity().magnitude()
        return 1/(2/r - v*v/Earth.MU)

    def update_attitude(self) -> None:
        if self.steering == Spacecraft.STEERING_MODES[0]:
            self.body_z = self.earth_vector()
            self.body_y = self.position().cross(self.velocity())
            self.body_x = self.body_y.cross(self.body_z)
        elif self.steering == Spacecraft.STEERING_MODES[1]:
            self.body_z = self.sun_vector().scaled(-1)
            self.body_x = self.body_z.cross(Vector3D(0, 0, 1))
            self.body_y = self.body_z.cross(self.body_x)
        elif self.steering == Spacecraft.STEERING_MODES[2]:
            if self.tracked_target.current_epoch().value != self.current_epoch().value:
                self.tracked_target.step_to_epoch(self.current_epoch())
            self.body_z = self.target_vector(self.tracked_target)
            self.body_y = self.body_z.cross(self.sun_vector())
            self.body_x = self.body_y.cross(self.body_z)

        if self.slewing:
            if self.current_epoch().value > self.slew_stop.value:
                self.slewing = False

    def track_lvlh(self) -> None:
        if self.steering != Spacecraft.STEERING_MODES[0]:
            self.steering = Spacecraft.STEERING_MODES[0]
            self.tracked_target = None
            self.slewing = True 
            t:float = self.body_z.angle(self.position().scaled(-1))/(self.slew_rate*SECONDS_IN_DAY)
            self.slew_stop = self.current_epoch().plus_days(t)
            self.update_attitude()

    def track_sun(self) -> None:
        if self.steering != Spacecraft.STEERING_MODES[1]:
            self.steering = Spacecraft.STEERING_MODES[1]
            self.tracked_target = None
            self.slewing = True 
            self.slewing = True 
            t:float = self.body_z.angle(self.sun_vector().scaled(-1))/(self.slew_rate*SECONDS_IN_DAY)
            self.slew_stop = self.current_epoch().plus_days(t)
            self.update_attitude()

    def track_state(self, target:"Spacecraft") -> None:
        if self.steering != Spacecraft.STEERING_MODES[2]:
            self.steering = Spacecraft.STEERING_MODES[2]
            self.tracked_target = target
            self.slewing = True 
            self.slewing = True 
            t:float = self.body_z.angle(self.target_vector(target))/(self.slew_rate*SECONDS_IN_DAY)
            self.slew_stop = self.current_epoch().plus_days(t)
            self.update_attitude()

    def velocity(self) -> Vector3D:
        return self.propagator.state.velocity

    def detect(self, target:"Spacecraft") -> bool:
        success:bool = True
        if self.sun_angle(target) < self.wfov.limits.sun_soft:
            success = False
        elif self.earth_angle(target) < self.wfov.limits.earth:
            success = False
        elif self.moon_angle(target) < self.wfov.limits.moon:
            success = False
        elif self.visual_magnitude(target) > self.wfov.limits.vismag:
            success = False
        elif self.body_z.angle(self.target_vector(target)) > self.wfov.limits.bore:
            success = False
        return success

    def visual_magnitude(self, target:"Spacecraft") -> float:
        r:float = self.body_radius
        dist:float = self.range(target)
        phi:float = pi - self.sun_angle(target)
        fdiff:float = (2/3)*self.albedo*r*r/(pi*dist*dist)*((sin(phi) + (pi-phi)*cos(phi)))
        return -26.74 - 2.5*log10(fdiff)

    def sun_angle(self, target:"Spacecraft") -> float:
        return self.sun_vector().angle(self.target_vector(target))

    def moon_angle(self, target:"Spacecraft") -> float:
        return self.moon_vector().angle(self.target_vector(target))

    def earth_angle(self, target:"Spacecraft") -> float:
        return self.earth_vector().angle(self.target_vector(target))

    def range(self, target:"Spacecraft") -> float:
        return self.target_vector(target).magnitude()

    def position(self) -> Vector3D:
        return self.current_state().position.copy()

    def step(self) -> None:
        self.propagator.step()
        self.update_attitude()

    def step_to_epoch(self, epoch:Epoch) -> None:
        self.propagator.step_to_epoch(epoch)
        self.update_attitude()

    def sun_vector(self) -> Vector3D:
        return self.current_state().sun_vector()

    def moon_vector(self) -> Vector3D:
        return self.current_state().moon_vector()

    def earth_vector(self) -> Vector3D:
        return self.position().scaled(-1)

    def target_vector(self, target:"Spacecraft") -> Vector3D:
        return target.position().minus(self.position())

    def hill_position(self, target:"Spacecraft") -> Vector3D:
        return HillState.from_gcrf(target.current_state(), self.current_state()).position

    def current_state(self) -> "GCRFstate":
        return self.propagator.state.copy()

    def current_epoch(self) -> Epoch:
        return self.current_state().epoch.copy()