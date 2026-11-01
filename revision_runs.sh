#!/usr/bin/env bash
# Experiments added after the synopsis review (~4 h total; AC power, all apps closed, don't use the laptop).
#   A: equal-core-count P vs E (1-4 physical cores)        -> results/equalcount.csv
#   B: mixed / full-chip configurations, separate           -> results/mixed.csv
# Both solve to the same tolerance (1e-8), 3 repetitions, randomised order;
# iteration counts and true residuals are recorded and checked, not forced equal.
set -euo pipefail
cd "$(dirname "$0")"
src/rapl_idle 0.1 > /dev/null || { echo "RAPL not readable: run the chmod from README first" >&2; exit 1; }
echo "== A: equal core counts =="
REPS=3 TOL=1e-8 ITERS=20000 OUT=results/equalcount.csv ./sweep.sh configs/equalcount.txt
python3 analyze.py results/equalcount.csv > /dev/null
echo "== B: mixed / full-chip =="
REPS=3 TOL=1e-8 ITERS=20000 OUT=results/mixed.csv ./sweep.sh configs/mixed.txt
python3 analyze.py results/mixed.csv > /dev/null
echo "done: results/equalcount_report.md, results/mixed_report.md"
