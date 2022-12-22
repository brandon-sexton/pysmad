from math import radians, tan

class OpticalConstraints:

    DEFAULT_SUN_HARD = radians(60)
    DEFAULT_SUN_SOFT = radians(90)
    DEFAULT_MOON_LIMIT = radians(10)
    DEFAULT_EARTH_LIMIT = radians(20)
    DEFAULT_LIMITING_MAG = 15
    DEFAULT_RESOLUTION_LIMIT= 1e-5
    DEFAULT_FRAME_DAMP = 1

    def __init__(self, pixels:float, fov:float) -> None:
        self.sun_hard:float = OpticalConstraints.DEFAULT_SUN_HARD
        self.sun_soft:float = OpticalConstraints.DEFAULT_SUN_SOFT
        self.moon:float = OpticalConstraints.DEFAULT_MOON_LIMIT
        self.earth:float = OpticalConstraints.DEFAULT_EARTH_LIMIT
        self.vismag:float = OpticalConstraints.DEFAULT_LIMITING_MAG
        self.bore:float = OpticalConstraints.DEFAULT_FRAME_DAMP*fov
        clos:float = OpticalConstraints.DEFAULT_RESOLUTION_LIMIT*2*pixels
        self.characterization:float = clos/tan(fov)
