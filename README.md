# Hybrid MPI+OpenMP CG on P-core/E-core: energy-performance study

Machine: Intel Core i5-13500H. P-cores = logical CPUs 0-7 (HT pairs 0-1, 2-3, 4-5, 6-7),
E-cores = CPUs 8-15 (L2 shared by 8-11 and by 12-15). Ubuntu 22.04, OpenMPI 4.1.2, GCC 11.4.

## Layout

| Path | What |
|---|---|
| `src/csr.[ch]` | CSR matrix, Matrix Market reader, binary `.csr` cache, nnz-balanced row-block loader |
| `src/cg_seq.c` | Sequential CG: correctness reference + single-core baseline |
| `src/cg_hybrid.c` | Hybrid MPI+OpenMP CG with RAPL/temperature/throttle metering around the solve loop |
| `src/rcm.c` | Reverse Cuthill-McKee reordering -> `*.rcm.csr` |
| `src/rapl.[ch]`, `src/rapl_idle.c` | RAPL powercap reader; idle power baseline |
| `src/bind.sh` | Per-rank pinning: rank r gets `CPUS[r*T .. r*T+T-1]`, threads pinned via `OMP_PLACES` |
| `configs/{pilot,full}.txt` | Sweep configurations (`label cpus ranks threads sched`) |
| `sweep.sh` | Runs a config file over all matrices x reps, appends one CSV row per run |
| `analyze.py` | Medians, quality checks, RQ1-RQ3 lines, plots |
| `matrices/` | SuiteSparse SPD matrices (+ `.rcm.csr` reordered versions used in the sweep) |
| `citations_verified.md` | Citation checks and corrections |

## One-time setup

```bash
cd src && make && cd ..
./get_matrices.sh      # downloads 5 SuiteSparse matrices (~430 MB) and builds the RCM-reordered .rcm.csr files
```

RAPL counters are root-only by default (deliberately, because of CVE-2020-8694 / PLATYPUS).
Allow reading until the next reboot:

```bash
sudo chmod o+r /sys/class/powercap/intel-rapl:*/energy_uj /sys/class/powercap/intel-rapl:*:*/energy_uj
```

Before a sweep: plug in AC power, close other apps, keep the same power profile for the whole sweep
(`sweep.sh` records governor/EPP/turbo/platform profile in `<out>.meta.txt`).

## Running

```bash
# single run, pinned: 2 ranks x 2 threads on the 4 P-cores, 1000 fixed iterations
CPUS=0,2,4,6 OMP_NUM_THREADS=2 OMP_SCHEDULE=static mpirun -np 2 --bind-to none src/bind.sh src/cg_hybrid matrices/thermal2/thermal2.rcm.csr 0 1000

# sweeps
REPS=3 ITERS=300 OUT=results/pilot.csv ./sweep.sh configs/pilot.txt
REPS=3 ITERS=1000 OUT=results/full.csv ./sweep.sh configs/full.txt   # ~2.5 h
python3 analyze.py results/full.csv

# experiments added after the synopsis review (equal-core-count P vs E, mixed configs; tol 1e-8; ~4 h)
./revision_runs.sh
python3 report/make_figures.py && python3 report/build_report.py
```

`cg_hybrid <matrix> <tol> <maxit>`: `tol = 0` runs exactly `maxit` iterations (used for all
measurements so every config does identical work).
