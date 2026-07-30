import numpy as np
import pytest
from src.simcore.projectile import simulate

def test_no_drag_matches_analytical_range():
    v0, angle_deg = 30, 45
    _, x, _, _ = simulate(v0, angle_deg, drag_coeff=0.0)
    analytic_range = (v0**2 * np.sin(np.radians(2 * angle_deg))) / 9.81
    assert x[-1] == pytest.approx(analytic_range, rel=.02)

def test_drag_reduces_range():
    v0, angle_deg = 30, 45
    _, x_no_drag, _, _ = simulate(v0, angle_deg, drag_coeff=0.0)
    _, x_drag, _, _ = simulate(v0, angle_deg, drag_coeff=0.02)
    assert x_drag[-1] < x_no_drag[-1]

def test_higher_drag_reduced_range_more():
    v0, angle_deg = 30, 45
    _, x_low_drag, _, _ = simulate(v0, angle_deg, drag_coeff=.01)
    _, x_high_drag, _, _ = simulate(v0, angle_deg, drag_coeff=0.05)
    assert x_high_drag[-1] < x_low_drag[-1]

def test_orientation_changes_with_angular_velocity():
    t, x, y, theta_final = simulate(v0=30, angle_deg=45)
    # initial omega is hardcoded to 0.1 rad/s in simulate(); theta should
    # accumulate away from its initial value of 0.0 over a nonzero flight time
    assert theta_final != 0.0
    assert len(t) > 0