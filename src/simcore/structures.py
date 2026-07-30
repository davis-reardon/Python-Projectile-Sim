import numpy as np


def axial_stress_pa(mass_kg, acceleration_m_s2, cross_section_area_m2):
    """
    Simplified axial stress on the airframe, from net acceleration loading.
    Treats total (not directionally-resolved) acceleration magnitude as the
    driving load — a conservative first-pass approximation, not true
    beam-bending analysis.
    """
    force_n = mass_kg * np.abs(acceleration_m_s2)
    return force_n / cross_section_area_m2


def structural_margin(stress_pa, yield_strength_pa):
    """
    Returns the fraction of yield strength used (margin < 1.0 means safe,
    margin >= 1.0 means the structure has exceeded yield strength).
    """
    return stress_pa / yield_strength_pa