#!/usr/bin/env bash
# Configuration sweep: one command, one CSV.
#
#   ./sweep.sh configs/full.txt                 # defaults below
#   REPS=3 ITERS=300 OUT=results/pilot.csv ./sweep.sh configs/pilot.txt
#
# Env knobs:
#   MATRICES    space-separated specs (default: the 5 RCM-reordered matrices)
#   REPS        repetitions of every (matrix, config)              [5]
#   ITERS       fixed CG iterations per run (tol=0 mode)           [1000]
#   OUT         output CSV (appended; header written if new)       [results/sweep.csv]
#   COOL_C      wait until package temp <= this before each run    [55]
#   COOL_MIN_S  minimum pause between runs                         [5]
#   COOL_MAX_S  give up waiting after this (run is still logged)   [120]
#   TOL         CG tolerance; 0 = fixed ITERS iterations, >0 = solve to
#               tolerance with ITERS as the iteration cap           [0]
#   IDLE_MAX_W  abort if idle package power at start exceeds this   [5]
#               (background activity); FORCE=1 to run anyway
#
# Pre-defined exclusion rule (applied by analyze.py, never by hand):
#   a run is excluded only if its thermal-throttle counter increased during
#   the solve or the laptop was not on AC power. Slow runs are NOT removed.
#
# Energy is read twice per run, never summed across MPI processes:
#   e_pkg_j      rank 0, package counter, between barriers around the solve loop
#   e_pkg_run_j  this script, package counter, around the whole mpirun
#
# Config lines: label cpus ranks threads sched [env] [mpiargs]
#   env      optional comma-separated VAR=value list, e.g. OMP_WAIT_POLICY=active
#   mpiargs  optional extra mpirun args, commas for spaces, e.g. --mca,mpi_yield_when_idle,1
#   use "-" as a placeholder for an empty env when giving mpiargs
#
# Order: rep-major, and (matrix, config) pairs shuffled within each rep, so
# slow drift (heat soak, background load) spreads across configs instead of
# biasing one of them.
set -euo pipefail
cd "$(dirname "$0")"

CFG=${1:?usage: $0 <config file>}
REPS=${REPS:-5}
ITERS=${ITERS:-1000}
OUT=${OUT:-results/sweep.csv}
COOL_C=${COOL_C:-55}
COOL_MIN_S=${COOL_MIN_S:-5}
COOL_MAX_S=${COOL_MAX_S:-120}
TOL=${TOL:-0}
IDLE_MAX_W=${IDLE_MAX_W:-5}
PKG=/sys/class/powercap/intel-rapl:0
MATRICES=${MATRICES:-"matrices/ecology2/ecology2.rcm.csr matrices/apache2/apache2.rcm.csr matrices/thermal2/thermal2.rcm.csr matrices/G3_circuit/G3_circuit.rcm.csr matrices/cant/cant.rcm.csr"}
BIN=src/cg_hybrid

mkdir -p "$(dirname "$OUT")"
COLS="matrix n nnz ranks threads sched iters converged rel_res true_rel_res max_err ghost_max time_s halo_s allreduce_s e_pkg_j e_core_j e_uncore_j e_psys_j temp_start_c temp_end_c throttle_delta cpu_map"

pkg_temp() {
    for z in /sys/class/thermal/thermal_zone*; do
        [[ $(cat "$z/type") == x86_pkg_temp ]] && { echo $(( $(cat "$z/temp") / 1000 )); return; }
    done
    echo 0
}

pkg_uj() { cat "$PKG/energy_uj" 2>/dev/null || echo -1; }

# package energy in J between two counter readings, handling one wraparound
pkg_delta_j() {
    local a=$1 b=$2 max
    (( a < 0 || b < 0 )) && { echo -1; return; }
    max=$(cat "$PKG/max_energy_range_uj")
    (( b < a )) && b=$(( b + max + 1 ))
    awk -v d=$(( b - a )) 'BEGIN { printf "%.3f", d / 1e6 }'
}

