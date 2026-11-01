# Project status — 2026-11-01

**Project:** Energy-Performance Characterization of Hybrid MPI+OpenMP Sparse Iterative Solvers on Heterogeneous P-core/E-core Processors.

**Current state:** the solver, measurement harness and planned datasets are complete. Results and the original terminal screenshot are integrated into [the final report](report/PCAP_Final_Report.md). Authors will complete title-page details. RAPL access was available for the recorded energy experiments; it is a prerequisite to recheck after reboot, not an outstanding blocker for those results.

This document describes the current state and supersedes the earlier pilot-stage status notes. [README.md](README.md) contains setup and execution instructions.

## Research questions

| Question | Evidence and conclusion |
|---|---|
| RQ1: Does the fastest configuration minimise energy? | No, across the observed A/B means: different configurations minimise runtime and package energy on each matrix. The fastest uses 1.24–1.37× the minimum energy. |
| RQ2: At equal physical core counts, which type is preferable? | P-cores are faster in every matched A comparison. Energy depends on count and placement: four spread E-cores save 12.2–27.9% versus four P-cores but take 1.62–1.93× as long. |
| RQ3: Does unpinned execution match the best pinned configuration? | Not consistently for both runtime and energy. Results depend on matrix and thread count; small differences are not significance-tested wins. |

The contribution is an instrumented solver and experimental characterisation. The project does not introduce a new CG algorithm, and speed-aware partitioning remains future work.

## Implementation completed

- **Sparse inputs:** five SuiteSparse matrices loaded into CSR, with symmetric Matrix Market storage expanded and binary caches for repeated loading.
- **Correctness reference:** sequential, unpreconditioned CG; `b = A*1`, initial `x = 0`, exact solution all ones.
- **MPI solver:** contiguous row blocks balanced approximately by nonzero count; neighbour halo exchange; two global reductions per iteration.
- **OpenMP:** threaded SpMV and vector operations. SpMV supports runtime-selected static or dynamic scheduling; vector operations use static scheduling.
- **Reordering:** symmetric RCM permutation before measurement. It reduces halo sizes substantially for some matrices, but does not guarantee an improvement for every matrix.
- **Placement:** explicit CPU sets via `taskset`, `OMP_PLACES` and `OMP_PROC_BIND`, plus unpinned comparisons. The CPU map records end-of-solve placement, not full migration history.
- **Measurement:** rank 0 reads RAPL before and after the solve interval; records package/core/uncore/psys energy, temperature and throttle counters. Whole-invocation package energy is separately recorded by the sweep driver.
- **Automation:** shuffled repeated sweeps, metadata, raw CSVs, statistical summaries, plots and report generation.

Halo messages use nonblocking MPI calls followed by `MPI_Waitall` before SpMV; communication–computation overlap is not implemented. Equal nonzero work is not speed-aware when ranks run on different core types.

## Recorded experiments and coverage

| Dataset | Design | Actual observations | Role |
|---|---|---:|---|
| `pilot_runtime` | 10 configurations × 5 matrices × 3 repetitions | 150 | Initial runtime and variability checks |
| `pilot_energy` | 10 configurations × 5 matrices × 3 repetitions | 150 | Initial energy checks |
| A: `equalcount` | 11 configurations × 5 matrices, tolerance `1e-8` | 183 | Equal physical-core counts, 1–4, packed/spread E placement |
| B: `mixed` | 11 configurations × 5 matrices × 3 repetitions, tolerance `1e-8` | 165 | Mixed, full-chip, HT and unpinned configurations |
| C: `full` | 51 configurations × 5 matrices × 3 repetitions, 1,000 iterations | 765 | Programming-model split and scheduling survey |
| D: `spin` | 13 configurations × 3 matrices × 3 repetitions, 1,000 iterations | 117 | Waiting-policy comparisons |
| `converge` | 6 configurations × 5 matrices × 1 repetition | 30 | Earlier complete-solve check |
| `perf` | 7 configurations × 2 repetitions, thermal2, 2,000 iterations | 14 | Hardware-counter follow-up |

