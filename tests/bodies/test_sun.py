from pysmad.bodies import Sun
from pysmad.math.linalg import Vector3D
from pysmad.time import Epoch


def test_get_position():
    epoch = Epoch.from_datetime_components(2022, 2, 25, 0, 0, 0)
    expected = Vector3D(1.353158384133262e8, -5.514968448042840e7, -2.390803633125914e7)

    sun_pos = Sun.get_position(epoch)
    assert sun_pos.magnitude() / expected.magnitude() == 1
    assert sun_pos.angle(expected) == 0
