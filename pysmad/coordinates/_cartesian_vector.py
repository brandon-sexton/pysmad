from math import acos, sqrt


class CartesianVector:
    def __init__(self, x: float, y: float, z: float) -> None:
        """class used to perform operations on a 3-dimension vector

        :param x: first component of the vector
        :type x: float
        :param y: second component of the vector
        :type y: float
        :param z: third component of the vector
        :type z: float
        """
        #: first component of the vector
        self.x: float = x

        #: second component of the vector
        self.y: float = y

        #: third component of the vector
        self.z: float = z

    @classmethod
    def x_axis(cls) -> "CartesianVector":
        """creates a vector pointing in the x-direction

        :return: 3-D vector with x-component equal to 1
        :rtype: CartesianVector
        """
        return cls(1, 0, 0)

    @classmethod
    def y_axis(cls) -> "CartesianVector":
        """creates a vector pointing in the y-direction

        :return: 3-D vector with y-component equal to 1
        :rtype: CartesianVector
        """
        return cls(0, 1, 0)

    @classmethod
    def z_axis(cls) -> "CartesianVector":
        """creates a vector pointing in the z-direction

        :return: 3-D vector with z-component equal to 1
        :rtype: CartesianVector
        """
        return cls(0, 0, 1)

    def copy(self) -> "CartesianVector":
        """creates a replica of the vector

        :return: 3-D vector with elements equal to the calling vector
        :rtype: CartesianVector
        """
        return CartesianVector(self.x, self.y, self.z)

    def plus(self, vec_to_add: "CartesianVector") -> "CartesianVector":
        """creates a vector whose elements equal the sum of the calling and argument vector

        :param vec_to_add: vector to be included in the sum
        :type vec_to_add: CartesianVector
        :return: vector with elements equal to the sum of the calling and argument vector
        :rtype: CartesianVector
        """
        return CartesianVector(self.x + vec_to_add.x, self.y + vec_to_add.y, self.z + vec_to_add.z)

    def minus(self, vec_to_subtract: "CartesianVector") -> "CartesianVector":
        """creates a vector whose elements equal the difference of the calling and argument vector

        :param vec_to_subtract: vector to be included in the difference
        :type vec_to_subtract: CartesianVector
        :return: vector with elements equal to the difference of the calling and argument vector
        :rtype: CartesianVector
        """
        return CartesianVector(
            self.x - vec_to_subtract.x,
            self.y - vec_to_subtract.y,
            self.z - vec_to_subtract.z,
        )

    def dot(self, vec_to_dot: "CartesianVector") -> float:
        """calculates the dot product of the two vectors

        :param vec_to_dot: the second vector to be used in the dot product
        :type vec_to_dot: CartesianVector
        :return: sum of the element products
        :rtype: float
        """
        return self.x * vec_to_dot.x + self.y * vec_to_dot.y + self.z * vec_to_dot.z

    def cross(self, vec_to_cross: "CartesianVector") -> "CartesianVector":
        """creates a vector orthogonal to the calling and argument vector

        :param vec_to_cross: vector which will be used to complete the right-hand rule
        :type vec_to_cross: CartesianVector
        :return: vector produced using the right-hand rule that is orthogonal to the original vectors
        :rtype: CartesianVector
        """
        return CartesianVector(
            self.y * vec_to_cross.z - self.z * vec_to_cross.y,
            self.z * vec_to_cross.x - self.x * vec_to_cross.z,
            self.x * vec_to_cross.y - self.y * vec_to_cross.x,
        )

    def magnitude(self) -> float:
        """calculates the length of the vector

        :return: square root of the sum of squares
        :rtype: float
        """
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def scaled(self, scalar: float) -> "CartesianVector":
        """creates a scaled copy of the calling vector

        :param scalar: value that will be multiplied against all elements
        :type scalar: float
        :return: vector equal to the calling vector scaled by the argument
        :rtype: CartesianVector
        """
        return CartesianVector(self.x * scalar, self.y * scalar, self.z * scalar)

    def normalized(self) -> "CartesianVector":
        """creates a vector parallel to the calling vector that is of length 1

        :return: unit vector of the calling vector
        :rtype: CartesianVector
        """
        return self.scaled(1 / self.magnitude())

    def angle(self, adj_vec: "CartesianVector") -> float:
        """calculates the angle between two vectors

        :param adj_vec: second leg of the angle
        :type adj_vec: CartesianVector
        :return: angle in radians between the two vectors
        :rtype: float
        """
        arg = self.dot(adj_vec) / (self.magnitude() * adj_vec.magnitude())
        if arg > 1:
            arg = 1
        elif arg < -1:
            arg = -1
        return acos(arg)