ac_online() {
    for f in /sys/class/power_supply/*/online; do [[ -r $f ]] && { cat "$f"; return; }; done
    echo "?"
}

cooldown() {
    local waited=0
    sleep "$COOL_MIN_S"; waited=$COOL_MIN_S
    while (( $(pkg_temp) > COOL_C && waited < COOL_MAX_S )); do sleep 2; waited=$((waited + 2)); done
    echo "$waited"
}

# --- run metadata (frequency policy etc. must stay fixed across the sweep) ---
META="${OUT%.csv}.meta.txt"
{
    echo "date: $(date -Is)"
    echo "config_file: $CFG  reps: $REPS  iters: $ITERS  tol: $TOL  cool_c: $COOL_C"
    echo "cpu: $(lscpu | sed -n 's/^Model name: *//p')"
    echo "kernel: $(uname -r)"
    echo "governor: $(sort -u /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor | tr '\n' ' ')"
    echo "epp: $(sort -u /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference 2>/dev/null | tr '\n' ' ')"
    echo "no_turbo: $(cat /sys/devices/system/cpu/intel_pstate/no_turbo 2>/dev/null)"
    echo "platform_profile: $(cat /sys/firmware/acpi/platform_profile 2>/dev/null || echo n/a)"
    echo "ac_online: $(ac_online)"
    echo "mpirun: $(mpirun --version 2>&1 | head -1)"
    echo "rapl_domains: $(for d in /sys/class/powercap/intel-rapl:*; do printf '%s=%s ' "${d##*/}" "$(cat "$d/name")"; done)"
    echo "exclusion_rule: throttle_delta > 0 or ac_online != 1 (fixed before the sweep; no other runs removed)"
    IDLE=$(src/rapl_idle 20 || true)
    echo "idle_baseline: $IDLE"
} >> "$META"
cat "$META" | tail -13

idle_w=$(sed -nE 's/.*p_pkg_w=([-0-9.]+).*/\1/p' <<< "$IDLE")
if [[ -n $idle_w ]] && awk -v w="$idle_w" -v m="$IDLE_MAX_W" 'BEGIN { exit !(w > m) }' && [[ ${FORCE:-0} != 1 ]]; then
    echo "ABORT: idle package power ${idle_w} W > ${IDLE_MAX_W} W -> background activity. Close apps and retry (FORCE=1 to override)." >&2
    exit 2
fi

if src/rapl_idle 0.1 > /dev/null; then echo "RAPL: readable"; else
    echo "WARNING: RAPL energy_uj not readable -> energy columns will be -1 (see README)"; fi

[[ -f $OUT ]] || echo "timestamp,rep,label,cpus,ac_online,cooldown_s,load1,run_wall_s,e_pkg_run_j,${COLS// /,}" > "$OUT"

mapfile -t CONFIGS < <(grep -v '^\s*#' "$CFG" | grep -v '^\s*$')
total=$(( REPS * ${#CONFIGS[@]} * $(wc -w <<< "$MATRICES") ))
done_n=0

for rep in $(seq 1 "$REPS"); do
    mapfile -t JOBS < <(for m in $MATRICES; do for c in "${CONFIGS[@]}"; do echo "$m|$c"; done; done | shuf)
    for job in "${JOBS[@]}"; do
        m=${job%%|*}; read -r label cpus ranks threads sched xenv xmpi <<< "${job#*|}"
        envs=(); mpiargs=()
        [[ -n ${xenv:-} && $xenv != - ]] && IFS=, read -ra envs <<< "$xenv"
        [[ -n ${xmpi:-} ]] && IFS=, read -ra mpiargs <<< "$xmpi"
        cool=$(cooldown)
        ac=$(ac_online)
        load1=$(cut -d' ' -f1 /proc/loadavg)
        r0=$(pkg_uj); w0=$(date +%s.%N)
        if [[ $cpus == none ]]; then
            line=$(env "${envs[@]}" OMP_NUM_THREADS=$threads OMP_SCHEDULE=$sched OMP_PROC_BIND=false \
                   timeout 900 mpirun -np "$ranks" --bind-to none --oversubscribe "${mpiargs[@]}" "$BIN" "$m" "$TOL" "$ITERS" | grep '^matrix=' || true)
        else
            line=$(env "${envs[@]}" CPUS=$cpus OMP_NUM_THREADS=$threads OMP_SCHEDULE=$sched \
                   timeout 900 mpirun -np "$ranks" --bind-to none --oversubscribe "${mpiargs[@]}" src/bind.sh "$BIN" "$m" "$TOL" "$ITERS" | grep '^matrix=' || true)
        fi
        r1=$(pkg_uj); w1=$(date +%s.%N)
        erun=$(pkg_delta_j "$r0" "$r1"); wall=$(awk -v a="$w0" -v b="$w1" 'BEGIN { printf "%.3f", b - a }')
        done_n=$((done_n + 1))
        if [[ -z $line ]]; then echo "[$done_n/$total] FAILED $label $ranks x $threads $m" >&2; continue; fi
        echo "$line" | awk -v cols="$COLS" -v pre="$(date -Is),$rep,$label,${cpus//,/;},$ac,$cool,$load1,$wall,$erun" '
            { for (i = 1; i <= NF; i++) { split($i, kv, "="); v[kv[1]] = kv[2] } }
            END { n = split(cols, c, " "); s = pre
                  for (i = 1; i <= n; i++) { x = v[c[i]]; gsub(",", ";", x); s = s "," x }
                  print s }' >> "$OUT"
        t=$(sed -E 's/.* time_s=([0-9.]+).*/\1/' <<< "$line"); e=$(sed -E 's/.* e_pkg_j=([-0-9.]+).*/\1/' <<< "$line")
        printf '[%d/%d] rep%d %-5s %2dx%-2d %-11s %-14s t=%6.2fs E_pkg=%sJ cool=%ss\n' \
            "$done_n" "$total" "$rep" "$label" "$ranks" "$threads" "$sched" "$(basename "$m" .rcm.csr)" "$t" "$e" "$cool"
    done
done
echo "done -> $OUT"
