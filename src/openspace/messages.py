class Alerts:

    WARNING: str = "\x1b[1;33;40m"
    CLOSE: str = "\x1b[0m"
    PROCESS: str = "\x1b[1;36;40m"
    SUCCESS: str = "\x1b[1;32;40m"

    @staticmethod
    def color(color_code: str, msg) -> None:
        print("".join([color_code, msg, Alerts.CLOSE]))

    @staticmethod
    def print_query_max_warning() -> None:
        msg: str = "WARNING:  Results may be missing.  The returned volume is equal to the query maximum."
        Alerts.color(Alerts.WARNING, msg)

    @staticmethod
    def print_query_start(url: str) -> None:
        Alerts.color(Alerts.PROCESS, " ".join(["Query in progress for URL", url]))

    @staticmethod
    def print_successful_query(num: int) -> None:
        msg: str = " ".join(["SUCCESS:  Query returned", str(num), "results."])
        Alerts.color(Alerts.SUCCESS, msg)
