from math import acos, cos, sin, sqrt


class Vector6D:
    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.vx: float = vx
        self.vy: float = vy
        self.vz: float = vz

    @classmethod
    def from_position_and_velocity(cls, r: "Vector3D", v: "Vector3D") -> "Vector6D":
        return cls(r.x, r.y, r.z, v.x, v.y, v.z)

    def __str__(self) -> str:
        return f"{self.x:.6f} {self.y:.6f} {self.z:.6f} {self.vx:.6f} {self.vy:.6f} {self.vz:.6f}"

    def dot(self, vec_to_dot: "Vector6D") -> float:
        return (
            self.x * vec_to_dot.x
            + self.y * vec_to_dot.y
            + self.z * vec_to_dot.z
            + self.vx * vec_to_dot.vx
            + self.vy * vec_to_dot.vy
            + self.vz * vec_to_dot.vz
        )

    def copy(self) -> "Vector6D":
        return Vector6D(self.x, self.y, self.z, self.vx, self.vy, self.vz)

    def plus(self, vec: "Vector6D") -> "Vector6D":
        return Vector6D(
            self.x + vec.x,
            self.y + vec.y,
            self.z + vec.z,
            self.vx + vec.vx,
            self.vy + vec.vy,
            self.vz + vec.vz,
        )

    def minus(self, vec: "Vector6D") -> "Vector6D":
        return Vector6D(
            self.x - vec.x,
            self.y - vec.y,
            self.z - vec.z,
            self.vx - vec.vx,
            self.vy - vec.vy,
            self.vz - vec.vz,
        )


