class SphericalVector:
    def __init__(self, ra: float, dec: float, radius: float) -> None:
        self.right_ascension: float = ra
        self.declination: float = dec
        self.radius: float = radius
