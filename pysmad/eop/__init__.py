from pathlib import Path

from pysmad.eop._polar_motion_record import PolarMotionRecord
from pysmad.eop._nutation_delta_record import NutationDeltaRecord
from pysmad.eop._time_delta_record import TimeDeltaRecord
from pysmad.eop._leap_second_data import LeapSecondData
from pysmad.eop._eop_record import EOPRecord
from pysmad.eop._eop_data import EOPData

module_dir = Path(__file__).parent
EOPData.load_files(module_dir / "finals.all", module_dir / "tai-utc.dat")

__all__ = ["EOPRecord", "LeapSecondData", "EOPData", "TimeDeltaRecord", "PolarMotionRecord", "NutationDeltaRecord"]
