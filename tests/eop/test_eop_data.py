from pysmad.constants import ARC_SECONDS_TO_RADIANS, MILLI_TO_BASE, SECONDS_TO_DAYS
from pysmad.eop import EOPData


def test_get_record():
    EOPData.load_files("pysmad/eop/finals.all", "pysmad/eop/tai-utc.dat")
    record = EOPData.get_record(57630)
    assert record.mjd == 57630
    assert record.time_delta.ut1_utc == -0.2449597 * SECONDS_TO_DAYS
    assert record.time_delta.ut1_error == 0.0000092 * SECONDS_TO_DAYS
    assert record.time_delta.tai_utc == 36 * SECONDS_TO_DAYS
    assert record.polar_motion.x == 0.235397 * ARC_SECONDS_TO_RADIANS
    assert record.polar_motion.x_error == 0.000019 * ARC_SECONDS_TO_RADIANS
    assert record.polar_motion.y == 0.393347 * ARC_SECONDS_TO_RADIANS
    assert record.polar_motion.y_error == 0.000025 * ARC_SECONDS_TO_RADIANS
    assert record.nutation_delta.psi == -105.883 * MILLI_TO_BASE * ARC_SECONDS_TO_RADIANS
    assert record.nutation_delta.psi_error == 0.300 * MILLI_TO_BASE * ARC_SECONDS_TO_RADIANS
    assert record.nutation_delta.epsilon == -13.437 * MILLI_TO_BASE * ARC_SECONDS_TO_RADIANS
    assert record.nutation_delta.epsilon_error == 0.030 * MILLI_TO_BASE * ARC_SECONDS_TO_RADIANS
    assert not record.is_empty
