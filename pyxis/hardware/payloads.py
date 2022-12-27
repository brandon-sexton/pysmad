from math import radians, tan

from pyxis.hardware.constraints import OpticalConstraints


class Camera:

    DEFAULT_WIDE_PIXELS = 3072
    DEFAULT_NARROW_PIXELS = 3072
    DEFAULT_NFOV = radians(0.125)
    DEFAULT_WFOV = radians(5)

    def __init__(self, pixels: float, fov: float) -> None:
        self.pixels: float = pixels
        self.fov: float = fov
        self.limits: OpticalConstraints = OpticalConstraints(self.pixels, self.fov)
        self.resolution_factor = 1 / self.pixels * 0.5

    @classmethod
    def wfov(cls) -> "Camera":
        return cls(Camera.DEFAULT_WIDE_PIXELS, Camera.DEFAULT_WFOV)

    @classmethod
    def nfov(cls) -> "Camera":
        return cls(Camera.DEFAULT_NARROW_PIXELS, Camera.DEFAULT_NFOV)

    def resolution(self, r: float) -> float:
        return tan(self.fov) * r * self.resolution_factor

    def range_error(self, r: float, d: float) -> float:
        return self.resolution(r) / (d) * r

    def tracking_minimum(self, body_r: float) -> float:
        return body_r / (tan(self.fov))
