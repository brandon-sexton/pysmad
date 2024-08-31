from pathlib import Path

import pytest

from pysmad.bodies import GeodeticModel


@pytest.fixture
def detic_model():
    geo_path = Path("pysmad/bodies/EGM96.potential")
    return GeodeticModel(geo_path)


def test_c_coefficient(detic_model):
    assert detic_model.c_coefficients[2][0] == -0.000484165371736
    assert len(detic_model.c_coefficients) == GeodeticModel.DEFAULT_DEGREE + 1


def test_s_coefficient(detic_model):
    assert detic_model.s_coefficients[3][1] == 2.48513158716e-07
    assert len(detic_model.s_coefficients) == GeodeticModel.DEFAULT_DEGREE + 1


def test_radius(detic_model):
    assert detic_model.radius == 6378.1363


def test_mu(detic_model):
    assert detic_model.mu == 398600.4415
