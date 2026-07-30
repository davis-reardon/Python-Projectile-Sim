import numpy as np


def align_and_compute_residual(t_reference, values_reference, t_other, values_other):
    """
    Interpolate values_other onto t_reference's time grid, then compute
    the residual (reference - interpolated_other) at each reference time.

    Points in t_reference that fall outside t_other's time range are
    excluded (interpolation is undefined there), since a real HWIL run
    may start/end at slightly different times than the digital sim.
    """
    valid_mask = (t_reference >= t_other.min()) & (t_reference <= t_other.max())
    t_valid = t_reference[valid_mask]
    ref_valid = values_reference[valid_mask]

    other_interp = np.interp(t_valid, t_other, values_other)
    residual = ref_valid - other_interp

    return t_valid, residual

def find_first_divergence(t, residual, tolerance, min_consecutive=3):
    """
    Find the first time at which |residual| exceeds tolerance for at
    least min_consecutive consecutive samples.

    Returns (divergence_time, divergence_residual) or (None, None) if
    no sustained divergence is found.
    """
    exceeds = np.abs(residual) > tolerance
    consecutive_count = 0

    for i in range(len(exceeds)):
        if exceeds[i]:
            consecutive_count += 1
            if consecutive_count >= min_consecutive:
                start_idx = i - min_consecutive + 1
                return t[start_idx], residual[start_idx]
        else:
            consecutive_count = 0

    return None, None