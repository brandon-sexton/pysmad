from pysmad.bodies import Moon
from pysmad.coordinates import CartesianVector
from pysmad.time import Epoch


def test_get_position():

    epoch = Epoch.from_datetime_components(2022, 2, 25, 0, 0, 0)
    expected = CartesianVector(-6.454159844478600e4, -3.280761448809440e5, -1.566863311585961e5)

    moon_pos = Moon.get_position(epoch)
    # assert moon_pos.magnitude() / expected.magnitude() == 1
    assert moon_pos.angle(expected) == 0
