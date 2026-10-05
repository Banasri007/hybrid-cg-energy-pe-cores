#!/usr/bin/env bash
# Follow-up experiments after the full sweep (~40 min total, AC power, nothing else running).
#  1. Spin test   -> results/spin.csv     (3 matrices x 13 configs x 3 reps, 1000 fixed iterations)
#  2. Convergence -> results/converge.csv (5 matrices x 6 configs x 1 rep, solve to 1e-8)
set -euo pipefail
cd "$(dirname "$0")"
src/rapl_idle 0.1 > /dev/null || { echo "RAPL not readable: run the chmod from README first" >&2; exit 1; }

echo "== 1/2 spin test =="
MATRICES="matrices/thermal2/thermal2.rcm.csr matrices/G3_circuit/G3_circuit.rcm.csr matrices/ecology2/ecology2.rcm.csr" \
REPS=3 ITERS=1000 OUT=results/spin.csv ./sweep.sh configs/spin.txt
python3 analyze.py results/spin.csv > /dev/null

echo "== 2/2 convergence check =="
REPS=1 TOL=1e-8 ITERS=20000 OUT=results/converge.csv ./sweep.sh configs/converge.txt
python3 analyze.py results/converge.csv > /dev/null

echo "done: results/spin_report.md, results/converge_report.md"
