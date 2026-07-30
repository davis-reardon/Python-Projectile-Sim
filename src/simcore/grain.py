import numpy as np


def bates_burn_radius(t, inner_radius0_m, outer_radius_m, burn_rate_m_s):
    """
    Radius of the burning surface at time t, for a BATES grain burning
    radially outward at a constant regression rate.
    Clipped at outer_radius_m once the web is fully consumed.
    """
    r = inner_radius0_m + burn_rate_m_s * t
    return np.minimum(r, outer_radius_m)


def bates_burn_area(radius_m, length_m):
    """
    Burning surface area (m^2) of a BATES grain's inner cylindrical wall
    at a given radius. Ends assumed inhibited (non-burning).
    """
    return 2 * np.pi * radius_m * length_m