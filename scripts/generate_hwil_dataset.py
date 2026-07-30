import argparse
import numpy as np
from src.simcore.projectile import simulate
from src.simcore.frames import range_to_enu
from src.simcore.telemetry import write_telemetry_csv
from src.simcore.faults import add_gaussian_noise, apply_clock_offset, drop_samples

SEED = 42


def generate(output_path, apply_noise=False, apply_offset=False,
             apply_dropout=False, noise_std=0.05, offset_s=0.05,
             dropout_fraction=0.03):
    t, x, y, z, theta = simulate(v0=50, angle_deg=45, thrust_n=500,
                                   burn_time_s=3.0, dry_mass_kg=5.0,
                                   propellant_mass_kg=2.0)

    if apply_dropout:
        t, x, y, z, theta = drop_samples(t, x, y, z, theta,
                                          drop_fraction=dropout_fraction, seed=SEED)

    if apply_noise:
        x = add_gaussian_noise(x, noise_std=noise_std, seed=SEED)
        y = add_gaussian_noise(y, noise_std=noise_std, seed=SEED + 1)

    if apply_offset:
        t = apply_clock_offset(t, offset_s=offset_s)

    e, n, u = range_to_enu(x, y, az_deg=0.0)
    write_telemetry_csv(output_path, t, x, y, e, n, u)
    print(f"Generated {output_path} "
          f"(noise={apply_noise}, offset={apply_offset}, dropout={apply_dropout})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a clean or faulted telemetry dataset")
    parser.add_argument("--output", default="data/results/hwil.csv")
    parser.add_argument("--noise", action="store_true")
    parser.add_argument("--offset", action="store_true")
    parser.add_argument("--dropout", action="store_true")
    args = parser.parse_args()

    generate(args.output, apply_noise=args.noise,
             apply_offset=args.offset, apply_dropout=args.dropout)