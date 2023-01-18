from openspace.math.linalg import Vector3D


class Velocity(Vector3D):
    def __init__(self, x: float, y: float, z: float) -> None:
        """class used to perform operations across various reference frames

        :param x: first component of velocity
        :type x: float
        :param y: second component of velocity
        :type y: float
        :param z: third component of velocity
        :type z: float
        """
        Vector3D.__init__(self, x, y, z)

    def copy(self) -> "Velocity":
        """create duplicate of calling velocity

        :return: copy of calling velocity
        :rtype: Velocity
        """
        return Velocity(self.x, self.y, self.z)
