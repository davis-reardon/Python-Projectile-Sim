import numpy as np
from src.simcore.faults import add_gaussian_noise, apply_clock_offset, drop_samples


def test_gaussian_noise_changes_values_but_preserves_shape():
    values = np.array([1.0, 2.0, 3.0, 4.0])
    noisy = add_gaussian_noise(values, noise_std=0.1, seed=42)
    assert noisy.shape == values.shape
    assert not np.allclose(noisy, values)


def test_gaussian_noise_is_reproducible_with_same_seed():
    values = np.array([1.0, 2.0, 3.0])
    noisy_a = add_gaussian_noise(values, noise_std=0.5, seed=7)
    noisy_b = add_gaussian_noise(values, noise_std=0.5, seed=7)
    assert np.array_equal(noisy_a, noisy_b)


def test_clock_offset_shifts_all_timestamps():
    t = np.array([0.0, 0.1, 0.2, 0.3])
    shifted = apply_clock_offset(t, offset_s=0.05)
    assert np.allclose(shifted, t + 0.05)


def test_drop_samples_reduces_length():
    t = np.linspace(0, 1, 100)
    x = t.copy()
    y = t.copy()
    z = t.copy()
    t_kept, x_kept, y_kept, z_kept, theta = drop_samples(
        t, x, y, z, theta=0.5, drop_fraction=0.1, seed=1)
    assert len(t_kept) < len(t)
    assert len(t_kept) == len(x_kept) == len(y_kept) == len(z_kept)