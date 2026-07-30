# Five-Minute Technical Walkthrough

## 1. What this is (30 sec)
Two related projects: a from-scratch RK4 projectile/rocket simulator,
and a sim-to-HWIL correlation workflow built on top of it — the second
one modeling the actual analysis work this role centers on.

## 2. Live demo (90 sec)
```bash
python -m scripts.generate_hwil_dataset --output data/results/digital.csv
python -m scripts.generate_hwil_dataset --output data/results/hwil.csv --noise --offset --dropout
python -m scripts.compare_runs
```
Walk through the printed report: first divergence, residual range, tolerance.

## 3. The finding (90 sec)
Full-fault comparison showed a large (~2m) residual immediately at
t=0.05s — looked like a physics/model problem at first glance. Isolating
factors (removing the clock offset alone) dropped the residual by >90%,
confirming a timing discrepancy, not a model-form error. Walk through
*why* that mattered: timing errors look identical to physics errors in
a residual plot, but the fix is completely different.

## 4. Supporting infrastructure (60 sec)
- Monte Carlo campaign manager: per-run seeding, aleatory vs epistemic
  uncertainty, convergence demonstrated (mean stabilizes, variance doesn't
  vanish)
- Requirements traceability: 10 requirements, live-verified against the
  real test suite, not hand-maintained
- 46 tests, all features developed via branch -> test -> PR -> merge

## 5. What this demonstrates (30 sec)
Comfort with the actual job: controlling configuration, treating
reproducibility as non-negotiable, distinguishing discrepancy categories
before jumping to conclusions, and using git/testing discipline as
default practice rather than an afterthought.