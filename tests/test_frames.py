import numpy as np
from src.simcore.frames import range_to_enu


def test_range_to_enu_due_north():
    E, N, U = range_to_enu(np.array([100.0]), np.array([50.0]), 0.0)
    assert np.isclose(E[0], 0.0)
    assert np.isclose(N[0], 100.0)
    assert np.isclose(U[0], 50.0)


def test_range_to_enu_due_east():
    E, N, U = range_to_enu(np.array([100.0]), np.array([50.0]), 90.0)
    assert np.isclose(E[0], 100.0)
    assert np.isclose(N[0], 0.0)
    assert np.isclose(U[0], 50.0)