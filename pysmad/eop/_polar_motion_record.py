class PolarMotionRecord:
    def __init__(self, px: float, py: float, px_err: float, py_err: float) -> None:
        self.x: float = px
        self.y: float = py
        self.x_error: float = px_err
        self.y_error: float = py_err
        self.is_empty: bool = False

    @classmethod
    def empty_record(cls) -> "PolarMotionRecord":
        record = cls(0, 0, 0, 0)
        record.is_empty = True
        return record
