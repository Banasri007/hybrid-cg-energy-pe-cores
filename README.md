# Hybrid MPI+OpenMP CG on P-core/E-core processors

An experimental study of runtime and processor-package energy for an unpreconditioned Conjugate Gradient (CG) solver on an Intel Core i5-13500H. The project compares P-core, E-core, mixed and unpinned execution, including MPI/OpenMP splits and OpenMP scheduling policies.

**Status:** experiments are complete and their results are integrated into the [final report](report/PCAP_Final_Report.md). See [PROJECT_STATUS.md](PROJECT_STATUS.md) for verified findings, limitations and remaining work. Title-page details remain for the authors to complete.

## Research questions and findings

- **RQ1 — runtime versus energy:** the fastest and lowest-energy observed mean configurations differ on all five matrices. Across Experiments A/B, the fastest choice uses 1.24–1.37× the energy of the minimum-energy choice.
- **RQ2 — equal physical core counts:** P-cores are faster in every matched comparison. Four E-cores spread across both E-modules save 12.2–27.9% package energy versus four P-cores, while taking 1.62–1.93× as long.
- **RQ3 — default scheduling:** unpinned execution does not consistently match both the best pinned runtime and the best pinned energy.
- **MPI/OpenMP split:** in the fixed-work survey, the mixed physical-core sets M8 (4P+4E) and A12 (4P+8E) use 1.51–1.76× the package energy with MPI-only versus OpenMP-only at similar runtimes. This range does not apply to A16: its corresponding energy ratio is 1.01–1.08×. Waiting-policy experiments and hardware counters support a busy-polling explanation; they do not isolate every source of energy consumption.

These are results for one processor, software stack and set of five matrices. Small differences are descriptive rankings, not significance-tested superiority claims.

## Recorded platform

Intel Core i5-13500H; Ubuntu 22.04; Open MPI 4.1.2; GCC 11.4.

| Resource | CPU IDs used in this project |
|---|---|
| Four physical P-cores, with Hyper-Threading | 0–7; sibling pairs 0–1, 2–3, 4–5, 6–7 |
| Eight physical E-cores | 8–15 |
| E-core modules, each sharing L2 | 8–11 and 12–15 |

The recorded policy was `powersave`, EPP `balance_performance`, turbo enabled, platform profile `balanced`, on AC power. **CPU numbering and RAPL paths are machine-specific:** inspect the target machine before reusing the configuration files.

## Repository layout

| Path | Purpose |
|---|---|
| `src/csr.[ch]` | CSR storage, Matrix Market reader, binary cache and nonzero-balanced row-block loading |
| `src/cg_seq.c` | Sequential CG correctness reference |
| `src/cg_hybrid.c` | MPI+OpenMP CG with solve-interval energy, temperature and throttle measurements |
| `src/rcm.c` | Reverse Cuthill–McKee reordering |
| `src/rapl.[ch]`, `src/rapl_idle.c` | RAPL counters and idle-power measurements |
| `src/bind.sh` | Explicit rank/thread placement |
| `configs/` | CPU placement, rank/thread split, schedule and optional waiting-policy settings |
| `sweep.sh` | Shuffled repeated runs, CSV output and metadata |
| `revision_runs.sh`, `extra_runs.sh` | Convenience launchers for the A/B and follow-up experiments |
| `perf_check.sh`, `perf_summary.py` | Hardware-counter experiment and summary |
| `analyze.py` | Summary CSVs, median-based sweep reports and plots |
| `results/` | Recorded data, metadata, summaries and plots |
| `report/report_src.md` | Editable report source |
| `report/build_report.py`, `report/make_figures.py` | Citation renumbering/report build and figure generation |
| `citations_verified.md` | Citation-check record, including unresolved full-text checks |
| `matrices/` | Downloaded matrices and binary caches; excluded from Git |

## Setup

Requirements: Linux, GCC, Make, Open MPI development tools/runtime, Python 3 with NumPy and Matplotlib, and the standard shell tools used by the scripts (`curl`, `tar`, `taskset`, `shuf`, `timeout`, `awk`). Hardware-counter experiments additionally require `perf` and suitable event permissions.

From the repository root:

```bash
make -C src
make -C src test
./get_matrices.sh
```

The download script obtains thermal2, G3_circuit, ecology2, apache2 and cant from SuiteSparse, then creates the RCM-reordered `.rcm.csr` inputs. `make test` runs two sequential Poisson examples; inspect their convergence and residual output. It is not a complete automated hybrid test suite.

For energy measurements, the RAPL counters must be readable. On the recorded machine, the following grants read access until reboot (and makes those counters readable by other local users):

```bash
sudo chmod o+r /sys/class/powercap/intel-rapl:*/energy_uj /sys/class/powercap/intel-rapl:*:*/energy_uj
src/rapl_idle 5
```

The solver itself runs without root privileges. If RAPL is unavailable, the solver can still run but reports unavailable energy as `-1`; the A/B convenience launcher checks for readable RAPL. That check can succeed when any discovered domain is readable, so also confirm that `p_pkg_w` from `rapl_idle` and the solver’s `e_pkg_j` are nonnegative before treating a run as a package-energy measurement.

## Solver modes and single runs

```text
cg_hybrid <matrix.mtx | matrix.csr | poisson:M> [tol] [maxit]
```

- **Tolerance mode:** positive `tol`; solve until the recursive residual meets the threshold or `maxit` is reached. A/B use `1e-8` with a 20,000-iteration cap. Check the independently recomputed `true_rel_res` and `converged` fields.
- **Fixed-work mode:** `tol=0`; request `maxit` iterations. C/D use 1,000 iterations, and the counter experiment uses 2,000. Verify the recorded iteration count: an exactly zero residual or numerical breakdown can terminate the loop early.

