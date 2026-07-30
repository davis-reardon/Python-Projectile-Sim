import numpy as np
import pytest
from src.simcore.projectile import simulate

def test_no_drag_matches_analytical_range():
    v0, angle_deg = 30, 45
    _, x, _, _, _ = simulate(v0, angle_deg, drag_coeff=0.0)
    analytic_range = (v0**2 * np.sin(np.radians(2 * angle_deg))) / 9.81
    assert x[-1] == pytest.approx(analytic_range, rel=.02)

def test_drag_reduces_range():
    v0, angle_deg = 30, 45
    _, x_no_drag, _, _, _ = simulate(v0, angle_deg, drag_coeff=0.0)
    _, x_drag, _, _, _ = simulate(v0, angle_deg, drag_coeff=0.02)
    assert x_drag[-1] < x_no_drag[-1]

def test_higher_drag_reduced_range_more():
    v0, angle_deg = 30, 45
    _, x_low_drag, _, _, _ = simulate(v0, angle_deg, drag_coeff=.01)
    _, x_high_drag, _, _, _ = simulate(v0, angle_deg, drag_coeff=0.05)
    assert x_high_drag[-1] < x_low_drag[-1]

def test_orientation_changes_with_angular_velocity():
    t, x, y, z, theta_final = simulate(v0=30, angle_deg=45)
    assert theta_final != 0.0
    assert len(t) > 0

def test_no_wind_stays_on_plane():
    """With zero crosswind, z should remain at 0 throughout flight."""
    _, _, _, z, _ = simulate(v0=30, angle_deg=45, wind_accel_z=0.0)
    assert np.allclose(z, 0.0)

def test_crosswind_produces_lateral_drift():
    """A nonzero crosswind should push the trajectory off the x-y plane."""
    _, _, _, z, _ = simulate(v0=30, angle_deg=45, wind_accel_z=2.0)
    assert z[-1] != 0.0
    assert z[-1] > 0  # wind_accel_z positive should drift in positive z

def test_aero_torque_changes_final_theta():
    """Nonzero stability_coeff should produce a different final orientation
    than stability_coeff=0, proving aero torque actually acts on theta."""
    _, _, _, _, theta_no_aero = simulate(v0=30, angle_deg=45, stability_coeff=0.0)
    _, _, _, _, theta_with_aero = simulate(v0=30, angle_deg=45, stability_coeff=5.0)

    assert theta_no_aero != theta_with_aero

def test_body_axis_thrust_requires_correct_initial_theta():
    """Thrust along body axis only helps range if theta starts aligned
    with the initial velocity direction — this guards against theta
    being hardcoded to 0 regardless of launch angle."""
    _, x_aligned, _, _, _ = simulate(v0=30, angle_deg=45, thrust_n=300,
                                       burn_time_s=1.0, dry_mass_kg=2.0,
                                       propellant_mass_kg=0.5)
    _, x_no_thrust, _, _, _ = simulate(v0=30, angle_deg=45, thrust_n=0)

    # With theta correctly initialized to the launch angle, thrust should
    # meaningfully outperform the unpowered case
    assert x_aligned[-1] > x_no_thrust[-1] * 1.1  # not just marginally more

def test_gimbal_angle_changes_trajectory():
    """A nonzero gimbal angle should steer the trajectory differently than
    zero gimbal (straight body-axis thrust) — proving vectoring actually
    changes flight path, not just torque."""
    _, x_straight, y_straight, _, _ = simulate(
        v0=30, angle_deg=45, thrust_n=300, burn_time_s=1.0,
        dry_mass_kg=2.0, propellant_mass_kg=0.5, gimbal_angle_deg=0.0)

    _, x_vectored, y_vectored, _, _ = simulate(
        v0=30, angle_deg=45, thrust_n=300, burn_time_s=1.0,
        dry_mass_kg=2.0, propellant_mass_kg=0.5, gimbal_angle_deg=15.0)

    assert x_vectored[-1] != x_straight[-1]


def test_gimbal_angle_produces_torque():
    """Nonzero gimbal angle should produce a different final theta than
    zero gimbal, proving the moment-arm torque is real."""
    _, _, _, _, theta_straight = simulate(
        v0=30, angle_deg=45, thrust_n=300, burn_time_s=1.0,
        dry_mass_kg=2.0, propellant_mass_kg=0.5, gimbal_angle_deg=0.0)

    _, _, _, _, theta_vectored = simulate(
        v0=30, angle_deg=45, thrust_n=300, burn_time_s=1.0,
        dry_mass_kg=2.0, propellant_mass_kg=0.5, gimbal_angle_deg=15.0)

    assert theta_straight != theta_vectored