import numpy as np
from src.simcore.grain import bates_burn_radius, bates_burn_area
from src.simcore.projectile import simulate


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

def test_grain_thrust_increases_range_vs_no_thrust():
    """A grain-driven progressive burn should still meaningfully outperform
    an unpowered flight, proving the wiring produces real, usable thrust."""
    _, x_no_thrust, _, _, _ = simulate(v0=30, angle_deg=45, thrust_n=0)

    _, x_grain, _, _, _ = simulate(
        v0=30, angle_deg=45, burn_time_s=2.0,
        dry_mass_kg=5.0, propellant_mass_kg=2.0,
        grain_inner_radius0_m=0.01, grain_outer_radius_m=0.03,
        grain_burn_rate_m_s=0.01, grain_length_m=0.2,
        thrust_per_area_n_m2=50000.0)

    assert x_grain[-1] > x_no_thrust[-1]


def test_grain_thrust_increases_over_burn():
    """Progressive BATES burn: burn area (and thrust) should be larger
    near the end of the burn than at the very start."""
    from src.simcore.grain import bates_burn_radius, bates_burn_area

    r0 = bates_burn_radius(0.0, 0.01, 0.03, 0.01)
    r_late = bates_burn_radius(1.5, 0.01, 0.03, 0.01)

    area0 = bates_burn_area(r0, 0.2)
    area_late = bates_burn_area(r_late, 0.2)

    assert area_late > area0