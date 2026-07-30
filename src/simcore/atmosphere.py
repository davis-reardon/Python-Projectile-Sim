import numpy as np

def isa_density(altitude_m):
    """Returns air density (kg/m^3) using the ISA troposphere model, valid 0-11000m."""
    T0 = 288.15      # K, sea level standard temp
    P0 = 101325.0    # Pa, sea level standard pressure
    L = 0.0065       # K/m, temperature lapse rate
    R = 8.31447      # J/(mol*K)
    M = 0.0289644    # kg/mol, molar mass of air
    g = 9.81         # m/s^2

    altitude_m = np.clip(altitude_m, 0, 11000)  # clamp to valid range for now
    T = T0 - L * altitude_m
    P = P0 * (T / T0) ** (g * M / (R * L))
    rho = P / (287.05 * T)  # 287.05 = specific gas constant for dry air
    return rho