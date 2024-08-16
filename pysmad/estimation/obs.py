from math import radians

from pysmad.coordinates.positions import ENZ, LLA, PositionConvert, SphericalPosition
from pysmad.coordinates.states import GCRF, ITRF
from pysmad.math.linalg import Vector3D
from pysmad.time import Epoch


class Observation:
    """super class used for space-based and ground-based observations"""

    def __init__(self) -> None:
        pass

    def ijk_position(self) -> Vector3D:
        raise NotImplementedError

    def epoch(self) -> Epoch:
        raise NotImplementedError

    def observer_ijk(self) -> Vector3D:
        raise NotImplementedError


class SpaceObservation(Observation):
    def __init__(self, observer_state: GCRF, observed_direction: Vector3D, r_error: float, ang_error: float) -> None:
        """object used for state estimation when the observer is a space asset

        :param observer_state: inertial state of the observer at the time of the observation
        :type observer_state: GCRF
        :param observed_direction: GCRF direction of the object from the observer
        :type observed_direction: Vector3D
        :param r_error: one-sigma error of the observed range in km
        :type r_error: float
        :param ang_error: one-sigma error of the angles in radians
        :type ang_error: float
        """
        #: inertial state of the observer at the time of the observation
        self.observer_state: GCRF = observer_state.copy()

        #: vector from observer to target in the GCRF frame
        self.observed_direction: Vector3D = observed_direction.copy()

        spherical: SphericalPosition = SphericalPosition.from_cartesian(observed_direction)

        #: magnitude of the observation in km
        self.range: float = spherical.radius

        #: right ascension of the observation in radians
        self.right_ascension: float = spherical.right_ascension

        #: declination of the observation in radians
        self.declination: float = spherical.declination

        #: one-sigma range error of the observation in km
        self.range_error: float = r_error

        #: one-sigma angular error of the observation in radians
        self.angular_error: float = ang_error

    def epoch(self) -> Epoch:
        """get the time the observation was taken

        :return: valid epoch of the observation
        :rtype: Epoch
        """
        return self.observer_state.epoch

    def ijk_position(self) -> Vector3D:
        """calculate the inertial position of the observation

        :return: inertial position of the observation in the IJK frame
        :rtype: Vector3D
        """
        return PositionConvert.gcrf.to_ijk(self.observer_state.position.plus(self.observed_direction), self.epoch())


class GroundObservation(Observation):
    def __init__(self, observer_state: ITRF, observed_direction: Vector3D, r_error: float, ang_error: float) -> None:
        """used to perform operations related to ground site measurements

        :param observer_state: geocentric coordinates of the observer
        :type observer_state: ITRF
        :param observed_direction: ENZ direction of object from observer
        :type observed_direction: Vector3D
        :param r_error: one-sigma error of the observed range in km
        :type r_error: float
        :param ang_error: one-sigma error of the angles in radians
        :type ang_error: float
        """
        #: geocentric state of the observer at the time of the observation
        self.observer_state: ITRF = observer_state.copy()

        #: vector from observer to target in the ENZ frame
        self.observed_direction: Vector3D = observed_direction.copy()

        spherical: SphericalPosition = SphericalPosition.from_cartesian(
            Vector3D(observed_direction.y, observed_direction.x, observed_direction.z)
        )

        #: magnitude of the observation in km
        self.range: float = spherical.radius

        #: azimuth of the observation in radians
        self.azimuth: float = spherical.right_ascension

        #: elevation of the observation in radians
        self.elevation: float = spherical.declination

        #: one-sigma range error of the observation in km
        self.range_error: float = r_error

        #: one-sigma angular error of the observation in radians
        self.angular_error: float = ang_error

    @classmethod
    def from_angles_and_range(
        cls, observer_state: ITRF, az: float, el: float, r: float, r_error: float, ang_error: float
    ) -> "GroundObservation":
        """create an observation from azimuth, elevation, and range

        :param observer_state: geocentric coordinates of the observer
        :type observer_state: ITRF
        :param az: azimuth of the observation in radians
        :type az: float
        :param el: elevation of the observation in radians
        :type el: float
        :param r: magnitude of the observation in km
        :type r: float
        :param r_error: one-sigma range error of the observation in km
        :type r_error: float
        :param ang_error: one-sigma angular error of the observation in radians
        :type ang_error: float
        :return: observation from a terrestrial site
        :rtype: GroundObservation
        """
        nez: Vector3D = SphericalPosition(r, az, el).to_cartesian()
        enz: Vector3D = Vector3D(nez.y, nez.x, nez.z)
        return cls(observer_state, enz, r_error, ang_error)

    def epoch(self) -> Epoch:
        """get the time the observation was taken

        :return: valid epoch of the observation
        :rtype: Epoch
        """
        return self.observer_state.epoch

    def ijk_position(self) -> Vector3D:
        """calculate the inertial position of the observation

        :return: inertial position of the observation in the IJK frame
        :rtype: Vector3D
        """
        lla_site: LLA = PositionConvert.itrf.to_lla(self.observer_state.position)
        itrf_ob: Vector3D = PositionConvert.enz.to_itrf(lla_site, self.observed_direction).plus(
            self.observer_state.position
        )
        return PositionConvert.itrf.to_ijk(itrf_ob, self.epoch())

    def gcrf_position(self) -> Vector3D:
        """calculate the inertial position of the observation

        :return: inertial position of the observation in the GCRF frame
        :rtype: Vector3D
        """
        lla_site: LLA = PositionConvert.itrf.to_lla(self.observer_state.position)
        itrf_ob: Vector3D = PositionConvert.enz.to_itrf(lla_site, self.observed_direction).plus(
            self.observer_state.position
        )
        return PositionConvert.itrf.to_gcrf(itrf_ob, self.epoch())


