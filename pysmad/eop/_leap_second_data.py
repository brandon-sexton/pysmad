from pathlib import Path

from pysmad.constants import MJD_ZERO_JULIAN_DATE, SECONDS_TO_DAYS


class LeapSecondData:
    def __init__(self, tai_utc_path: Path | str) -> None:
        """class used to interact with the leap second data files

        :param tai_utc_path: path to the tai-utc.dat file produced by USNO
        """
        self._records: list[list[int | float]] = []
        self.update_from_file(tai_utc_path)

    def update_from_file(self, file_path: Path | str) -> None:
        with open(file_path, "r") as f:
            lines = f.readlines()

        mjd_zero_int = int(MJD_ZERO_JULIAN_DATE)
        for line in lines:
            mjd = int(line[17:24]) - mjd_zero_int
            self._records.append([mjd, float(line[38:48]) * SECONDS_TO_DAYS])

    def get_record(self, mjd: float) -> float:
        # If the MJD is greater than the last record, return the last record
        if mjd >= self._records[-1][0]:
            leap_seconds = self._records[-1][1]

        # If the MJD is less than the first record, return 0
        elif mjd < self._records[0][0]:
            leap_seconds = 0

        # Otherwise, find the first record that is less than or equal to the MJD
        else:
            for record in self._records:
                if record[0] > mjd:
                    break
                leap_seconds = record[1]
        return leap_seconds
