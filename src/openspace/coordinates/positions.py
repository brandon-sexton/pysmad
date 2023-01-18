from openspace.math.linalg import Vector3D


class Position(Vector3D):
    def __init__(self, x: float, y: float, z: float) -> None:
        """class used to perform operations across various reference frames

        :param x: first component of position
        :type x: float
        :param y: second component of position
        :type y: float
        :param z: third component of position
        :type z: float
        """
        Vector3D.__init__(self, x, y, z)

    def copy(self) -> "Position":
        """create duplicate of calling position

        :return: copy of calling position
        :rtype: Position
        """
        return Position(self.x, self.y, self.z)
