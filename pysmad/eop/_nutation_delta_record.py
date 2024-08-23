class NutationDeltaRecord:
    def __init__(self, psi: float, epsilon: float, psi_err: float, epsilon_err: float) -> None:
        self.psi: float = psi
        self.epsilon: float = epsilon
        self.psi_error: float = psi_err
        self.epsilon_error: float = epsilon_err
        self.is_empty: bool = False

    @classmethod
    def empty_record(cls) -> "NutationDeltaRecord":
        record = cls(0, 0, 0, 0)
        record.is_empty = True
        return record
