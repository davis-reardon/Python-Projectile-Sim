import numpy as np
from src.simcore.projectile import simulate
from src.simcore.frames import range_to_enu
from src.simcore.telemetry import write_telemetry_csv
from src.simcore.faults import add_gaussian_noise, apply_clock_offset, drop_samples

SEED = 42

# --- Clean digital simulation ---
t, x, y, z, theta = simulate(v0=50, angle_deg=45, thrust_n=500,
                               burn_time_s=3.0, dry_mass_kg=5.0,
                               propellant_mass_kg=2.0)
e, n, u = range_to_enu(x, y, az_deg=0.0)
write_telemetry_csv("data/results/digital.csv", t, x, y, e, n, u)

# --- Faulted "HWIL-like" version, same underlying run ---
t_faulted, x_faulted, y_faulted, z_faulted, theta_faulted = drop_samples(
    t, x, y, z, theta, drop_fraction=0.03, seed=SEED)

x_faulted = add_gaussian_noise(x_faulted, noise_std=0.05, seed=SEED)
y_faulted = add_gaussian_noise(y_faulted, noise_std=0.05, seed=SEED + 1)
t_faulted = apply_clock_offset(t_faulted, offset_s=0.05)

e_faulted, n_faulted, u_faulted = range_to_enu(x_faulted, y_faulted, az_deg=0.0)
write_telemetry_csv("data/results/hwil.csv", t_faulted, x_faulted, y_faulted,
                     e_faulted, n_faulted, u_faulted)

print("Generated data/results/digital.csv and data/results/hwil.csv")