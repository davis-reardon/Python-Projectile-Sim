import numpy as np
from src.simcore.atmosphere import isa_density

SUTTON_GRAVES_K = 1.7415e-4  # empirical constant, SI units


def stagnation_heat_flux_w_m2(altitude_m, speed_m_s, nose_radius_m):
    """
    Simplified stagnation-point convective heat flux (Sutton-Graves
    approximation). Convective heating only — ignores radiative heating
    and does not model heat conduction/temperature rise over time.
    """
    rho = isa_density(altitude_m)
    return SUTTON_GRAVES_K * np.sqrt(rho / nose_radius_m) * speed_m_s**3


def thermal_margin(heat_flux_w_m2, max_allowable_w_m2):
    """
    Fraction of maximum allowable heat flux used. margin < 1.0 is safe,
    >= 1.0 means the allowable heating limit has been exceeded.
    """
    return heat_flux_w_m2 / max_allowable_w_m2