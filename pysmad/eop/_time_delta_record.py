class TimeDeltaRecord:
    def __init__(self, ut1_utc: float, tai_utc: float, ut1_error: float) -> None:
        """Class used to store time differences.

        :param ut1_utc: UT1 - UTC (days)
        :param tai_utc: TAI - UTC (days)
        :param ut1_error: The error in UT1 - UTC (days)
        """

        #: UT1 - UTC (days)
        self.ut1_utc: float = ut1_utc

        #: TAI - UTC (days)
        self.tai_utc: float = tai_utc

        #: UT1 - UTC error (days)
        self.ut1_error: float = ut1_error
