import csv
import numpy as np
from src.simcore.comparison import align_and_compute_residual, find_first_divergence


def load_telemetry_csv(filepath):
    with open(filepath) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return {
        "t_s": np.array([float(r["t_s"]) for r in rows]),
        "x_m": np.array([float(r["x_m"]) for r in rows]),
        "y_m": np.array([float(r["y_m"]) for r in rows]),
    }


def compare(digital_path, hwil_path, tolerance_m=0.5):
    digital = load_telemetry_csv(digital_path)
    hwil = load_telemetry_csv(hwil_path)

    results = {}
    for signal in ["x_m", "y_m"]:
        t_valid, residual = align_and_compute_residual(
            digital["t_s"], digital[signal], hwil["t_s"], hwil[signal])
        div_time, div_residual = find_first_divergence(
            t_valid, residual, tolerance=tolerance_m, min_consecutive=3)
        results[signal] = {
            "t_valid": t_valid,
            "residual": residual,
            "first_divergence_time": div_time,
            "first_divergence_residual": div_residual,
        }

    return results


def print_report(results, tolerance_m):
    print("=" * 50)
    print("SIM-TO-HWIL COMPARISON REPORT")
    print("=" * 50)
    for signal, r in results.items():
        print(f"\nSignal: {signal}")
        if r["first_divergence_time"] is not None:
            print(f"  First divergence: t={r['first_divergence_time']:.3f}s")
            print(f"  Observed residual: {r['first_divergence_residual']:.4f} m")
            print(f"  Tolerance: {tolerance_m} m")
        else:
            print(f"  No sustained divergence detected (within {tolerance_m} m tolerance)")
        print(f"  Residual range: [{r['residual'].min():.4f}, {r['residual'].max():.4f}] m")


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare digital vs HWIL telemetry")
    parser.add_argument("--digital", default="data/results/digital.csv")
    parser.add_argument("--hwil", default="data/results/hwil.csv")
    parser.add_argument("--tolerance", type=float, default=0.5)
    args = parser.parse_args()

    results = compare(args.digital, args.hwil, tolerance_m=args.tolerance)
    print_report(results, tolerance_m=args.tolerance)