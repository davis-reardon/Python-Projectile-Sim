import numpy as np
from src.simcore.comparison import align_and_compute_residual
from src.simcore.comparison import align_and_compute_residual, find_first_divergence

def test_residual_near_zero_for_identical_signal():
    t = np.linspace(0, 10, 100)
    values = np.sin(t)
    t_valid, residual = align_and_compute_residual(t, values, t, values)
    assert np.allclose(residual, 0.0, atol=1e-10)


def test_residual_reflects_offset_signal():
    t = np.linspace(0, 10, 100)
    values = np.zeros_like(t)
    values_offset = values + 5.0  # constant 5-unit offset
    t_valid, residual = align_and_compute_residual(t, values, t, values_offset)
    assert np.allclose(residual, -5.0)


def test_time_ranges_outside_overlap_are_excluded():
    t_reference = np.linspace(0, 10, 50)
    values_reference = np.ones_like(t_reference)
    t_other = np.linspace(2, 8, 30)  # narrower range
    values_other = np.ones_like(t_other)

    t_valid, residual = align_and_compute_residual(
        t_reference, values_reference, t_other, values_other)

    assert t_valid.min() >= 2.0
    assert t_valid.max() <= 8.0

def test_find_first_divergence_detects_sustained_exceedance():
    t = np.arange(10, dtype=float)
    residual = np.array([0.1, 0.1, 0.1, 5.0, 5.0, 5.0, 5.0, 0.1, 0.1, 0.1])
    div_time, div_residual = find_first_divergence(
        t, residual, tolerance=1.0, min_consecutive=3)
    assert div_time == 3.0
    assert div_residual == 5.0


def test_find_first_divergence_ignores_brief_spike():
    """A single-sample spike (not sustained) should not count as divergence."""
    t = np.arange(10, dtype=float)
    residual = np.array([0.1, 0.1, 5.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    div_time, div_residual = find_first_divergence(
        t, residual, tolerance=1.0, min_consecutive=3)
    assert div_time is None


def test_find_first_divergence_returns_none_when_within_tolerance():
    t = np.arange(10, dtype=float)
    residual = np.full(10, 0.05)
    div_time, div_residual = find_first_divergence(
        t, residual, tolerance=1.0, min_consecutive=3)
    assert div_time is None