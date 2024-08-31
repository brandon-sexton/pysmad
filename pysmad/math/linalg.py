from math import cos, sin

from pysmad.coordinates import CartesianVector


class Vector6D(list[float]):
    def __init__(self, el1: float, el2: float, el3: float, el4: float, el5: float, el6: float) -> None:
        """class used to perform operations on a vector that has 6 components

        :param el1: first component of the vector
        :param el2: second component of the vector
        :param el3: third component of the vector
        :param el4: fourth component of the vector
        :param el5: fifth component of the vector
        :param el6: sixth component of the vector
        """

        super().__init__([el1, el2, el3, el4, el5, el6])

    def dot(self, vec_to_dot: "Vector6D") -> float:
        """calculates the dot product of the two vectors

        :param vec_to_dot: the second vector to be used in the dot product
        :type vec_to_dot: Vector6D
        :return: sum of the element products
        :rtype: float
        """
        return (
            self[0] * vec_to_dot[0]
            + self[1] * vec_to_dot[1]
            + self[2] * vec_to_dot[2]
            + self[3] * vec_to_dot[3]
            + self[4] * vec_to_dot[4]
            + self[5] * vec_to_dot[5]
        )

    def copy(self) -> "Vector6D":
        """create a replica of the current vector

        :return: 6-D vector with components that match the calling vector
        :rtype: Vector6D
        """
        return Vector6D(*self[:])

    def plus(self, vec: "Vector6D") -> "Vector6D":
        """calculates the sum of the elements of the two vectors

        :param vec: second vector to be included in the sum
        :type vec: Vector6D
        :return: vector whose elements are sums of the calling and argument vector
        :rtype: Vector6D
        """
        return Vector6D(
            self[0] + vec[0],
            self[1] + vec[1],
            self[2] + vec[2],
            self[3] + vec[3],
            self[4] + vec[4],
            self[5] + vec[5],
        )

    def minus(self, vec: "Vector6D") -> "Vector6D":
        """calculates the difference of the elements of the two vectors

        :param vec: second vector to be included in the difference
        :type vec: Vector6D
        :return: vector whose elements are the difference of the calling and argument vector
        :rtype: Vector6D
        """
        return Vector6D(
            self[0] - vec[0],
            self[1] - vec[1],
            self[2] - vec[2],
            self[3] - vec[3],
            self[4] - vec[4],
            self[5] - vec[5],
        )


