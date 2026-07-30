import numpy as np
from src.simcore.grain import bates_burn_radius, bates_burn_area


def test_radius_grows_linearly_then_clips():
    r0, r_outer, burn_rate = 0.01, 0.03, 0.005  # meters, m/s
    r_start = bates_burn_radius(0.0, r0, r_outer, burn_rate)
    r_mid = bates_burn_radius(2.0, r0, r_outer, burn_rate)
    r_late = bates_burn_radius(100.0, r0, r_outer, burn_rate)  # far past burnout

    assert np.isclose(r_start, r0)
    assert r_mid > r_start
    assert np.isclose(r_late, r_outer)  # clipped, doesn't exceed outer radius


def test_burn_area_increases_with_radius():
    length = 0.2
    area_small = bates_burn_area(0.01, length)
    area_large = bates_burn_area(0.02, length)
    assert area_large > area_small
    assert np.isclose(area_small, 2 * np.pi * 0.01 * length)