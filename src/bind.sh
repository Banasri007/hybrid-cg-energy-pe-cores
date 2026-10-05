#!/usr/bin/env bash
# Per-rank CPU pinning wrapper for Open MPI.
#   CPUS="0,2,4,6" OMP_NUM_THREADS=2 mpirun -np 2 --bind-to none ./bind.sh ./cg_hybrid ...
# Rank r (node-local) gets CPUS[r*T .. r*T+T-1], T = OMP_NUM_THREADS:
#   - the process is restricted to those CPUs (taskset)
#   - each OpenMP thread is pinned to one of them (OMP_PLACES + OMP_PROC_BIND=close)
set -euo pipefail
r=${OMPI_COMM_WORLD_LOCAL_RANK:?bind.sh must be launched by Open MPI mpirun}
T=${OMP_NUM_THREADS:?set OMP_NUM_THREADS}
IFS=, read -ra all <<< "${CPUS:?set CPUS to a comma-separated CPU list}"
need=$(( (r + 1) * T ))
if (( need > ${#all[@]} )); then
    echo "bind.sh: rank $r needs $need CPUs but CPUS has ${#all[@]}" >&2
    exit 1
fi
mine=("${all[@]:r*T:T}")
places=$(printf '{%s},' "${mine[@]}")
export OMP_PLACES=${places%,}
export OMP_PROC_BIND=close
exec taskset -c "$(IFS=,; echo "${mine[*]}")" "$@"
