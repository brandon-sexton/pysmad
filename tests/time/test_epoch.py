import pytest

from pysmad.constants import SECONDS_TO_DAYS
from pysmad.time import Epoch


@pytest.fixture
def epoch():
    return Epoch.from_datetime_components(2022, 12, 19, 12, 0, 0)


def test_utc(epoch):
    assert epoch.utc == 59932.5


def test_tai(epoch):
    assert epoch.tai == 59932.5 + 37 * SECONDS_TO_DAYS


def test_tt(epoch):
    assert epoch.tt == 59932.5 + 69.184 * SECONDS_TO_DAYS


def test_ut1(epoch):
    assert epoch.ut1 == 59932.5 - 0.01788165 * SECONDS_TO_DAYS


def test_mjd_to_jd(epoch):
    assert Epoch.mjd_to_jd(epoch.utc) == 2459933.0
