from pysmad.constants import ARC_SECONDS_TO_RADIANS, MILLI_TO_BASE, SECONDS_TO_DAYS
from pysmad.eop._leap_second_data import LeapSecondData
from pysmad.eop._nutation_delta_record import NutationDeltaRecord
from pysmad.eop._polar_motion_record import PolarMotionRecord
from pysmad.eop._time_delta_record import TimeDeltaRecord


class EOPRecord:
    def __init__(self, mjd: int | float, td: TimeDeltaRecord, pm: PolarMotionRecord, nd: NutationDeltaRecord) -> None:
        self.mjd: int | float = mjd
        self.time_delta: TimeDeltaRecord = td
        self.polar_motion: PolarMotionRecord = pm
        self.nutation_delta: NutationDeltaRecord = nd
        self.is_empty: bool = False

    @classmethod
    def empty_record(cls, mjd: int | float) -> "EOPRecord":
        """create a null record

        :param mjd: modified julian day of the record
        """
        record = cls(mjd, TimeDeltaRecord(0, 0, 0), PolarMotionRecord(0, 0, 0, 0), NutationDeltaRecord(0, 0, 0, 0))
        record.is_empty = True
        return record

    @classmethod
    def from_finals_line(cls, line: str, ls: LeapSecondData) -> "EOPRecord":
        """class used to interact with a line from the finals data files

        The format of the finals.data, finals.daily, and finals.all files is:

        .. code-block:: none

        Col.#    Format  Quantity
        -------  ------  -------------------------------------------------------------
        1-2      I2      year (to get true calendar year, add 1900 for MJD<=51543 or add 2000 for MJD>=51544)
        3-4      I2      month number
        5-6      I2      day of month
        7        X       [blank]
        8-15     F8.2    fractional Modified Julian Date (MJD UTC)
        16       X       [blank]
        17       A1      IERS (I) or Prediction (P) flag for Bull. A polar motion values
        18       X       [blank]
        19-27    F9.6    Bull. A PM-x (sec. of arc)
        28-36    F9.6    error in PM-x (sec. of arc)
        37       X       [blank]
        38-46    F9.6    Bull. A PM-y (sec. of arc)
        47-55    F9.6    error in PM-y (sec. of arc)
        56-57    2X      [blanks]
        58       A1      IERS (I) or Prediction (P) flag for Bull. A UT1-UTC values
        59-68    F10.7   Bull. A UT1-UTC (sec. of time)
        69-78    F10.7   error in UT1-UTC (sec. of time)
        79       X       [blank]
        80-86    F7.4    Bull. A LOD (msec. of time) -- NOT ALWAYS FILLED
        87-93    F7.4    error in LOD (msec. of time) -- NOT ALWAYS FILLED
        94-95    2X      [blanks]
        96       A1      IERS (I) or Prediction (P) flag for Bull. A nutation values
        97       X       [blank]
        98-106   F9.3    Bull. A dPSI (msec. of arc)
        107-115  F9.3    error in dPSI (msec. of arc)
        116      X       [blank]
        117-125  F9.3    Bull. A dEPSILON (msec. of arc)
        126-134  F9.3    error in dEPSILON (msec. of arc)
        135-144  F10.6   Bull. B PM-x (sec. of arc)
        145-154  F10.6   Bull. B PM-y (sec. of arc)
        155-165  F11.7   Bull. B UT1-UTC (sec. of time)
        166-175  F10.3   Bull. B dPSI (msec. of arc)
        176-185  F10.3   Bull. B dEPSILON (msec. of arc)

        :param line: line from the finals data files
        """

        mjd = int(line[7:12].strip())
        ut1_utc: float = float(line[58:68].strip()) * SECONDS_TO_DAYS
        ut1_utc_error: float = float(line[68:78].strip()) * SECONDS_TO_DAYS
        polar_x: float = float(line[18:27].strip()) * ARC_SECONDS_TO_RADIANS
        polar_x_error: float = float(line[27:36].strip()) * ARC_SECONDS_TO_RADIANS
        polar_y: float = float(line[37:46].strip()) * ARC_SECONDS_TO_RADIANS
        polar_y_error: float = float(line[46:55].strip()) * ARC_SECONDS_TO_RADIANS
        delta_psi: float = float(line[97:106].strip()) * MILLI_TO_BASE * ARC_SECONDS_TO_RADIANS
        delta_psi_error: float = float(line[106:115].strip()) * MILLI_TO_BASE * ARC_SECONDS_TO_RADIANS
        delta_epsilon: float = float(line[116:125].strip()) * MILLI_TO_BASE * ARC_SECONDS_TO_RADIANS
        delta_epsilon_error: float = float(line[125:134].strip()) * MILLI_TO_BASE * ARC_SECONDS_TO_RADIANS

        time_record = TimeDeltaRecord(ut1_utc, ls.get_record(mjd), ut1_utc_error)
        polar_record = PolarMotionRecord(polar_x, polar_y, polar_x_error, polar_y_error)
        nutation_record = NutationDeltaRecord(delta_psi, delta_epsilon, delta_psi_error, delta_epsilon_error)

        return cls(mjd, time_record, polar_record, nutation_record)