A tolerance-mode solve on the four physical P-cores, using two ranks with two threads each:

```bash
CPUS=0,2,4,6 OMP_NUM_THREADS=2 OMP_SCHEDULE=static \
  mpirun -np 2 --bind-to none src/bind.sh src/cg_hybrid \
  matrices/thermal2/thermal2.rcm.csr 1e-8 20000
```

For a fixed-work run, replace the final two arguments with `0 1000`. The RHS is `b = A*1`, the initial guess is zero, and the known exact solution is the all-ones vector. No preconditioner is used.

## Recorded experiments

| Dataset | Purpose | Recorded runs |
|---|---|---:|
| `pilot_runtime.csv` / `pilot_energy.csv` | Initial runtime / energy pilots | 150 each |
| `equalcount.csv` — A | 11 configurations × 5 matrices, tolerance mode | 183 |
| `mixed.csv` — B | 11 configurations × 5 matrices × 3 repetitions, tolerance mode | 165 |
| `full.csv` — C | 51 configurations × 5 matrices × 3 repetitions, fixed 1,000 iterations | 765 |
| `spin.csv` — D | 13 configurations × 3 matrices × 3 repetitions, fixed 1,000 iterations | 117 |
| `converge.csv` | Earlier complete-solve check, 6 configurations × 5 matrices × 1 repetition | 30 |
| `perf/` | 7 configurations × 2 repetitions, thermal2, 2,000 iterations | 14 |

A contains 18 earlier observations in addition to a complete 165-run invocation: 37 groups have three observations and 18 have four. All valid observations were retained. All 348 A/B runs converged and meet the recorded true-residual bound of `1e-8`; none recorded a throttle event or battery/unknown-power state.

### Running a new sweep

Keep the laptop on AC power, close unrelated applications and preserve the power policy. **Use an unused output filename for each new invocation.** The script appends to existing CSVs and restarts repetition labels; it does not automatically resume missing jobs.

For example, after confirming these output paths do not exist:

```bash
REPS=3 TOL=1e-8 ITERS=20000 OUT=results/equalcount_new.csv \
  ./sweep.sh configs/equalcount.txt
python3 analyze.py results/equalcount_new.csv

REPS=3 TOL=1e-8 ITERS=20000 OUT=results/mixed_new.csv \
  ./sweep.sh configs/mixed.txt
python3 analyze.py results/mixed_new.csv

REPS=3 TOL=0 ITERS=1000 OUT=results/full_new.csv \
  ./sweep.sh configs/full.txt
python3 analyze.py results/full_new.csv
```

`revision_runs.sh` uses the existing `results/equalcount.csv` and `results/mixed.csv` paths. `extra_runs.sh` uses `results/spin.csv` and `results/converge.csv`. Running those launchers again will append to the recorded datasets. `perf_check.sh` reuses its per-repetition output filenames. Preserve the published data before rerunning any of these launchers.

After a sweep, check expected group coverage, sample counts, iteration counts and energy availability. For tolerance-mode runs, also require convergence and a true residual within the target. A fixed-work run normally reports `converged=0` because its tolerance is zero; assess its requested iteration count and finite numerical output instead. The script can skip failed jobs and still print `done`; that message alone does not establish completeness.

## Measurement and interpretation

- Rank 0 takes two RAPL snapshots around the solve interval. Package energy is **not summed across ranks**. Matrix loading and setup are excluded; `e_pkg_run_j` is a separate measurement around the whole `mpirun`.
- Package energy is not wall-plug energy, and the available RAPL domains must not be added together as independent components. There is no separate P/E-core energy measurement or DRAM domain in this setup.
- The sweep targets ≤55 °C **before launch**, waiting at least 5 s with a nominal 120 s limit. Two-second polling can overshoot that limit; the maximum logged cooldown in A is 121 s. Setup can heat the processor before the solve. A/B recorded solve-start maxima of 74 °C / 67 °C; no throttle events were recorded, but temperature remains a potential confounder.
- The recorded exclusion rule removes runs with `throttle_delta > 0` or `ac_online != 1`. Slow runs are not selectively removed. Unknown throttle telemetry is not automatically rejected by the current analyzer.
- `results/idle_baseline.txt` is a separately measured clean baseline (0.34 W package). It differs from per-invocation startup measurements and is used for optional dynamic-energy estimates. Main report energy tables use measured package energy without idle subtraction.
- Summary CSVs contain means, sample SDs and medians. Sweep reports use **medians**; the final A/B tables use **mean ± sample SD**, with actual sample counts. Ratios can therefore differ between these outputs.
- P8ht versus E8 is an equal-hardware-thread comparison, not an equal-physical-core comparison. E4s means four E-cores spread across two modules.

## Reports and current limitations

```bash
python3 report/make_figures.py
python3 report/build_report.py
```

The figure script reads existing summaries. The report builder renumbers citations and creates `PCAP_Final_Report.md` from `report_src.md`; **it does not recalculate the report's numerical tables or prose**. If raw data change, regenerate the relevant summaries and reconcile the report source before rebuilding.

Automatic RQ3 lines may name the runtime-optimal configuration while quoting energy from a different configuration; the final report names the references separately. The automatic “tie within 3%” label is a heuristic, not a significance test.

The study uses one platform and small samples; some groups exceed the 2% CV target. Cache and waiting mechanisms are supported interpretations rather than fully isolated causal measurements. See [PROJECT_STATUS.md](PROJECT_STATUS.md) and the [final report](report/PCAP_Final_Report.md) for the remaining validation and reproducibility work.
