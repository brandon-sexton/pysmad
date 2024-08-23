from pathlib import Path

from pysmad.eop._eop_record import EOPRecord
from pysmad.eop._leap_second_data import LeapSecondData
from pysmad.eop._nutation_delta_record import NutationDeltaRecord
from pysmad.eop._polar_motion_record import PolarMotionRecord
from pysmad.eop._time_delta_record import TimeDeltaRecord


class EOPData:

    MINIMUM_FINALS_LINE_LENGTH = 134

    _records: dict[int | float, EOPRecord] = {}
    records_start: int | float | None = None
    records_end: int | float | None = None

    @staticmethod
    def load_files(finals_path: Path | str, tai_utc_path: Path | str) -> None:

        leap_seconds = LeapSecondData(tai_utc_path)
        with open(finals_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            if len(line.strip()) < EOPData.MINIMUM_FINALS_LINE_LENGTH:
                break
            record = EOPRecord.from_finals_line(line, leap_seconds)
            EOPData._records[record.mjd] = record

        EOPData.records_start = min(EOPData._records.keys())
        EOPData.records_end = max(EOPData._records.keys())

    @staticmethod
    def get_record(mjd: float) -> EOPRecord:
        """get a record from the data

        :param mjd: modified julian day of the record
        :return: record from the data
        """

        if EOPData.records_start is None or EOPData.records_end is None:
            record = EOPRecord.empty_record(0)
        elif mjd < EOPData.records_start:
            record = EOPData.get_record(EOPData.records_start)
        elif mjd > EOPData.records_end:
            record = EOPData.get_record(EOPData.records_end)
        else:
            mjd_floor = int(mjd)
            mjd_ceiling = mjd_floor + 1
            r_1: EOPRecord = EOPData._records[mjd_floor]
            r_2: EOPRecord = EOPData._records[mjd_ceiling]

            # interpolate time delta
            frac = mjd - mjd_floor
            ut1_utc = r_1.time_delta.ut1_utc + frac * (r_2.time_delta.ut1_utc - r_1.time_delta.ut1_utc)
            ut1_error = r_1.time_delta.ut1_error + frac * (r_2.time_delta.ut1_error - r_1.time_delta.ut1_error)
            tai_utc = r_1.time_delta.tai_utc + frac * (r_2.time_delta.tai_utc - r_1.time_delta.tai_utc)
            td = TimeDeltaRecord(ut1_utc, tai_utc, ut1_error)

            # interpolate polar motion
            x = r_1.polar_motion.x + frac * (r_2.polar_motion.x - r_1.polar_motion.x)
            x_error = r_1.polar_motion.x_error + frac * (r_2.polar_motion.x_error - r_1.polar_motion.x_error)
            y = r_1.polar_motion.y + frac * (r_2.polar_motion.y - r_1.polar_motion.y)
            y_error = r_1.polar_motion.y_error + frac * (r_2.polar_motion.y_error - r_1.polar_motion.y_error)
            pm = PolarMotionRecord(x, y, x_error, y_error)

            # interpolate nutation delta
            psi = r_1.nutation_delta.psi + frac * (r_2.nutation_delta.psi - r_1.nutation_delta.psi)
            psi_e = r_1.nutation_delta.psi_error + frac * (r_2.nutation_delta.psi_error - r_1.nutation_delta.psi_error)
            eps = r_1.nutation_delta.epsilon + frac * (r_2.nutation_delta.epsilon - r_1.nutation_delta.epsilon)
            eps_e = r_1.nutation_delta.epsilon_error + frac * (
                r_2.nutation_delta.epsilon_error - r_1.nutation_delta.epsilon_error
            )
            nd = NutationDeltaRecord(psi, eps, psi_e, eps_e)

            record = EOPRecord(mjd, td, pm, nd)

        return record
