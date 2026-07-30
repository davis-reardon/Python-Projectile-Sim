import numpy as np
from src.simcore.structures import axial_stress_pa, structural_margin


def test_axial_stress_scales_with_acceleration():
    stress_low = axial_stress_pa(mass_kg=5.0, acceleration_m_s2=10.0,
                                   cross_section_area_m2=0.001)
    stress_high = axial_stress_pa(mass_kg=5.0, acceleration_m_s2=50.0,
                                    cross_section_area_m2=0.001)
    assert stress_high > stress_low
    assert np.isclose(stress_low, 5.0 * 10.0 / 0.001)


def test_structural_margin_under_yield_is_safe():
    stress = axial_stress_pa(mass_kg=5.0, acceleration_m_s2=20.0,
                               cross_section_area_m2=0.001)
    margin = structural_margin(stress, yield_strength_pa=270e6)  # aluminum
    assert margin < 1.0


def test_structural_margin_exceeds_yield_when_overloaded():
    # Deliberately extreme acceleration/tiny cross-section to force overload
    stress = axial_stress_pa(mass_kg=5.0, acceleration_m_s2=1000.0,
                               cross_section_area_m2=0.00001)
    margin = structural_margin(stress, yield_strength_pa=270e6)
    assert margin > 1.0