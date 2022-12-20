import unittest

from pyxis.math.linalg import Vector3D

class TestVector3D(unittest.TestCase):

    VEC_1 = Vector3D(4, 2, 42)
    VEC_2 = Vector3D(4, 42, 2)

    def test_plus(self):
        vec_sum = self.VEC_1.plus(self.VEC_2)
        self.assertAlmostEqual(vec_sum.x, 8)
        self.assertAlmostEqual(vec_sum.y, 44)
        self.assertAlmostEqual(vec_sum.z, 44)

    def test_minus(self):
        vec_diff = self.VEC_1.minus(self.VEC_2)
        self.assertAlmostEqual(vec_diff.x, 0)
        self.assertAlmostEqual(vec_diff.y, -40)
        self.assertAlmostEqual(vec_diff.z, 40)

    def test_dot(self):
        vec_dot = self.VEC_1.dot(self.VEC_2)
        self.assertAlmostEqual(vec_dot, 184)

    def test_cross(self):
        vec_cross = self.VEC_1.cross(self.VEC_2)
        self.assertAlmostEqual(vec_cross.x, -1760)
        self.assertAlmostEqual(vec_cross.y, 160)
        self.assertAlmostEqual(vec_cross.z, 160)

    def test_magnitude(self):
        self.assertAlmostEqual(self.VEC_1.magnitude(), 42.23742416388575)
        self.assertAlmostEqual(self.VEC_2.magnitude(), 42.23742416388575)

    def test_scaled(self):
        vec_scaled = self.VEC_1.scaled(2)
        self.assertAlmostEqual(vec_scaled.x, 8)
        self.assertAlmostEqual(vec_scaled.y, 4)
        self.assertAlmostEqual(vec_scaled.z, 84)

    def test_normalized(self):
        vec_normed = self.VEC_1.normalized()
        self.assertAlmostEqual(vec_normed.x, .0947027447620757)
        self.assertAlmostEqual(vec_normed.y, .0473513723810378)
        self.assertAlmostEqual(vec_normed.z, .9943788200017946)

