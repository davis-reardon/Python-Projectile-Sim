import numpy as np


def add_gaussian_noise(values, noise_std, seed=None):
    """
    Add Gaussian sensor noise to a signal array.
    noise_std: standard deviation of noise, same units as values.
    """
    rng = np.random.default_rng(seed)
    return values + rng.normal(0.0, noise_std, size=values.shape)


def apply_clock_offset(timestamps, offset_s):
    """
    Shift timestamps by a fixed offset, simulating unsynchronized clocks
    between the simulation and HWIL/tactical system.
    """
    return timestamps + offset_s


def drop_samples(t, x, y, z, theta, drop_fraction, seed=None):
    """
    Randomly remove a fraction of samples (simulating dropped telemetry
    packets). Returns filtered (t, x, y, z, theta) arrays of matching length.
    """
    rng = np.random.default_rng(seed)
    n = len(t)
    keep_mask = rng.random(n) >= drop_fraction
    return t[keep_mask], x[keep_mask], y[keep_mask], z[keep_mask], theta