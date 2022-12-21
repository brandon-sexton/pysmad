from math import sqrt, acos, cos, sin

class Vector6D:
    def __init__(self, x:float, y:float, z:float, vx:float, vy:float, vz:float) -> None:
        self.x:float = x
        self.y:float = y
        self.z:float = z
        self.vx:float = vx
        self.vy:float = vy
        self.vz:float = vz

    @classmethod
    def from_position_and_velocity(cls, r:"Vector3D", v:"Vector3D") -> "Vector6D":
        return cls(r.x, r.y, r.z, v.x, v.y, v.z)

    def dot(self, vec_to_dot:"Vector6D") -> float:
        return self.x*vec_to_dot.x + self.y*vec_to_dot.y + self.z*vec_to_dot.z \
            + self.vx*vec_to_dot.vx + self.vy*vec_to_dot.vy + self.vz*vec_to_dot.vz

    def copy(self) -> "Vector6D":
        return Vector6D(self.x, self.y, self.z, self.vx, self.vy, self.vz)

class Vector3D:

    def __init__(self, x:float, y:float, z:float) -> None:
        self.x:float = x
        self.y:float = y
        self.z:float = z

    def copy(self) -> "Vector3D":
        return Vector3D(self.x, self.y, self.z)

    def plus(self, vec_to_add:"Vector3D") -> "Vector3D":
        return Vector3D(self.x + vec_to_add.x, self.y + vec_to_add.y, self.z + vec_to_add.z)

    def minus(self, vec_to_subtract:"Vector3D") -> "Vector3D":
        return Vector3D(self.x - vec_to_subtract.x, self.y - vec_to_subtract.y, self.z - vec_to_subtract.z)

    def dot(self, vec_to_dot:"Vector3D") -> float:
        return self.x*vec_to_dot.x + self.y*vec_to_dot.y + self.z*vec_to_dot.z

    def cross(self, vec_to_cross:"Vector3D") -> "Vector3D":
        return Vector3D(
            self.y*vec_to_cross.z - self.z*vec_to_cross.y, 
            self.z*vec_to_cross.x - self.x*vec_to_cross.z, 
            self.x*vec_to_cross.y - self.y*vec_to_cross.x
        )

    def magnitude(self) -> float:
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def scaled(self, scalar:float) -> "Vector3D":
        return Vector3D(self.x*scalar, self.y*scalar, self.z*scalar)

    def normalized(self) -> "Vector3D":
        return self.scaled(1/self.magnitude())

    def angle(self, adj_vec) -> float:
        return acos(self.dot(adj_vec)/(self.magnitude()*adj_vec.magnitude()))

    @staticmethod
    def rotation_matrix(axis:"Vector3D", theta:float) -> "Matrix3D":
        unit_ax:Vector3D = axis.normalized()
        ux:float = unit_ax.x
        uy:float = unit_ax.y
        uz:float = unit_ax.z
        c:float = cos(theta)
        s:float = sin(theta)
        cdiff:float = 1-c

        x1:float = c + ux*ux*cdiff
        y1:float = ux*uy*cdiff-uz*s
        z1:float = ux*uz*cdiff+uy*s
        x2:float = uy*ux*cdiff+uz*s
        y2:float = c+uy*uy*cdiff
        z2:float = uy*uz*cdiff-ux*s
        x3:float = uz*ux*cdiff-uy*s
        y3:float = uz*uy*cdiff+ux*s
        z3:float = c+uz*uz*cdiff

        r1:Vector3D = Vector3D(x1, y1, z1)
        r2:Vector3D = Vector3D(x2, y2, z2)
        r3:Vector3D = Vector3D(x3, y3, z3)
        
        return Matrix3D(r1, r2, r3)

    def rotation_about_axis(self, axis:"Vector3D", theta:float) -> "Vector3D":
        return Vector3D.rotation_matrix(axis, theta).multiply_vector(self.copy())

class Matrix3D:
    def __init__(self, row1:Vector3D, row2:Vector3D, row3:Vector3D) -> None:
        self.row1:Vector3D = row1.copy()
        self.row2:Vector3D = row2.copy()
        self.row3:Vector3D = row3.copy()

    def multiply_vector(self, vec:Vector3D) -> Vector3D:
        return Vector3D(self.row1.dot(vec), self.row2.dot(vec), self.row3.dot(vec))

    def transpose(self) -> "Matrix3D":
        return Matrix3D(
            Vector3D(self.row1.x, self.row2.x, self.row3.x),
            Vector3D(self.row1.y, self.row2.y, self.row3.y),
            Vector3D(self.row1.z, self.row2.z, self.row3.z)
        )

class Matrix6D:
    def __init__(self, r1:Vector6D, r2:Vector6D, r3:Vector6D, r4:Vector6D, r5:Vector6D, r6:Vector6D) -> None:
        self.row1:Vector6D = r1.copy()
        self.row2:Vector6D = r2.copy()
        self.row3:Vector6D = r3.copy()
        self.row4:Vector6D = r4.copy()
        self.row5:Vector6D = r5.copy()
        self.row6:Vector6D = r6.copy()

    def multiply_vector(self, vec:Vector6D) -> Vector6D:
        return Vector6D(
            self.row1.dot(vec),
            self.row2.dot(vec),
            self.row3.dot(vec),
            self.row4.dot(vec),
            self.row5.dot(vec),
            self.row6.dot(vec),
        )