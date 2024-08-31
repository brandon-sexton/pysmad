from pysmad.math import EquationsOfMotion


def test_from_e_ea():
    e = 0.83285
    ea = 0.6095079699392008
    assert EquationsOfMotion.mean_anomaly.from_ea_e(ea, e) == 0.1327312448297558