class LiveOpticalObservation:
    def __init__(self, ob_dict):
        """interface used to access data stored in live observations

        :param ob_dict: single return from a Query JSON
        :type ob_dict: dict
        """
        self.epoch: Epoch = Epoch.from_udl_string(ob_dict["obTime"])
        self.sat_id: str = ob_dict.get("origObjectId", ob_dict.get("idOnOrbit", "UNKNOWN"))
        self.observer_id: str = ob_dict.get("origSensorId", ob_dict.get("sensorId", "NOT PROVIDED"))
        self.azimuth: float = radians(ob_dict.get("azimuth", 0))
        self.elevation: float = radians(ob_dict.get("elevation", 0))
        self.observer_lla: LLA = LLA(radians(ob_dict["senlat"]), radians(ob_dict["senlon"]), ob_dict["senalt"])
        self.observer_eci: Vector3D = Vector3D(ob_dict.get("senx", 0), ob_dict.get("seny"), ob_dict.get("senz"))
        self.right_ascension: float = radians(ob_dict["ra"])
        self.declination: float = radians(ob_dict["declination"])
        self.visual_magnitude: float = ob_dict.get("mag", 0)
        self.source: str = ob_dict["source"]
        self.mode: str = ob_dict["dataMode"]
        self.equatorial_phase_angle: float = ob_dict.get("solarEqPhaseAngle", 0)
        self.solar_declination_angle: float = ob_dict.get("solarDecAngle", 0)

    def get_observer_itrf(self) -> ITRF:
        return ITRF.from_fixed(self.epoch, PositionConvert.lla.to_itrf(self.observer_lla))

    def get_clos(self, tgt_gcrf: GCRF) -> float:
        observed = GroundObservation.from_angles_and_range(
            self.get_observer_itrf(), self.azimuth, self.elevation, 1, 0, 0
        )
        observed.observed_direction
        mat = ENZ.matrix(self.observer_lla.longitude, self.observer_lla.latitude)
        tgt_itrf = PositionConvert.gcrf.to_itrf(tgt_gcrf.position, tgt_gcrf.epoch)
        expected = mat.multiply_vector(tgt_itrf.minus(self.get_observer_itrf().position))
        return expected.magnitude() * expected.angle(observed.observed_direction)

    def csv_headers(self) -> str:
        return ",".join(
            [
                "UTC_EPOCH",
                "SOURCE",
                "TARGET_ID",
                "AZ",
                "EL",
                "RA",
                "DEC",
                "SOLAR_EQ_PHASE",
                "SOLAR_DEC_PHASE",
                "VISMAG",
                "SENSOR_ID",
                "SENSOR_LAT",
                "SENSOR_LON",
                "SENSOR_ALT",
            ]
        )

    def to_csv_format(self) -> str:
        return ",".join(
            [
                self.epoch.to_udl_string(),
                self.source,
                self.sat_id,
                str(self.azimuth),
                str(self.elevation),
                str(self.right_ascension),
                str(self.declination),
                str(self.equatorial_phase_angle),
                str(self.solar_declination_angle),
                str(self.visual_magnitude),
                self.observer_id,
                str(self.observer_lla.latitude),
                str(self.observer_lla.longitude),
                str(self.observer_lla.altitude),
            ]
        )


class LiveOpticalSet:
    def __init__(self):
        self.list = []
        self.sensors = {}
        self.targets = {}
        self.sources = {}
        self.modes = {}
        self.total = 0

    def publish_set(self, filename: str, write_mode: str) -> None:

        with open(filename, write_mode) as f:
            for ob in self.list:
                f.write("".join([ob.to_csv_format(), "\n"]))

    def process_observation(self, ob: LiveOpticalObservation) -> None:
        self.list.append(ob)
        self.total += 1
        if self.sensors.get(ob.observer_id) is None:
            self.sensors[ob.observer_id] = []
        if self.targets.get(ob.sat_id) is None:
            self.targets[ob.sat_id] = []
        if self.sources.get(ob.source) is None:
            self.sources[ob.source] = []
        if self.modes.get(ob.mode) is None:
            self.modes[ob.mode] = []

        self.sensors[ob.observer_id].append(ob)
        self.targets[ob.sat_id].append(ob)
        self.sources[ob.source].append(ob)
        self.modes[ob.mode].append(ob)

    def get_observers(self):
        return self.sensors.keys()

    def get_targets(self):
        return self.targets.keys()

    def get_sources(self):
        return self.sources.keys()
