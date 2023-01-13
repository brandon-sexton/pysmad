from pyxis.astro.coordinates import GCRFstate, SphericalPosition
from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch


class SpaceObservation:
    def __init__(
        self, observer_state: GCRFstate, observed_direction: Vector3D, r_error: float, ang_error: float
    ) -> None:
        self.observer_state: GCRFstate = observer_state.copy()
        self.observed_direction: Vector3D = observed_direction.copy()
        spherical: SphericalPosition = SphericalPosition.from_cartesian(observed_direction)
        self.range: float = spherical.radius
        self.right_ascension: float = spherical.right_ascension
        self.declination: float = spherical.declination
        self.range_error: float = r_error
        self.angular_error: float = ang_error


class PositionOb:
    def __init__(self, epoch: Epoch, position: Vector3D, error: float) -> None:
        """class used to store an observation that contains position only

        :param epoch: time of the observation
        :type epoch: Epoch
        :param position: observed position vector in km
        :type position: Vector3D
        :param error: error associated with the magnitude of the observed position vector in km
        :type error: float
        """
        #: time of the observation
        self.epoch: Epoch = epoch.copy()

        #: observed position in km
        self.position: Vector3D = position.copy()

        #: error in km of the observed position magnitude
        self.error: float = error
