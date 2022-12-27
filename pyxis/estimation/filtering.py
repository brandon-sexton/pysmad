from pyxis.astro.coordinates import HillState
from pyxis.astro.propagators.relative import Hill
from pyxis.estimation.obs import PositionOb
from pyxis.math.constants import SECONDS_IN_DAY
from pyxis.math.linalg import Matrix3by6, Matrix3D, Matrix6by3, Matrix6D, Vector3D, Vector6D
from pyxis.time import Epoch


class RelativeKalman:

    DEFAULT_COVARIANCE = Matrix6D(
        Vector6D(0.5, 0, 0, 0, 0, 0),
        Vector6D(0, 0.5, 0, 0, 0, 0),
        Vector6D(0, 0, 0.5, 0, 0, 0),
        Vector6D(0, 0, 0, 5e-5, 0, 0),
        Vector6D(0, 0, 0, 0, 5e-5, 0),
        Vector6D(0, 0, 0, 0, 0, 5e-5),
    )

    DEFAULT_NOISE = Matrix6D(
        Vector6D(1e-16, 0, 0, 0, 0, 0),
        Vector6D(0, 1e-16, 0, 0, 0, 0),
        Vector6D(0, 0, 1e-16, 0, 0, 0),
        Vector6D(0, 0, 0, 1e-16, 0, 0),
        Vector6D(0, 0, 0, 0, 1e-16, 0),
        Vector6D(0, 0, 0, 0, 0, 1e-16),
    )

    H: Matrix3by6 = Matrix3by6(
        Vector6D(1, 0, 0, 0, 0, 0),
        Vector6D(0, 1, 0, 0, 0, 0),
        Vector6D(0, 0, 1, 0, 0, 0),
    )
    HT: Matrix6by3 = H.transpose()
    I: Matrix6D = Matrix6D.identity()

    def __init__(self, epoch: Epoch, propagator: Hill) -> None:
        self.epoch: Epoch = epoch.copy()
        self.propagator: Hill = propagator
        self.x00: Vector6D = self.propagator.state.vector.copy()
        self.x10: Vector6D
        self.p00: Matrix6D = RelativeKalman.DEFAULT_COVARIANCE
        self.p10: Matrix6D
        self.q: Matrix6D = RelativeKalman.DEFAULT_NOISE
        self.f: Matrix6D = self.propagator.system_matrix(0)
        self.k: Matrix6by3
        self.z: Vector3D
        self.range_error: float = 0
        self.r: Matrix3D
        self.angles_only: bool = True

    def predict_covariance(self) -> None:
        self.p10 = self.f.multiply_matrix(self.p00.multiply_matrix(self.f.transpose())).plus(self.q)

    def gain(self) -> None:
        normal_measurment = self.z.normalized()
        self.r = Matrix3D(
            Vector3D(
                normal_measurment.x * self.range_error * normal_measurment.x * self.range_error,
                0,
                0,
            ),
            Vector3D(
                0,
                normal_measurment.y * self.range_error * normal_measurment.y * self.range_error,
                0,
            ),
            Vector3D(
                0,
                0,
                normal_measurment.z * self.range_error * normal_measurment.z * self.range_error,
            ),
        )
        hph: Matrix3D = self.H.multiply_matrix_6by3(self.p10.multiply_matrix_6by3(self.HT))
        self.k = self.p10.multiply_matrix_6by3(self.HT.multiply(hph.plus(self.r).inverse()))

    def predict_state(self, dt: float) -> None:
        self.f = self.propagator.system_matrix(dt)
        self.x10 = self.f.multiply_vector(self.x00)

    def update_state(self) -> None:
        self.x00 = self.x10.plus(self.k.multiply_vector(self.z.minus(self.H.multiply_vector(self.x10))))
        self.propagator.state = HillState.from_state_vector(self.x00)

    def update_covariance(self) -> None:
        m1: Matrix6D = self.I.minus(self.k.multiply_matrix3by6(self.H))
        m2: Matrix6D = self.k.multiply_matrix3by6(self.r.multiply_matrix3by6(self.k.transpose()))
        self.p00 = m1.multiply_matrix(self.p10.multiply_matrix(m1.transpose())).plus(m2)

    def predict(self, dt: float) -> None:
        self.predict_state(dt)
        self.predict_covariance()

    def update(self) -> None:
        self.gain()
        self.update_state()
        self.update_covariance()

    def process(self, ob: PositionOb) -> None:
        dt = (ob.epoch.value - self.epoch.value) * SECONDS_IN_DAY
        self.epoch = ob.epoch.copy()
        self.z = ob.position.copy()
        self.range_error = ob.error
        self.predict(dt)
        self.update()