class Matrix3D:
    def __init__(self, row1: CartesianVector, row2: CartesianVector, row3: CartesianVector) -> None:
        """used to perform operations on a 3x3 matrix

        :param row1: first row of matrix
        :type row1: CartesianVector
        :param row2: second row of matrix
        :type row2: CartesianVector
        :param row3: third row of matrix
        :type row3: CartesianVector
        """
        #: first row of matrix
        self.row1: CartesianVector = row1.copy()

        #: second row of matrix
        self.row2: CartesianVector = row2.copy()

        #: third row of matrix
        self.row3: CartesianVector = row3.copy()

    @classmethod
    def rotation_matrix(cls, axis: "CartesianVector", theta: float) -> "Matrix3D":
        """calculates the rotation matrix required for a rotation

        :param axis: axis that will be used to rotate a vector around
        :type axis: CartesianVector
        :param theta: angle in radians the vector will be rotated
        :type theta: float
        :return: transition matrix that will rotate a vector
        :rtype: Matrix3D
        """
        unit_ax: CartesianVector = axis.normalized()
        ux: float = unit_ax.x
        uy: float = unit_ax.y
        uz: float = unit_ax.z
        c: float = cos(theta)
        s: float = sin(theta)
        cdiff: float = 1 - c

        x1: float = c + ux * ux * cdiff
        y1: float = ux * uy * cdiff - uz * s
        z1: float = ux * uz * cdiff + uy * s
        x2: float = uy * ux * cdiff + uz * s
        y2: float = c + uy * uy * cdiff
        z2: float = uy * uz * cdiff - ux * s
        x3: float = uz * ux * cdiff - uy * s
        y3: float = uz * uy * cdiff + ux * s
        z3: float = c + uz * uz * cdiff

        r1: CartesianVector = CartesianVector(x1, y1, z1)
        r2: CartesianVector = CartesianVector(x2, y2, z2)
        r3: CartesianVector = CartesianVector(x3, y3, z3)

        return cls(r1, r2, r3)

    def diagonal(self) -> CartesianVector:
        """creates a vector with components equal to the diagonal of the matrix

        :return: vector equal to (xx, yy, zz)
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1.x, self.row2.y, self.row3.z)

    def column_1(self) -> CartesianVector:
        """creates a vector with elements equal to the first column of the matrix

        :return: vector with elements equal to the first column of the matrix
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1.x, self.row2.x, self.row3.x)

    def column_2(self) -> CartesianVector:
        """creates a vector with elements equal to the second column of the matrix

        :return: vector with elements equal to the second column of the matrix
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1.y, self.row2.y, self.row3.y)

    def column_3(self) -> CartesianVector:
        """creates a vector with elements equal to the third column of the matrix

        :return: vector with elements equal to the third column of the matrix
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1.z, self.row2.z, self.row3.z)

    def multiply_vector(self, vec: CartesianVector) -> CartesianVector:
        """performs matrix multiplication of the calling matrix and the argument vector

        :param vec: vector to be used in the multiplication
        :type vec: CartesianVector
        :return: product of the matrix multiplication
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1.dot(vec), self.row2.dot(vec), self.row3.dot(vec))

    def scaled(self, scalar: float) -> "Matrix3D":
        """creates a matrix whose elements have been scaled by the argument

        :param scalar: multiple to be used in the scale
        :type scalar: float
        :return: matrix with elements equal to the original scaled by the multiple
        :rtype: Matrix3D
        """
        return Matrix3D(self.row1.scaled(scalar), self.row2.scaled(scalar), self.row3.scaled(scalar))

    def transpose(self) -> "Matrix3D":
        """creates a matrix whose rows are equal to the columns of the calling matrix

        :return: transposed matrix of the calling matrix
        :rtype: Matrix3D
        """
        return Matrix3D(
            CartesianVector(self.row1.x, self.row2.x, self.row3.x),
            CartesianVector(self.row1.y, self.row2.y, self.row3.y),
            CartesianVector(self.row1.z, self.row2.z, self.row3.z),
        )

    def plus(self, mat: "Matrix3D") -> "Matrix3D":
        """creates a matrix whose elements are equal to the sum of the calling and argument matrix

        :param mat: matrix to be used in the sum
        :type mat: Matrix3D
        :return: sum matrix
        :rtype: Matrix3D
        """
        return Matrix3D(self.row1.plus(mat.row1), self.row2.plus(mat.row2), self.row3.plus(mat.row3))

    def determinant(self) -> float:
        """calculate the determinant of the matrix

        :return: determinant
        :rtype: float
        """
        return (
            self.row1.x * self.row2.y * self.row3.z
            + self.row1.y * self.row2.z * self.row3.x
            + self.row1.z * self.row2.x * self.row3.y
            - self.row1.z * self.row2.y * self.row3.x
            - self.row1.y * self.row2.x * self.row3.z
            - self.row1.x * self.row2.z * self.row3.y
        )

    def cofactor(self) -> "Matrix3D":
        """create a matrix that is the cofactor of the calling matrix

        :return: cofactor matrix
        :rtype: Matrix3D
        """
        return Matrix3D(
            CartesianVector(
                self.row2.y * self.row3.z - self.row2.z * self.row3.y,
                -(self.row2.x * self.row3.z - self.row3.x * self.row2.z),
                self.row2.x * self.row3.y - self.row3.x * self.row2.y,
            ),
            CartesianVector(
                -(self.row1.y * self.row3.z - self.row3.y * self.row1.z),
                self.row1.x * self.row3.z - self.row1.z * self.row3.x,
                -(self.row1.x * self.row3.y - self.row1.y * self.row3.x),
            ),
            CartesianVector(
                self.row1.y * self.row2.z - self.row1.z * self.row2.y,
                -(self.row1.x * self.row2.z - self.row2.x * self.row1.z),
                self.row1.x * self.row2.y - self.row1.y * self.row2.x,
            ),
        )

    def adjugate(self) -> "Matrix3D":
        """create a matrix that is the adjugate of the calling matrix

        :return: adjugate matrix
        :rtype: Matrix3D
        """
        return self.cofactor().transpose()

    def inverse(self) -> "Matrix3D":
        """create a matrix that is the inverse of the calling matrix

        :return: inverse matrix
        :rtype: Matrix3D
        """
        return self.adjugate().scaled(1 / self.determinant())

    def multiply_matrix3by6(self, mat: "Matrix3by6") -> "Matrix3by6":
        """create a matrix that is the product of the calling 3x3 and an argument 3x6 matrix

        :param mat: 3x6 matrix to be used in the product
        :type mat: Matrix3by6
        :return: product matrix
        :rtype: Matrix3by6
        """
        return Matrix3by6(
            Vector6D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
                self.row1.dot(mat.column_4()),
                self.row1.dot(mat.column_5()),
                self.row1.dot(mat.column_6()),
            ),
            Vector6D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
                self.row2.dot(mat.column_4()),
                self.row2.dot(mat.column_5()),
                self.row2.dot(mat.column_6()),
            ),
            Vector6D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
                self.row3.dot(mat.column_4()),
                self.row3.dot(mat.column_5()),
                self.row3.dot(mat.column_6()),
            ),
        )


class Matrix3by6:
    def __init__(self, row1: Vector6D, row2: Vector6D, row3: Vector6D) -> None:
        """used to perform operations for a 3x6 matrix

        :param row1: first row of the matrix
        :type row1: Vector6D
        :param row2: second row of the matrix
        :type row2: Vector6D
        :param row3: third row of the matrix
        :type row3: Vector6D
        """
        self.row1: Vector6D = row1.copy()
        self.row2: Vector6D = row2.copy()
        self.row3: Vector6D = row3.copy()

    def column_1(self) -> CartesianVector:
        """create a vector whose elements are equal to the first column of the calling matrix

        :return: first column
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1[0], self.row2[0], self.row3[0])

    def column_2(self) -> CartesianVector:
        """create a vector whose elements are equal to the second column of the calling matrix

        :return: second column
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1[1], self.row2[1], self.row3[1])

    def column_3(self) -> CartesianVector:
        """create a vector whose elements are equal to the third column of the calling matrix

        :return: third column
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1[2], self.row2[2], self.row3[2])

    def column_4(self) -> CartesianVector:
        """create a vector whose elements are equal to the fourth column of the calling matrix

        :return: fourth column
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1[3], self.row2[3], self.row3[3])

    def column_5(self) -> CartesianVector:
        """create a vector whose elements are equal to the fifth column of the calling matrix

        :return: fifth column
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1[4], self.row2[4], self.row3[4])

    def column_6(self) -> CartesianVector:
        """create a vector whose elements are equal to the sixth column of the calling matrix

        :return: sixth column
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1[5], self.row2[5], self.row3[5])

    def multiply_vector(self, vec: Vector6D) -> CartesianVector:
        """create a vector that is the product of the calling matrix and the argument vector

        :param vec: vector to be used in the product
        :type vec: Vector6D
        :return: product vector
        :rtype: CartesianVector
        """
        return CartesianVector(self.row1.dot(vec), self.row2.dot(vec), self.row3.dot(vec))

    def transpose(self) -> "Matrix6by3":
        """create a matrix whose rows are equal to the columns of the calling matrix

        :return: the transpose of the calling matrix
        :rtype: Matrix6by3
        """
        return Matrix6by3(
            self.column_1(),
            self.column_2(),
            self.column_3(),
            self.column_4(),
            self.column_5(),
            self.column_6(),
        )

    def multiply_matrix_6by3(self, mat: "Matrix6by3") -> Matrix3D:
        """create a matrix equal to the product of the calling matrix and the argument matrix

        :param mat: matrix to be used in the product
        :type mat: Matrix6by3
        :return: product matrix
        :rtype: Matrix3D
        """
        return Matrix3D(
            CartesianVector(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
        )


class Matrix6by3:
    def __init__(
        self,
        r1: CartesianVector,
        r2: CartesianVector,
        r3: CartesianVector,
        r4: CartesianVector,
        r5: CartesianVector,
        r6: CartesianVector,
    ) -> None:
        """used to perform operations for a 6x3 matrix

        :param r1: first row of the matrix
        :type r1: CartesianVector
        :param r2: second row of the matrix
        :type r2: CartesianVector
        :param r3: third row of the matrix
        :type r3: CartesianVector
        :param r4: fourth row of the matrix
        :type r4: CartesianVector
        :param r5: fifth row of the matrix
        :type r5: CartesianVector
        :param r6: sixth row of the matrix
        :type r6: CartesianVector
        """
        #: first row of the matrix
        self.row1: CartesianVector = r1.copy()

        #: second row of the matrix
        self.row2: CartesianVector = r2.copy()

        #: third row of the matrix
        self.row3: CartesianVector = r3.copy()

        #: fourth row of the matrix
        self.row4: CartesianVector = r4.copy()

        #: fifth row of the matrix
        self.row5: CartesianVector = r5.copy()

        #: sixth row of the matrix
        self.row6: CartesianVector = r6.copy()

    def column_1(self) -> Vector6D:
        """create a vector whose elements equal the first column of the matrix

        :return: first column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.x, self.row2.x, self.row3.x, self.row4.x, self.row5.x, self.row6.x)

    def column_2(self) -> Vector6D:
        """create a vector whose elements equal the second column of the matrix

        :return: second column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.y, self.row2.y, self.row3.y, self.row4.y, self.row5.y, self.row6.y)

    def column_3(self) -> Vector6D:
        """create a vector whose elements equal the third column of the matrix

        :return: third column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.z, self.row2.z, self.row3.z, self.row4.z, self.row5.z, self.row6.z)

    def transpose(self) -> Matrix3by6:
        """create a matrix whose rows equal the columns of the calling matrix

        :return: transpose of the calling matrix
        :rtype: Matrix3by6
        """
        return Matrix3by6(self.column_1(), self.column_2(), self.column_3())

    def multiply(self, mat: Matrix3D) -> "Matrix6by3":
        """create a matrix that is the product of the calling and argument matrices

        :param mat: matrix to be used in the product
        :type mat: Matrix3D
        :return: product matrix
        :rtype: Matrix6by3
        """
        return Matrix6by3(
            CartesianVector(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
            ),
        )

    def multiply_vector(self, vec: "CartesianVector") -> Vector6D:
        """create a vector equal to the product of the calling matrix and the argument vector

        :param vec: vector to be used in the product
        :type vec: CartesianVector
        :return: product vector
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1.dot(vec),
            self.row2.dot(vec),
            self.row3.dot(vec),
            self.row4.dot(vec),
            self.row5.dot(vec),
            self.row6.dot(vec),
        )

    def multiply_matrix3by6(self, mat: "Matrix3by6") -> "Matrix6D":
        """create a matrix equal to the product of the calling and the argument matrices

        :param mat: matrix to be used in the product
        :type mat: Matrix3by6
        :return: product matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            Vector6D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
                self.row1.dot(mat.column_4()),
                self.row1.dot(mat.column_5()),
                self.row1.dot(mat.column_6()),
            ),
            Vector6D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
                self.row2.dot(mat.column_4()),
                self.row2.dot(mat.column_5()),
                self.row2.dot(mat.column_6()),
            ),
            Vector6D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
                self.row3.dot(mat.column_4()),
                self.row3.dot(mat.column_5()),
                self.row3.dot(mat.column_6()),
            ),
            Vector6D(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
                self.row4.dot(mat.column_4()),
                self.row4.dot(mat.column_5()),
                self.row4.dot(mat.column_6()),
            ),
            Vector6D(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
                self.row5.dot(mat.column_4()),
                self.row5.dot(mat.column_5()),
                self.row5.dot(mat.column_6()),
            ),
            Vector6D(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
                self.row6.dot(mat.column_4()),
                self.row6.dot(mat.column_5()),
                self.row6.dot(mat.column_6()),
            ),
        )


