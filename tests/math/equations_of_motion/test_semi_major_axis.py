from pysmad.math import EquationsOfMotion


def test_from_p_e():
    p = 11067.79
    e = 0.83285
    assert EquationsOfMotion.semi_major_axis.from_p_e(p, e) == 36126.64283480516