A retains 18 observations from an earlier invocation plus the complete 165-run invocation: 37 groups have `n=3`, and 18 have `n=4`. B has 55 groups with `n=3`. The repeated repetition labels are not unique session identifiers. No valid observation was dropped merely because it was slower or consumed more energy.

Fixed-iteration measurements are work-normalised comparisons; A/B are complete solves to a common residual target. These are related but different measurements. Identical iteration counts are not required in tolerance mode because parallel floating-point reduction order can affect convergence.

## Verified A/B results

All 348 A/B rows report convergence and meet the strict true-relative-residual bound of `1e-8` at the recorded precision. No A/B row records throttling or battery/unknown power. The maximum recorded absolute solution error is `1.530e-3` for G3_circuit; a small residual does not imply equally small forward error.

The following are arithmetic means. The report provides sample SDs; sweep reports instead use medians.

| Matrix | Fastest observed mean configuration | Time (s) | Minimum-energy mean configuration | Package energy (J) |
|---|---|---:|---|---:|
| G3_circuit | A16 1×16 (B) | 30.605 | E8 1×8 (B) | 578.60 |
| apache2 | P4 1×4 (B) | 9.851 | E8 1×8 (B) | 215.68 |
| cant | U16 1×16 (B) | 7.086 | E8 1×8 (B) | 194.63 |
| ecology2 | P4 1×4 (B) | 16.493 | E4s 1×4 (A) | 330.10 |
| thermal2 | U16 1×16 (B) | 17.548 | E8 1×8 (B) | 408.15 |

P4 observations from A and B are kept as separate groups rather than pooled across sessions. The small ecology2 E4s/E8 difference and close U16/A16 runtimes should not be presented as established superiority.

At one physical core, E1/P1 mean ratios are 1.77–2.11 for runtime and 1.09–1.22 for package energy. At four physical cores, E4s/P4 ratios are 1.62–1.93 for runtime and 0.72–0.88 for energy. E4s has the lowest mean energy on every matrix within A. P8ht/E8 comparisons use equal hardware-thread counts, not equal physical-core counts.

## Supplementary findings

- **MPI/OpenMP:** the M8 (4P+4E) and A12 (4P+8E) CPU sets in C use 1.51–1.76× the package energy with MPI-only versus OpenMP-only at similar runtimes. A16, which also uses P-core Hyper-Threading, instead has a 1.01–1.08× energy ratio.
- **Waiting evidence:** the measured M8/A12 OpenMP runs spend about 38% of measured P-core cycles in PAUSE; corresponding MPI runs spend 0.1–0.2% and execute many more P-core instructions. This supports a busy-polling explanation, not a direct attribution of every extra joule.
- **Counter scope:** `perf` measures selected CPUs system-wide over the invocation, including setup and potentially unrelated activity. The reported solver energy covers the solve interval. Two repetitions provide limited uncertainty information.
- **Waiting policies:** MPI yield saves 2.8–5.3% mean energy in the reported comparisons. Active OpenMP waiting raises mean energy by at most 4.3%. Passive A12 takes 3.01–3.49× the default-wait runtime; lower power does not guarantee lower energy.
- **Dynamic scheduling:** in the reported C comparisons, it increases energy by roughly 2–46%; runtime improvements occur only on cant for some configurations.
- **Communication:** C's largest group-median halo fraction is 7.14% for pinned configurations and 25.12% overall (apache2, U16 4×4). Halo time is separate from collective-reduction time.

## Validation performed

