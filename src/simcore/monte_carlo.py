import numpy as np
from src.simcore.projectile import simulate


def run_campaign(n_runs, base_seed=0, angle_deg_mean=45.0, angle_deg_std=1.0,
                  drag_coeff_mean=0.02, drag_coeff_std=0.005):
    """
    Run a Monte Carlo campaign varying launch angle (aleatory) and drag
    coefficient (epistemic). Each run has an independent, reproducible seed.

    Returns a list of dicts, one per run, with run_id, seed, inputs, and
    final_range_m.
    """
    results = []
    for run_id in range(n_runs):
        seed = base_seed + run_id
        rng = np.random.default_rng(seed)

        angle_deg = rng.normal(angle_deg_mean, angle_deg_std)
        drag_coeff = max(0.0, rng.normal(drag_coeff_mean, drag_coeff_std))

        _, x, _, _, _ = simulate(v0=50, angle_deg=angle_deg,
                                   drag_coeff=drag_coeff)

        results.append({
            "run_id": run_id,
            "seed": seed,
            "angle_deg": angle_deg,
            "drag_coeff": drag_coeff,
            "final_range_m": x[-1],
        })

    return results


def campaign_statistics(results):
    """Compute summary statistics from a completed campaign."""
    ranges = np.array([r["final_range_m"] for r in results])
    return {
        "mean": np.mean(ranges),
        "std": np.std(ranges),
        "min": np.min(ranges),
        "max": np.max(ranges),
        "p5": np.percentile(ranges, 5),
        "p95": np.percentile(ranges, 95),
        "worst_case_run": results[np.argmin(ranges)],
    }
    

def convergence_study(sample_sizes, base_seed=0, **campaign_kwargs):
    """
    Run campaigns at increasing sample sizes to demonstrate Monte Carlo
    convergence: the estimated mean should stabilize as n grows, while
    any systematic model bias remains regardless of n.
    """
    convergence_results = []
    for n in sample_sizes:
        results = run_campaign(n_runs=n, base_seed=base_seed, **campaign_kwargs)
        stats = campaign_statistics(results)
        convergence_results.append({
            "n_runs": n,
            "mean": stats["mean"],
            "std": stats["std"],
        })
    return convergence_results