class Vector3D:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __str__(self) -> str:
        return f"{self.x:.6f} {self.y:.6f} {self.z:.6f}"

    def copy(self) -> "Vector3D":
        return Vector3D(self.x, self.y, self.z)

    def plus(self, vec_to_add: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + vec_to_add.x, self.y + vec_to_add.y, self.z + vec_to_add.z)

    def minus(self, vec_to_subtract: "Vector3D") -> "Vector3D":
        return Vector3D(
            self.x - vec_to_subtract.x,
            self.y - vec_to_subtract.y,
            self.z - vec_to_subtract.z,
        )

    def dot(self, vec_to_dot: "Vector3D") -> float:
        return self.x * vec_to_dot.x + self.y * vec_to_dot.y + self.z * vec_to_dot.z

    def cross(self, vec_to_cross: "Vector3D") -> "Vector3D":
        return Vector3D(
            self.y * vec_to_cross.z - self.z * vec_to_cross.y,
            self.z * vec_to_cross.x - self.x * vec_to_cross.z,
            self.x * vec_to_cross.y - self.y * vec_to_cross.x,
        )

    def magnitude(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def scaled(self, scalar: float) -> "Vector3D":
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def normalized(self) -> "Vector3D":
        return self.scaled(1 / self.magnitude())

    def angle(self, adj_vec: "Vector3D") -> float:
        arg = self.dot(adj_vec) / (self.magnitude() * adj_vec.magnitude())
        if arg > 1:
            arg = 1
        elif arg < -1:
            arg = -1
        return acos(arg)

    @staticmethod
    def rotation_matrix(axis: "Vector3D", theta: float) -> "Matrix3D":
        unit_ax: Vector3D = axis.normalized()
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

        r1: Vector3D = Vector3D(x1, y1, z1)
        r2: Vector3D = Vector3D(x2, y2, z2)
        r3: Vector3D = Vector3D(x3, y3, z3)

        return Matrix3D(r1, r2, r3)

    def rotation_about_axis(self, axis: "Vector3D", theta: float) -> "Vector3D":
        return Vector3D.rotation_matrix(axis, theta).multiply_vector(self.copy())


class Matrix3D:
    def __init__(self, row1: Vector3D, row2: Vector3D, row3: Vector3D) -> None:
        self.row1: Vector3D = row1.copy()
        self.row2: Vector3D = row2.copy()
        self.row3: Vector3D = row3.copy()

    def diagonal(self) -> Vector3D:
        return Vector3D(self.row1.x, self.row2.y, self.row3.z)

    def column_1(self) -> Vector3D:
        return Vector3D(self.row1.x, self.row2.x, self.row3.x)

    def column_2(self) -> Vector3D:
        return Vector3D(self.row1.y, self.row2.y, self.row3.y)

    def column_3(self) -> Vector3D:
        return Vector3D(self.row1.z, self.row2.z, self.row3.z)

    def multiply_vector(self, vec: Vector3D) -> Vector3D:
        return Vector3D(self.row1.dot(vec), self.row2.dot(vec), self.row3.dot(vec))

    def scaled(self, scalar: float) -> "Matrix3D":
        return Matrix3D(self.row1.scaled(scalar), self.row2.scaled(scalar), self.row3.scaled(scalar))

    def transpose(self) -> "Matrix3D":
        return Matrix3D(
            Vector3D(self.row1.x, self.row2.x, self.row3.x),
            Vector3D(self.row1.y, self.row2.y, self.row3.y),
            Vector3D(self.row1.z, self.row2.z, self.row3.z),
        )

    def plus(self, mat: "Matrix3D") -> "Matrix3D":
        return Matrix3D(self.row1.plus(mat.row1), self.row2.plus(mat.row2), self.row3.plus(mat.row3))

    def determinant(self) -> float:

        return (
            self.row1.x * self.row2.y * self.row3.z
            + self.row1.y * self.row2.z * self.row3.x
            + self.row1.z * self.row2.x * self.row3.y
            - self.row1.z * self.row2.y * self.row3.x
            - self.row1.y * self.row2.x * self.row3.z
            - self.row1.x * self.row2.z * self.row3.y
        )

    def cofactor(self) -> "Matrix3D":
        return Matrix3D(
            Vector3D(
                self.row2.y * self.row3.z - self.row2.z * self.row3.y,
                -(self.row2.x * self.row3.z - self.row3.x * self.row2.z),
                self.row2.x * self.row3.y - self.row3.x * self.row2.y,
            ),
            Vector3D(
                -(self.row1.y * self.row3.z - self.row3.y * self.row1.z),
                self.row1.x * self.row3.z - self.row1.z * self.row3.x,
                -(self.row1.x * self.row3.y - self.row1.y * self.row3.x),
            ),
            Vector3D(
                self.row1.y * self.row2.z - self.row1.z * self.row2.y,
                -(self.row1.x * self.row2.z - self.row2.x * self.row1.z),
                self.row1.x * self.row2.y - self.row1.y * self.row2.x,
            ),
        )

    def adjugate(self) -> "Matrix3D":
        return self.cofactor().transpose()

    def inverse(self) -> "Matrix3D":
        return self.adjugate().scaled(1 / self.determinant())

    def multiply_matrix3by6(self, mat: "Matrix3by6") -> "Matrix3by6":
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
        self.row1: Vector6D = row1.copy()
        self.row2: Vector6D = row2.copy()
        self.row3: Vector6D = row3.copy()

    def column_1(self) -> Vector3D:
        return Vector3D(self.row1.x, self.row2.x, self.row3.x)

    def column_2(self) -> Vector3D:
        return Vector3D(self.row1.y, self.row2.y, self.row3.y)

    def column_3(self) -> Vector3D:
        return Vector3D(self.row1.z, self.row2.z, self.row3.z)

    def column_4(self) -> Vector3D:
        return Vector3D(self.row1.vx, self.row2.vx, self.row3.vx)

    def column_5(self) -> Vector3D:
        return Vector3D(self.row1.vy, self.row2.vy, self.row3.vy)

    def column_6(self) -> Vector3D:
        return Vector3D(self.row1.vz, self.row2.vz, self.row3.vz)

    def multiply_vector(self, vec: Vector6D) -> Vector3D:
        return Vector3D(self.row1.dot(vec), self.row2.dot(vec), self.row3.dot(vec))

    def transpose(self) -> "Matrix6by3":
        return Matrix6by3(
            self.column_1(),
            self.column_2(),
            self.column_3(),
            self.column_4(),
            self.column_5(),
            self.column_6(),
        )

    def multiply_matrix_6by3(self, mat: "Matrix6by3") -> Matrix3D:
        return Matrix3D(
            Vector3D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            Vector3D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            Vector3D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
        )


class Matrix6by3:
    def __init__(
        self,
        r1: Vector3D,
        r2: Vector3D,
        r3: Vector3D,
        r4: Vector3D,
        r5: Vector3D,
        r6: Vector3D,
    ) -> None:
        self.row1: Vector3D = r1.copy()
        self.row2: Vector3D = r2.copy()
        self.row3: Vector3D = r3.copy()
        self.row4: Vector3D = r4.copy()
        self.row5: Vector3D = r5.copy()
        self.row6: Vector3D = r6.copy()

    def column_1(self) -> Vector6D:
        return Vector6D(self.row1.x, self.row2.x, self.row3.x, self.row4.x, self.row5.x, self.row6.x)

    def column_2(self) -> Vector6D:
        return Vector6D(self.row1.y, self.row2.y, self.row3.y, self.row4.y, self.row5.y, self.row6.y)

    def column_3(self) -> Vector6D:
        return Vector6D(self.row1.z, self.row2.z, self.row3.z, self.row4.z, self.row5.z, self.row6.z)

    def transpose(self) -> Matrix3by6:
        return Matrix3by6(self.column_1(), self.column_2(), self.column_3())

    def multiply(self, mat: Matrix3D) -> "Matrix6by3":
        return Matrix6by3(
            Vector3D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            Vector3D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            Vector3D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
            Vector3D(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
            ),
            Vector3D(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
            ),
            Vector3D(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
            ),
        )

    def multiply_vector(self, vec: "Vector3D") -> Vector6D:
        return Vector6D(
            self.row1.dot(vec),
            self.row2.dot(vec),
            self.row3.dot(vec),
            self.row4.dot(vec),
            self.row5.dot(vec),
            self.row6.dot(vec),
        )

    def multiply_matrix3by6(self, mat: "Matrix3by6") -> "Matrix6D":
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
        self.row1: Vector6D = r1.copy()
        self.row2: Vector6D = r2.copy()
        self.row3: Vector6D = r3.copy()
        self.row4: Vector6D = r4.copy()
        self.row5: Vector6D = r5.copy()
        self.row6: Vector6D = r6.copy()

    @classmethod
    def identity(cls) -> "Matrix6D":
        return cls(
            Vector6D(1, 0, 0, 0, 0, 0),
            Vector6D(0, 1, 0, 0, 0, 0),
            Vector6D(0, 0, 1, 0, 0, 0),
            Vector6D(0, 0, 0, 1, 0, 0),
            Vector6D(0, 0, 0, 0, 1, 0),
            Vector6D(0, 0, 0, 0, 0, 1),
        )

    def diagonal(self) -> Vector6D:
        return Vector6D(
            self.row1.x,
            self.row2.y,
            self.row3.z,
            self.row4.vx,
            self.row5.vy,
            self.row6.vz,
        )

    def multiply_vector(self, vec: Vector6D) -> Vector6D:
        return Vector6D(
            self.row1.dot(vec),
            self.row2.dot(vec),
            self.row3.dot(vec),
            self.row4.dot(vec),
            self.row5.dot(vec),
            self.row6.dot(vec),
        )

    def column_1(self) -> Vector6D:
        return Vector6D(self.row1.x, self.row2.x, self.row3.x, self.row4.x, self.row5.x, self.row6.x)

    def column_2(self) -> Vector6D:
        return Vector6D(self.row1.y, self.row2.y, self.row3.y, self.row4.y, self.row5.y, self.row6.y)

    def column_3(self) -> Vector6D:
        return Vector6D(self.row1.z, self.row2.z, self.row3.z, self.row4.z, self.row5.z, self.row6.z)

    def column_4(self) -> Vector6D:
        return Vector6D(
            self.row1.vx,
            self.row2.vx,
            self.row3.vx,
            self.row4.vx,
            self.row5.vx,
            self.row6.vx,
        )

    def column_5(self) -> Vector6D:
        return Vector6D(
            self.row1.vy,
            self.row2.vy,
            self.row3.vy,
            self.row4.vy,
            self.row5.vy,
            self.row6.vy,
        )

    def column_6(self) -> Vector6D:
        return Vector6D(
            self.row1.vz,
            self.row2.vz,
            self.row3.vz,
            self.row4.vz,
            self.row5.vz,
            self.row6.vz,
        )

    def transpose(self) -> "Matrix6D":
        return Matrix6D(
            self.column_1(),
            self.column_2(),
            self.column_3(),
            self.column_4(),
            self.column_5(),
            self.column_6(),
        )

    def multiply_matrix_6by3(self, mat: Matrix6by3) -> Matrix6by3:
        return Matrix6by3(
            Vector3D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            Vector3D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            Vector3D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
            Vector3D(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
            ),
            Vector3D(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
            ),
            Vector3D(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
            ),
        )

    def multiply_matrix(self, mat: "Matrix6D") -> "Matrix6D":
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
        return Matrix6D(
            self.row1.plus(mat.row1),
            self.row2.plus(mat.row2),
            self.row3.plus(mat.row3),
            self.row4.plus(mat.row4),
            self.row5.plus(mat.row5),
            self.row6.plus(mat.row6),
        )

    def minus(self, mat: "Matrix6D") -> "Matrix6D":
        return Matrix6D(
            self.row1.minus(mat.row1),
            self.row2.minus(mat.row2),
            self.row3.minus(mat.row3),
            self.row4.minus(mat.row4),
            self.row5.minus(mat.row5),
            self.row6.minus(mat.row6),
        )
