from pysmad.constants import HOURS_TO_DAYS, MINUTES_TO_DAYS, SECONDS_TO_DAYS


class GetDecimalDay:
    @staticmethod
    def from__hms(hours: int, minutes: int, seconds: float) -> float:
        return hours * HOURS_TO_DAYS + minutes * MINUTES_TO_DAYS + seconds * SECONDS_TO_DAYS