class Matrix6D:
    def __init__(
        self,
        r1: Vector6D,
        r2: Vector6D,
        r3: Vector6D,
        r4: Vector6D,
        r5: Vector6D,
        r6: Vector6D,
    ) -> None:
        """used to perform operations for a 6x6 matrix

        :param r1: first row of the matrix
        :type r1: Vector6D
        :param r2: second row of the matrix
        :type r2: Vector6D
        :param r3: third row of the matrix
        :type r3: Vector6D
        :param r4: fourth row of the matrix
        :type r4: Vector6D
        :param r5: fifth row of the matrix
        :type r5: Vector6D
        :param r6: sixth row of the matrix
        :type r6: Vector6D
        """
        #: first row of the matrix
        self.row1: Vector6D = r1.copy()

        #: second row of the matrix
        self.row2: Vector6D = r2.copy()

        #: third row of the matrix
        self.row3: Vector6D = r3.copy()

        #: fourth row of the matrix
        self.row4: Vector6D = r4.copy()

        #: fifth row of the matrix
        self.row5: Vector6D = r5.copy()

        #: sixth row of the matrix
        self.row6: Vector6D = r6.copy()

    @classmethod
    def identity(cls) -> "Matrix6D":
        """create a matrix with a diagonal with elements of 1 and off-diagonal elements of 0

        :return: the identity matrix
        :rtype: Matrix6D
        """
        return cls(
            Vector6D(1, 0, 0, 0, 0, 0),
            Vector6D(0, 1, 0, 0, 0, 0),
            Vector6D(0, 0, 1, 0, 0, 0),
            Vector6D(0, 0, 0, 1, 0, 0),
            Vector6D(0, 0, 0, 0, 1, 0),
            Vector6D(0, 0, 0, 0, 0, 1),
        )

    def diagonal(self) -> Vector6D:
        """create a vector whose elements are equal to the diagonal of the matrix

        :return: vector whose elements equal the diagonal
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1[0],
            self.row2[1],
            self.row3[2],
            self.row4[3],
            self.row5[4],
            self.row6[5],
        )

    def multiply_vector(self, vec: Vector6D) -> Vector6D:
        """create a vector equal to the product of the calling matrix and the argument vector

        :param vec: vector to be used in the product
        :type vec: Vector6D
        :return: product vector
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1.dot(vec),
            self.row2.dot(vec),
            self.row3.dot(vec),
            self.row4.dot(vec),
            self.row5.dot(vec),
            self.row6.dot(vec),
        )

    def column_1(self) -> Vector6D:
        """create a vector whose elements equal the first column of the matrix

        :return: first column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1[0], self.row2[0], self.row3[0], self.row4[0], self.row5[0], self.row6[0])

    def column_2(self) -> Vector6D:
        """create a vector whose elements equal the second column of the matrix

        :return: second column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1[1], self.row2[1], self.row3[1], self.row4[1], self.row5[1], self.row6[1])

    def column_3(self) -> Vector6D:
        """create a vector whose elements equal the third column of the matrix

        :return: third column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1[2], self.row2[2], self.row3[2], self.row4[2], self.row5[2], self.row6[2])

    def column_4(self) -> Vector6D:
        """create a vector whose elements equal the fourth column of the matrix

        :return: fourth column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1[3],
            self.row2[3],
            self.row3[3],
            self.row4[3],
            self.row5[3],
            self.row6[3],
        )

    def column_5(self) -> Vector6D:
        """create a vector whose elements equal the fifth column of the matrix

        :return: fifth column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1[4],
            self.row2[4],
            self.row3[4],
            self.row4[4],
            self.row5[4],
            self.row6[4],
        )

    def column_6(self) -> Vector6D:
        """create a vector whose elements equal the sixth column of the matrix

        :return: sixth column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1[5],
            self.row2[5],
            self.row3[5],
            self.row4[5],
            self.row5[5],
            self.row6[5],
        )

    def transpose(self) -> "Matrix6D":
        """create a matrix whose rows equal the columns of the calling matrix

        :return: transpose of the calling matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            self.column_1(),
            self.column_2(),
            self.column_3(),
            self.column_4(),
            self.column_5(),
            self.column_6(),
        )

    def multiply_matrix_6by3(self, mat: Matrix6by3) -> Matrix6by3:
        """create a matrix equal to the product of the calling and argument matrices

        :param mat: matrix to be used in the product
        :type mat: Matrix6by3
        :return: product matrix
        :rtype: Matrix6by3
        """
        return Matrix6by3(
            CartesianVector(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
            ),
            CartesianVector(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
            ),
        )

    def multiply_matrix(self, mat: "Matrix6D") -> "Matrix6D":
        """create a matrix equal to the product of the calling and the argument matrices

        :param mat: matrix to be used in the product
        :type mat: Matrix6D
        :return: product matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            Vector6D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
                self.row1.dot(mat.column_4()),
                self.row1.dot(mat.column_5()),
                self.row1.dot(mat.column_6()),
            ),
            Vector6D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
                self.row2.dot(mat.column_4()),
                self.row2.dot(mat.column_5()),
                self.row2.dot(mat.column_6()),
            ),
            Vector6D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
                self.row3.dot(mat.column_4()),
                self.row3.dot(mat.column_5()),
                self.row3.dot(mat.column_6()),
            ),
            Vector6D(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
                self.row4.dot(mat.column_4()),
                self.row4.dot(mat.column_5()),
                self.row4.dot(mat.column_6()),
            ),
            Vector6D(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
                self.row5.dot(mat.column_4()),
                self.row5.dot(mat.column_5()),
                self.row5.dot(mat.column_6()),
            ),
            Vector6D(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
                self.row6.dot(mat.column_4()),
                self.row6.dot(mat.column_5()),
                self.row6.dot(mat.column_6()),
            ),
        )

    def plus(self, mat: "Matrix6D") -> "Matrix6D":
        """create a matrix whose elements are equal to the sum of the elements in the calling and argument matrices

        :param mat: matrix to be used in the sum
        :type mat: Matrix6D
        :return: sum matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            self.row1.plus(mat.row1),
            self.row2.plus(mat.row2),
            self.row3.plus(mat.row3),
            self.row4.plus(mat.row4),
            self.row5.plus(mat.row5),
            self.row6.plus(mat.row6),
        )

    def minus(self, mat: "Matrix6D") -> "Matrix6D":
        """create a matrix whose elements are equal to the difference of the elements in the calling and argument
        matrices

        :param mat: matrix to be used in the difference
        :type mat: Matrix6D
        :return: difference matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            self.row1.minus(mat.row1),
            self.row2.minus(mat.row2),
            self.row3.minus(mat.row3),
            self.row4.minus(mat.row4),
            self.row5.minus(mat.row5),
            self.row6.minus(mat.row6),
        )
