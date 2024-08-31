from pysmad.coordinates import CartesianVector
from pysmad.math.linalg import Vector6D


class CartesianElements(Vector6D):
    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float) -> None:
        super().__init__(x, y, z, vx, vy, vz)
        self.position = CartesianVector(x, y, z)
        self.velocity = CartesianVector(vx, vy, vz)

    @property
    def x(self) -> float:
        return self[0]

    @property
    def y(self) -> float:
        return self[1]

    @property
    def z(self) -> float:
        return self[2]

    @property
    def vx(self) -> float:
        return self[3]

    @property
    def vy(self) -> float:
        return self[4]

    @property
    def vz(self) -> float:
        return self[5]

    @classmethod
    def from_position_and_velocity(cls, r: CartesianVector, v: CartesianVector) -> "CartesianElements":
        """Create a CartesianElements object from a position and velocity vector

        :param r: 3-D position vector
        :param v: 3-D velocity vector
        """
        return cls(r.x, r.y, r.z, v.x, v.y, v.z)
