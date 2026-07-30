# Python Projectile Sim — Simulation & Sim-to-HWIL Correlation Lab

![Tests](https://github.com/davis-reardon/Python-Projectile-Sim/actions/workflows/tests.yml/badge.svg)

A reproducible RK4 projectile/rocket simulation with a full sim-to-HWIL
correlation workflow: reproducible telemetry generation, fault injection,
time-aligned residual comparison, first-divergence detection, Monte Carlo
uncertainty quantification, and requirements traceability.

## What this demonstrates

This project is not primarily a physics simulator. It demonstrates the
workflow: **generate controlled simulation data → compare against
imperfect "HWIL-like" data → identify discrepancies → trace causes
upstream → automate the analysis → preserve reproducibility.**

## Quickstart

```bash
conda env create -f environment.yml
conda activate projectile-sim

# Run the physics sim + generate telemetry
python -m scripts.generate_hwil_dataset --output data/results/digital.csv
python -m scripts.generate_hwil_dataset --output data/results/hwil.csv --noise --offset --dropout

# Compare digital vs HWIL, detect first divergence
python -m scripts.compare_runs

# Run a Monte Carlo campaign with convergence analysis
python -m scripts.run_campaign --n-runs 200 --convergence

# Generate the requirements traceability matrix
python -m requirements.traceability

# Run the full test suite
python -m pytest -v
```

## Simulation capabilities

- 3D (downrange/altitude/cross-range) RK4 trajectory integration
- Quadratic drag with ISA atmosphere density model
- Solid-propellant propulsion via BATES grain geometry (progressive burn)
- Command-and-control abort with realistic latency modeling
- Aerodynamic restoring torque (angle-of-attack coupling)
- Gimbaled thrust vectoring (body-axis thrust + moment-arm torque)
- Structural (axial stress/yield margin) and thermal (stagnation heating)
  post-processing analysis

## Scripts Reference

### `scripts/generate_hwil_dataset.py`
Generates telemetry from a simulated flight, optionally injecting
sensor noise, clock offset, and sample dropout to mimic imperfect
HWIL-style data.

```bash
# Clean digital baseline
python -m scripts.generate_hwil_dataset --output data/results/digital.csv

# Faulted "HWIL-like" dataset with all three fault types
python -m scripts.generate_hwil_dataset --output data/results/hwil.csv --noise --offset --dropout

# Isolate a single fault type (for root-cause investigation)
python -m scripts.generate_hwil_dataset --output data/results/hwil_offset_only.csv --offset
```

**Use case:** producing paired datasets for correlation analysis, or
isolating individual fault types to determine which one is driving a
discrepancy (see `scripts/compare_runs.py` below).

---

### `scripts/compare_runs.py`
Time-aligns two telemetry datasets via interpolation and reports the
first sustained divergence between them, per signal.

```bash
# Compare the default digital.csv vs hwil.csv
python -m scripts.compare_runs

# Compare specific files with a custom tolerance
python -m scripts.compare_runs --digital data/results/digital.csv --hwil data/results/hwil_offset_only.csv --tolerance 0.3
```

**Use case:** the core discrepancy-investigation tool — run it against
different fault combinations to determine whether a large residual is
caused by noise, timing, dropout, or a genuine model error.

---

### `scripts/run_campaign.py`
Runs a reproducible Monte Carlo campaign, varying launch angle
(aleatory) and drag coefficient (epistemic), and reports summary
statistics and the worst-case run.

```bash
# Basic 200-run campaign
python -m scripts.run_campaign --n-runs 200

# Include a convergence study (10, 50, 100, 500 runs)
python -m scripts.run_campaign --n-runs 200 --convergence --seed 42
```

**Use case:** quantifying uncertainty in final range given known
input variability, and identifying which specific run (seed) produced
the worst-case outcome for further investigation.

---

### `scripts/plot_trajectory.py`
Renders a 3D visualization of a single simulated trajectory
(downrange, cross-range, altitude), saved as a PNG.

```bash
python -m scripts.plot_trajectory
```

## Sim-to-HWIL correlation workflow

- **Fault injection** (`src/simcore/faults.py`): seeded, reproducible
  sensor noise, clock offset, and sample dropout
- **Comparison pipeline** (`src/simcore/comparison.py`): time-aligned
  residual computation (interpolation-based, not index-based) and
  sustained (N-consecutive-sample) first-divergence detection
- **Monte Carlo campaign manager** (`src/simcore/monte_carlo.py`):
  per-run-seeded parameter variation, aleatory vs. epistemic uncertainty,
  convergence analysis
- **Requirements traceability** (`requirements/`): 10 requirements,
  live-verified against the actual test suite

## Demonstrated finding

An initial full-fault comparison (noise + clock offset + dropout) showed
a ~1.8–2.8m residual immediately at the first comparison point. Isolating
factors (removing the clock offset, keeping noise + dropout) dropped the
residual to ~0.16–0.18m — within tolerance — confirming a 0.05s clock
offset (amplified by high initial velocity) as the dominant discrepancy
source, not a model-form error.

## Testing

46 tests across 11 test files, covering physics, coordinate transforms,
telemetry schema, fault injection, comparison logic, and Monte Carlo
reproducibility. Run with both an automated CI workflow under the 'Actions' 
tab on github as well as: `python -m pytest -v`.

## Development workflow

All features developed on isolated branches, merged via reviewed pull
requests. See git history for the full sequence of PRs (23 merged),
including a deliberate `git bisect` regression-hunting exercise
(see commit history around the grain-geometry module).
