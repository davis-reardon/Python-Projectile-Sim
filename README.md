# Python Projectile Sim — Simulation & Sim-to-HWIL Correlation Lab

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
reproducibility. Run with `python -m pytest -v`.

## Development workflow

All features developed on isolated branches, merged via reviewed pull
requests. See git history for the full sequence of PRs (23 merged),
including a deliberate `git bisect` regression-hunting exercise
(see commit history around the grain-geometry module).