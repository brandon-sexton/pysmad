from pysmad.constants import MJD_ZERO_JULIAN_DATE, SECONDS_TO_DAYS
from pysmad.eop import LeapSecondData


def test_get_record():
    leap_seconds = LeapSecondData("pysmad/eop/tai-utc.dat")
    int_mjd_zero = int(MJD_ZERO_JULIAN_DATE)

    # exact MJDs to test
    too_early_mjd = 2437300 - int_mjd_zero - 1
    mjd_jan_2017 = 2457754 - int_mjd_zero
    too_late_mjd = mjd_jan_2017 + 1
    mjd_dec_2016 = mjd_jan_2017 - 1

    assert leap_seconds.get_record(too_early_mjd) == 0
    assert leap_seconds.get_record(mjd_jan_2017) == 37 * SECONDS_TO_DAYS
    assert leap_seconds.get_record(too_late_mjd) == 37 * SECONDS_TO_DAYS
    assert leap_seconds.get_record(mjd_dec_2016) == 36 * SECONDS_TO_DAYS
