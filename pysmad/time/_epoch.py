from datetime import datetime, timedelta, timezone
from math import floor, modf, radians, trunc

from pysmad.constants import DAYS_TO_JULIAN_CENTURY, J2000_JULIAN_DATE, MJD_ZERO_JULIAN_DATE, TAI_TO_TT
from pysmad.eop import EOPData
from pysmad.math.functions import Conversions


class Epoch:
    def __init__(self, utc_mjd: float) -> None:
        """class used to represent time

        :param utc_mjd: time in modified julian days
        :type utc_mjd: float
        """
        self.utc = utc_mjd

    @property
    def tai(self) -> float:
        return self.utc + EOPData.get_record(self.utc).time_delta.tai_utc

    @property
    def ut1(self) -> float:
        return self.utc + EOPData.get_record(self.utc).time_delta.ut1_utc

    @property
    def tt(self) -> float:
        return self.tai + TAI_TO_TT

    @property
    def iso_string(self) -> str:
        jd = Epoch.mjd_to_jd(self.utc) + 0.5

        jd_frac, jd_int = modf(jd)
        jd_int = int(jd_int)

        exp_a = trunc((jd_int - 1867216.25) / 36524.25)

        if jd_int > 2299160:
            exp_b = jd_int + 1 + exp_a - trunc(exp_a / 4.0)
        else:
            exp_b = jd_int

        exp_c = exp_b + 1524

        exp_d = trunc((exp_c - 122.1) / 365.25)

        exp_e = trunc(365.25 * exp_d)

        exp_g = trunc((exp_c - exp_e) / 30.6001)

        day = exp_c - exp_e + jd_frac - trunc(30.6001 * exp_g)

        if exp_g < 13.5:
            month = exp_g - 1
        else:
            month = exp_g - 13

        if month > 2.5:
            year = exp_d - 4716
        else:
            year = exp_d - 4715

        frac_days, day = modf(day)

        day = int(day)

        hours = frac_days * 24.0
        hours, hour = modf(hours)

        mins = hours * 60.0
        mins, min = modf(mins)

        secs = mins * 60.0

        return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{min:02d}:{secs:02.6f}Z"

    @staticmethod
    def mjd_to_jd(mjd: float) -> float:
        return mjd + MJD_ZERO_JULIAN_DATE

    def copy(self) -> "Epoch":
        """used to create a copy of the current epoch

        :return: a replica of the calling epoch
        """
        return Epoch(self.utc)

    @classmethod
    def from_current_utc(cls):
        return cls.from_datetime(datetime.now(timezone.utc))

    @classmethod
    def from_current_utc_delta(cls, delta_days: float):
        return cls.from_datetime(datetime.now(timezone.utc) - timedelta(delta_days))

    @classmethod
    def from_datetime(cls, dt: datetime):
        return cls.from_iso_string("".join([str(dt).replace(" ", "T"), "Z"]))

    @classmethod
    def from_datetime_components(cls, year: int, month: int, day: int, hour: int, minute: int, sec: float) -> "Epoch":
        """instantiate an epoch from the standard calendar format

        :param year: 4-digit year
        :type year: int
        :param month: 2-digit month
        :type month: int
        :param day: 2-digit day
        :type day: int
        :param hour: 2-digit hour
        :type hour: int
        :param minute: 2-digit minute
        :type minute: int
        :param sec: 2-digit and trailing decimal second
        :type sec: float
        :return: epoch with an mjd value equivalent to the corresponding calendar date
        :rtype: Epoch
        """
        y = year
        m = month
        d = day

        if m <= 2:
            y -= 1
            m += 12

        b = floor(y / 400) - floor(y / 100) + floor(y / 4)
        mjd = 365 * y - 679004 + b + floor(30.6001 * (m + 1)) + d

        return cls(mjd + Conversions.hms_to_decimal_day(hour, minute, sec))

    @classmethod
    def from_iso_string(cls, udl_date: str) -> "Epoch":
        """create an Epoch from a string in the standard format for the UDL

        :param udl_date: string representing the UDL epoch
        :type udl_date: str
        :return: Epoch representing the UDL time
        :rtype: Epoch
        """
        date_str = udl_date.split("T")[0]
        date_vals = date_str.split("-")
        yr = int(date_vals[0])
        mon = int(date_vals[1])
        day = int(date_vals[2])

        time_str = udl_date.split("T")[1]
        time_vals = time_str.split(":")
        hr = int(time_vals[0])
        min = int(time_vals[1])
        sec = float(time_vals[2].replace("Z", ""))

        return cls.from_datetime_components(yr, mon, day, hr, min, sec)

    def to_datetime(self):
        return datetime.strptime(self.iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def julian_centuries_past_j2000(mjd: float) -> float:
        """calculate the number of julian centuries that have elapsed since the j2000 epoch

        :return: number of julian centuries past the j2000 epoch
        :rtype: float
        """
        return (Epoch.mjd_to_jd(mjd) - J2000_JULIAN_DATE) * DAYS_TO_JULIAN_CENTURY

    @staticmethod
    def days_past_j2000(mjd: float) -> float:
        return Epoch.mjd_to_jd(mjd) - J2000_JULIAN_DATE

    def plus_days(self, t: float) -> "Epoch":
        """calculate an epoch that is separated from the calling epoch by t days

        :param t: time delta of the two epochs in days
        :type t: float
        :return: an epoch that is t days away from the calling epoch
        :rtype: Epoch
        """
        return Epoch(self.utc + t)

    def greenwich_hour_angle(self) -> float:
        """calculate the greenwich hour angle used to determine sidereal time

        :return: greenwich mean sidereal time in radians
        :rtype: float
        """
        # solve for julian centuries since j2000 using equation 2.7
        dec_day = self.utc % 1
        j0 = Epoch.mjd_to_jd(self.ut1) - dec_day
        j = (j0 - J2000_JULIAN_DATE) * DAYS_TO_JULIAN_CENTURY

        # solve for theta0 using equation 2.6
        theta0 = 100.4606184 + 36000.77004 * j + 0.000387933 * j * j

        # solve for gmst using equation 2.8
        total_deg = theta0 + 360.98564724 * dec_day

        return radians(total_deg % 360)
