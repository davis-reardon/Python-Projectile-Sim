import argparse
from src.simcore.monte_carlo import run_campaign, campaign_statistics, convergence_study


def print_campaign_report(results, stats):
    print("=" * 50)
    print("MONTE CARLO CAMPAIGN REPORT")
    print("=" * 50)
    print(f"\nRuns: {len(results)}")
    print(f"Mean final range: {stats['mean']:.3f} m")
    print(f"Std dev: {stats['std']:.3f} m")
    print(f"Range: [{stats['min']:.3f}, {stats['max']:.3f}] m")
    print(f"5th-95th percentile: [{stats['p5']:.3f}, {stats['p95']:.3f}] m")
    print(f"\nWorst case (min range):")
    wc = stats["worst_case_run"]
    print(f"  run_id={wc['run_id']}, seed={wc['seed']}, "
          f"angle={wc['angle_deg']:.3f}deg, drag={wc['drag_coeff']:.4f}, "
          f"range={wc['final_range_m']:.3f}m")


def print_convergence_report(conv_results):
    print("\n" + "=" * 50)
    print("CONVERGENCE STUDY")
    print("=" * 50)
    for r in conv_results:
        print(f"  n={r['n_runs']:>4}  mean={r['mean']:.3f} m  std={r['std']:.3f} m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Monte Carlo campaign")
    parser.add_argument("--n-runs", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--convergence", action="store_true",
                         help="Also run a convergence study")
    args = parser.parse_args()

    results = run_campaign(n_runs=args.n_runs, base_seed=args.seed)
    stats = campaign_statistics(results)
    print_campaign_report(results, stats)

    if args.convergence:
        conv = convergence_study(sample_sizes=[10, 50, 100, 500], base_seed=args.seed)
        print_convergence_report(conv)