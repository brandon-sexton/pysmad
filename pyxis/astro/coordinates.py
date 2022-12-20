from typing import List

from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch
from pyxis.astro.bodies.celestial import Sun, Earth, Moon

class GCRFstate:
    def __init__(self, epoch:Epoch, position:Vector3D, velocity:Vector3D) -> None:
        self.epoch:Epoch = epoch.copy()
        self.position:Vector3D = position.copy()
        self.velocity:Vector3D = velocity.copy()

    def copy(self) -> "GCRFstate":
        return GCRFstate(self.epoch, self.position, self.velocity)

    def vector_list(self) -> List[Vector3D]:
        return [self.position.copy(), self.velocity.copy()]

    def acceleration_from_earth(self) -> Vector3D:
        r_mag:float = self.position.magnitude()
        return self.position.scaled(-Earth.MU/(r_mag*r_mag*r_mag))

    def acceleration_from_moon(self) -> Vector3D:
        s:Vector3D = Moon.get_position(self.epoch)
        r:Vector3D = s.minus(self.position)
        r_mag:float = r.magnitude()
        s_mag:float = s.magnitude()
        vec_1:Vector3D = r.scaled(1/(r_mag*r_mag*r_mag))
        vec_2:Vector3D = s.scaled(1/(s_mag*s_mag*s_mag))
        return vec_1.minus(vec_2).scaled(Moon.MU)

    def acceleration_from_sun(self) -> Vector3D:
        s:Vector3D = Sun.get_position(self.epoch)
        r:Vector3D = s.minus(self.position)
        r_mag:float = r.magnitude()
        s_mag:float = s.magnitude()
        vec_1:Vector3D = r.scaled(1/(r_mag*r_mag*r_mag))
        vec_2:Vector3D = s.scaled(1/(s_mag*s_mag*s_mag))
        return vec_1.minus(vec_2).scaled(Sun.MU)

    def acceleration_from_srp(self) -> Vector3D:
        sun_vec:Vector3D = self.sun_vector().normalized()
        return sun_vec.scaled(-Sun.P*3.6e-5)

    def derivative(self) -> List[Vector3D]:
        net_0 = Vector3D(0, 0, 0)
        net_1 = net_0.plus(self.acceleration_from_moon())
        net_2 = net_1.plus(self.acceleration_from_sun())
        net_3 = net_2.plus(self.acceleration_from_srp())
        net_a = net_3.plus(self.acceleration_from_earth())
        return [self.velocity.copy(), net_a]

    def sun_vector(self) -> Vector3D:
        return Sun.get_position(self.epoch).minus(self.position)

    def moon_vector(self) -> Vector3D:
        return Moon.get_position(self.epoch).minus(self.position)
