#!/usr/bin/env bash
# Hardware-counter check of HOW waiting ranks/threads spend their cycles.
# Hypothesis: libgomp waits with PAUSE (low power); Open MPI's shared-memory
# polling does not -> P-cores burn full-power instructions while waiting for E-cores.
#
# Needs system-wide perf counters (resets on reboot):
#   sudo sysctl kernel.perf_event_paranoid=0
# Run:  ./perf_check.sh        (~5 min)  -> results/perf/*.csv + results/perf_summary.md
set -euo pipefail
cd "$(dirname "$0")"
(( $(cat /proc/sys/kernel/perf_event_paranoid) <= 0 )) || {
    echo "run first: sudo sysctl kernel.perf_event_paranoid=0" >&2; exit 1; }

M=${M:-matrices/thermal2/thermal2.rcm.csr}
ITERS=${ITERS:-2000}
REPS=${REPS:-2}
OUT=results/perf; mkdir -p "$OUT"
A12=0,2,4,6,8,9,10,11,12,13,14,15; M8=0,2,4,6,8,9,10,11; P4=0,2,4,6
EVENTS="cpu_core/cycles/,cpu_core/instructions/,cpu_core/cpu_clk_unhalted.pause/,cpu_core/cpu_clk_unhalted.c0_wait/,cpu_atom/cycles/,cpu_atom/instructions/"

# label cpus ranks threads env
CONFIGS=(
  "A12-mpi $A12 12 1 -"
  "A12-omp $A12 1 12 -"
  "A12-ompactive $A12 1 12 OMP_WAIT_POLICY=active"
  "M8-mpi $M8 8 1 -"
  "M8-omp $M8 1 8 -"
  "P4-mpi $P4 4 1 -"
  "P4-omp $P4 1 4 -"
)

pkg_temp() { for z in /sys/class/thermal/thermal_zone*; do
    [[ $(cat "$z/type") == x86_pkg_temp ]] && { echo $(( $(cat "$z/temp") / 1000 )); return; }; done; echo 0; }

for rep in $(seq 1 "$REPS"); do
  for c in "${CONFIGS[@]}"; do
    read -r label cpus ranks threads xenv <<< "$c"
    envs=(); [[ $xenv != - ]] && envs=("$xenv")
    sleep 5; while (( $(pkg_temp) > 55 )); do sleep 2; done
    f="$OUT/${label}_r${rep}"
    env "${envs[@]}" CPUS=$cpus OMP_NUM_THREADS=$threads OMP_SCHEDULE=static \
      perf stat -a -A -C "$cpus" -x, -o "$f.perf.csv" -e "$EVENTS" -- \
      mpirun -np "$ranks" --bind-to none --oversubscribe src/bind.sh src/cg_hybrid "$M" 0 "$ITERS" \
      | grep '^matrix=' > "$f.run.txt"
    printf '%-14s rep%d  %s\n' "$label" "$rep" "$(grep -o 'time_s=[0-9.]*\|e_pkg_j=[0-9.]*' "$f.run.txt" | tr '\n' ' ')"
  done
done
python3 perf_summary.py "$OUT" | tee results/perf_summary.md
