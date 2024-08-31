from pysmad.math._equations_of_motion._areal_velocity import ArealVelocity
from pysmad.math._equations_of_motion._eccentric_anomaly import EccentricAnomaly
from pysmad.math._equations_of_motion._eccentricity import Eccentricity
from pysmad.math._equations_of_motion._flattening import Flattening
from pysmad.math._equations_of_motion._mean_anomaly import MeanAnomaly
from pysmad.math._equations_of_motion._semi_major_axis import SemiMajorAxis
from pysmad.math._equations_of_motion._semi_minor_axis import SemiMinorAxis
from pysmad.math._equations_of_motion._semi_parameter import SemiParameter
from pysmad.math._equations_of_motion._true_anomaly import TrueAnomaly


class EquationsOfMotion:
    """A static class used to solve various equations of motion"""

    eccentricity = Eccentricity
    flattening = Flattening
    semi_major_axis = SemiMajorAxis
    semi_minor_axis = SemiMinorAxis
    semi_parameter = SemiParameter
    areal_velocity = ArealVelocity
    eccentric_anomaly = EccentricAnomaly
    true_anomaly = TrueAnomaly
    mean_anomaly = MeanAnomaly
