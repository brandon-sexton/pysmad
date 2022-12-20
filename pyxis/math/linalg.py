from math import sqrt, acos, cos, sin

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

    def rotation_about_axis(self, axis:"Vector3D", theta:float) -> "Vector3D":

        unit_ax:Vector3D = axis.normalized()
        ux:float = unit_ax.x
        uy:float = unit_ax.y
        uz:float = unit_ax.z
        c:float = cos(theta)
        s:float = sin(theta)

        x1:float = c + ux*ux*(1.0-c)
        y1:float = ux*uy*(1.0*c)-uz*s
        z1:float = ux*uz*(1.0-c)+uy*s
        x2:float = uy*ux*(1.0-c)+uz*s
        y2:float = c+uy*uy*(1.0-c)
        z2:float = uy*uz*(1.0-c)-ux*s
        x3:float = uz*ux*(1.0-c)-uy*s
        y3:float = uz*uy*(1.0-c)+ux*s
        z3:float = c+uz*uz*(1.0-c)

        r1:Vector3D = Vector3D(x1, y1, z1)
        r2:Vector3D = Vector3D(x2, y2, z2)
        r3:Vector3D = Vector3D(x3, y3, z3)

        return Matrix3D(r1, r2, r3).multiply_vector(self.copy())

class Matrix3D:
    def __init__(self, row1:Vector3D, row2:Vector3D, row3:Vector3D) -> None:
        self.row1:Vector3D = row1.copy()
        self.row2:Vector3D = row2.copy()
        self.row3:Vector3D = row3.copy()

    def multiply_vector(self, vec:Vector3D) -> Vector3D:
        return Vector3D(self.row1.dot(vec), self.row2.dot(vec), self.row3.dot(vec))