- Fresh compilation of all five programs and shell-script syntax checks passed.
- Sequential Poisson checks: 64×64 converged in 135 iterations, and 256×256 in 526, with true relative residuals approximately `9.64e-11` and `9.84e-11` respectively.
- A 2-rank × 2-thread Poisson 64×64 run converged in 135 iterations with matching residual accuracy.
- RCM-reordered Poisson 64×64 also converged correctly.
- Raw-data means, sample SDs and medians match the equalcount, mixed, full and spin summary CSVs within output rounding.
- The 550 added mean/SD values in report Tables 6.3–6.5 were checked against raw rows, along with sample counts, correctness data and scheduler comparisons. Supplementary split/scheduling and waiting-policy tables were also checked.
- `perf_summary.md` was reproduced exactly from the stored counter/run files.
- All 25 fully visible times and energies in the selected terminal screenshot match the equalcount CSV. Its 165-run progress denominator refers to one invocation, not all 183 retained rows.
- Report generation is reproducible from the current Markdown source; referenced images exist.

These checks are not an exhaustive proof for arbitrary inputs, an independent experimental replication or complete verification of the external literature.

## Limitations and objectives

| Objective / condition | Current status |
|---|---|
| O1: implement and validate the solver | Achieved for the recorded A/B workloads and tested synthetic cases |
| O2: measurement harness and pinned CV below 2% | Partly achieved: harness complete, but some groups exceed the CV target |
| O3: equal-count and separate mixed comparisons | Achieved, with actual sample counts disclosed |
| O4: answer RQ1–RQ3 | Addressed descriptively, with measurement and statistical limits stated |

Median pinned-group CVs are 0.52% runtime / 0.66% energy in A, and 0.15% / 0.25% in B. These medians conceal higher-variability groups: A reaches 21.84% energy CV. C's median group CVs are 0.31% runtime / 0.70% energy, keeping static and dynamic schedules separate.

The sweep checks a ≤55 °C target before launch, with a nominal 120 s wait limit. Two-second polling can overshoot that limit; A records a maximum cooldown of 121 s. Solve-start temperature is recorded after setup: it exceeds 55 °C in 180/183 A rows and 165/165 B rows, with maxima of 74 °C and 67 °C. The absence of recorded throttle events does not establish identical frequency or thermal conditions.

Other limits include one platform, one MPI implementation, small samples, unequal A sample counts, package-level rather than per-core or wall-plug energy, no DRAM domain, and a constructed RHS with no preconditioner. A matrix exceeding cache capacity alone does not prove bandwidth saturation. Cache contention and the exact polling mechanism have not been fully isolated by controlled measurements.

## Remaining work

The following are open issues, not completed fixes:

1. **Analysis correctness:** reconcile the `1.05 * tol` diagnostic with the generated `<= tol` wording; reject or explicitly flag nonfinite/unknown measurements. A/B separately pass the strict recorded bound.
2. **Automatic comparison wording:** distinguish physical cores from hardware threads; name RQ3 runtime and energy references separately; label the 3% tie rule as a heuristic rather than a significance test.
3. **Sweep completeness:** preserve structured failure records, validate expected coverage, add session identifiers and explicit resume/new-run behaviour. Currently a failed job can be skipped while the script still prints `done`.
4. **Exit status and tests:** tolerance-mode nonconvergence currently returns exit code zero. Add numerical assertions and hybrid/input-failure tests; `make test` is presently limited to sequential examples.
5. **Report reproducibility:** automate data-to-table/prose generation. `build_report.py` renumbers citations; it does not recalculate numerical content after data changes.
6. **Literature and claims:** resolve outstanding full-text checks recorded in `citations_verified.md` and distinguish supported interpretations from isolated causal findings.
7. **Presentation:** authors will complete the title-page details and prepare the final document format.

Future experimental work could add speed-aware partitioning, more independent sessions and tighter thermal controls, direct bandwidth measurements, other processors/MPI implementations, preconditioners, and alternative waiting strategies. These extensions are not part of the completed implementation.

## Reproduction guidance

Follow [README.md](README.md). Use new output paths rather than appending to the published CSVs. Recheck RAPL access after reboot, preserve power settings, and inspect run coverage and numerical output rather than relying on exit status or a `done` message. Preserve raw data and metadata, then reconcile summaries, figures and report prose together.
