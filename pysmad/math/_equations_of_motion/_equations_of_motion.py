from pysmad.math._equations_of_motion._get_areal_velocity import GetArealVelocity
from pysmad.math._equations_of_motion._get_argument_of_latitude import GetArgumentOfLatitude
from pysmad.math._equations_of_motion._get_argument_of_perigee import GetArgumentOfPerigee
from pysmad.math._equations_of_motion._get_eccentric_anomaly import GetEccentricAnomaly
from pysmad.math._equations_of_motion._get_eccentricity import GetEccentricity
from pysmad.math._equations_of_motion._get_flattening import GetFlattening
from pysmad.math._equations_of_motion._get_inclination import GetInclination
from pysmad.math._equations_of_motion._get_mean_anomaly import GetMeanAnomaly
from pysmad.math._equations_of_motion._get_mean_motion import GetMeanMotion
from pysmad.math._equations_of_motion._get_raan import GetRAAN
from pysmad.math._equations_of_motion._get_semi_major_axis import GetSemiMajorAxis
from pysmad.math._equations_of_motion._get_semi_minor_axis import GetSemiMinorAxis
from pysmad.math._equations_of_motion._get_semi_parameter import GetSemiParameter
from pysmad.math._equations_of_motion._get_true_anomaly import GetTrueAnomaly


class EquationsOfMotion:
    """A static class used to solve various equations of motion"""

    eccentricity = GetEccentricity
    flattening = GetFlattening
    semi_major_axis = GetSemiMajorAxis
    semi_minor_axis = GetSemiMinorAxis
    semi_parameter = GetSemiParameter
    areal_velocity = GetArealVelocity
    eccentric_anomaly = GetEccentricAnomaly
    true_anomaly = GetTrueAnomaly
    mean_anomaly = GetMeanAnomaly
    inclination = GetInclination
    raan = GetRAAN
    mean_motion = GetMeanMotion
    argument_of_latitude = GetArgumentOfLatitude
    argument_of_perigee = GetArgumentOfPerigee
