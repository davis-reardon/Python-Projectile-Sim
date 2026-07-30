import numpy as np
from src.simcore.monte_carlo import run_campaign, campaign_statistics
from src.simcore.monte_carlo import convergence_study


def test_convergence_study_returns_one_entry_per_sample_size():
    results = convergence_study(sample_sizes=[5, 10, 20], base_seed=1)
    assert len(results) == 3
    assert [r["n_runs"] for r in results] == [5, 10, 20]


def test_convergence_study_means_stay_in_reasonable_range():
    """As n grows, the mean shouldn't wildly diverge — it should
    stabilize around the same underlying value."""
    results = convergence_study(sample_sizes=[10, 100], base_seed=1)
    mean_small_n = results[0]["mean"]
    mean_large_n = results[1]["mean"]
    # Both should be within a reasonable range of each other, not wildly different
    assert abs(mean_small_n - mean_large_n) < 5.0  # meters, generous tolerance

def test_campaign_produces_one_result_per_run():
    results = run_campaign(n_runs=10, base_seed=42)
    assert len(results) == 10


def test_campaign_is_reproducible_with_same_seed():
    results_a = run_campaign(n_runs=5, base_seed=100)
    results_b = run_campaign(n_runs=5, base_seed=100)
    ranges_a = [r["final_range_m"] for r in results_a]
    ranges_b = [r["final_range_m"] for r in results_b]
    assert np.allclose(ranges_a, ranges_b)


def test_each_run_has_unique_seed():
    results = run_campaign(n_runs=5, base_seed=0)
    seeds = [r["seed"] for r in results]
    assert len(set(seeds)) == 5


def test_campaign_statistics_computes_expected_fields():
    results = run_campaign(n_runs=20, base_seed=7)
    stats = campaign_statistics(results)
    assert stats["min"] <= stats["mean"] <= stats["max"]
    assert stats["p5"] <= stats["p95"]
    assert "worst_case_run" in stats