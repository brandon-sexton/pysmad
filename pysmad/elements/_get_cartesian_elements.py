from pysmad.elements._cartesian_elements import CartesianElements
from pysmad.elements._classical_elements import ClassicalElements


class GetCartesianElements:
    @staticmethod
    def from_classical(els: ClassicalElements) -> CartesianElements:
        """calculates the cartesian representation of the element set

        :return: inertial state of the element set
        :rtype: IJK
        """

        pqw_matrix = els.pqw_matrix
        r = pqw_matrix.multiply_vector(els.pqw_position)
        v = pqw_matrix.multiply_vector(els.pqw_velocity)

        return CartesianElements.from_position_and_velocity(r, v)
