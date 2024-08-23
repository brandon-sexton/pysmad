from pysmad import RESOURCE_DIR
from pysmad.eop._eop_data import EOPData
from pysmad.eop._eop_record import EOPRecord
from pysmad.eop._leap_second_data import LeapSecondData
from pysmad.eop._time_delta_record import TimeDeltaRecord

EOPData.load_files(RESOURCE_DIR / "finals.all", RESOURCE_DIR / "tai-utc.dat")

__all__ = ["EOPRecord", "LeapSecondData", "EOPData", "TimeDeltaRecord"]
