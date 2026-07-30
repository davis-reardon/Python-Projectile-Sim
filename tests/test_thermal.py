import numpy as np
from src.simcore.thermal import stagnation_heat_flux_w_m2, thermal_margin


def test_heat_flux_increases_with_speed():
    flux_low = stagnation_heat_flux_w_m2(altitude_m=0, speed_m_s=500,
                                           nose_radius_m=0.1)
    flux_high = stagnation_heat_flux_w_m2(altitude_m=0, speed_m_s=1000,
                                            nose_radius_m=0.1)
    assert flux_high > flux_low


def test_heat_flux_decreases_with_altitude():
    """Lower density at altitude should reduce heat flux at same speed."""
    flux_sea_level = stagnation_heat_flux_w_m2(altitude_m=0, speed_m_s=1000,
                                                  nose_radius_m=0.1)
    flux_high_alt = stagnation_heat_flux_w_m2(altitude_m=8000, speed_m_s=1000,
                                                 nose_radius_m=0.1)
    assert flux_high_alt < flux_sea_level


def test_thermal_margin_under_limit_is_safe():
    flux = stagnation_heat_flux_w_m2(altitude_m=0, speed_m_s=500,
                                       nose_radius_m=0.1)
    margin = thermal_margin(flux, max_allowable_w_m2=5e6)
    assert margin < 1.0


def test_thermal_margin_exceeds_limit_when_overheated():
    flux = stagnation_heat_flux_w_m2(altitude_m=0, speed_m_s=3000,
                                       nose_radius_m=0.05)
    margin = thermal_margin(flux, max_allowable_w_m2=5e5)
    assert margin > 1.0