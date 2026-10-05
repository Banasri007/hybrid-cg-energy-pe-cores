# Project status — 2026-10-04

**Title:** Energy-Performance Characterization of Hybrid MPI+OpenMP Sparse Iterative Solvers on Heterogeneous P-core/E-core Processors

## 1. What we are doing (one paragraph)

We built a Conjugate Gradient (CG) solver for sparse symmetric positive-definite systems that runs as several MPI processes, each with several OpenMP threads, on one Intel i5-13500H laptop CPU. That CPU has two kinds of cores: 4 fast **P-cores** (with hyper-threading, logical CPUs 0–7) and 8 slower, smaller **E-cores** (CPUs 8–15). We run the same solve under many configurations — how many MPI ranks × OpenMP threads, which cores they are pinned to (P only, E only, mixed, or left to Linux), and the OpenMP loop schedule — and for each run we record the time and the CPU energy (Intel RAPL counters). The question is which configuration is fastest, which uses the least energy, whether those differ, and whether E-cores' reputation for energy efficiency on memory-heavy work holds for a real sparse solver.

## 2. Research questions

| | Question | Status |
|---|---|---|
| RQ1 | Does the fastest process×thread configuration also use the least energy? | runtime data in; energy blocked on RAPL permission |
| RQ2 (main contribution) | At equal core count, do P-cores or E-cores give lower energy-to-solution for memory-bound sparse CG, and does it depend on the matrix? | runtime data in; energy pending |
| RQ3 | Does the default Linux scheduler (no pinning) match the best hand-pinned configuration? | runtime: **yes, within 0–10%**; energy pending |

## 3. Pipeline — exact steps and where we are

| # | Step | Status | Where |
|---|---|---|---|
| 1 | Verify hardware: RAPL domains, P/E core IDs, caches | ✅ done | §5 |
| 2 | Check the two papers our gap depends on | ✅ gap survives (Velugoti et al. arXiv:2608.23165 is OpenMP-only, no energy, read in full); Wlotzka & Heuveline (the paper the handoff called "Kuhn") still needs a full read through library access | `citations_verified.md` |
| 3 | Verify all citations against Crossref/arXiv | ✅ metadata done, 7 corrections; some claims still need full-text checks (marked ⚠) | `citations_verified.md` |
| 4 | Toolchain: OpenMPI + GCC/OpenMP hybrid hello-world | ✅ | `src/hello_hybrid.c` |
| 5 | Get 5 SPD test matrices from SuiteSparse | ✅ | `matrices/` |
| 6 | Sequential CG baseline + correctness check | ✅ error ~1e-10 vs known solution | `src/cg_seq.c` |
| 7 | MPI row-block CG + halo exchange + Allreduce | ✅ identical iteration count for every split tried | `src/cg_hybrid.c` |
| 8 | OpenMP threading inside each rank (static / dynamic) | ✅ | `src/cg_hybrid.c` |
| 9 | RCM reordering of matrices | ✅ checked against SciPy | `src/rcm.c` |
| 10 | Per-rank core pinning wrapper | ✅ checked with hello-world | `src/bind.sh` |
| 11 | RAPL + temperature + throttle metering in the solver; idle-power tool | ✅ code done, **can't take energy readings until RAPL is made readable (needs your sudo)** | `src/rapl.c`, `src/rapl_idle.c` |
| 12 | Sweep driver (one command → one CSV) | ✅ | `sweep.sh`, `configs/` |
| 13 | Analysis + plots | ✅ | `analyze.py` |
| 14 | Runtime-only pilot (10 configs × 5 matrices × 3 reps) | ✅ 150/150 runs, 0 throttled | `results/pilot_runtime*` |
| 15 | Pilot with energy | ✅ 150 runs | `results/pilot_energy*` |
| 16 | Full sweep (51 configs × 5 matrices × 3 reps) | ✅ 765/765 runs, 0 throttled, identical iteration counts | `results/full*` |
| 17 | Write final report (17 sections) as .docx | ⏳ | |

## 4. How it works (methodology as built)

**Solver.** Unpreconditioned CG on matrices in CSR format. Right-hand side `b = A·1`, so the exact solution is all ones and the error can be checked directly. Start from `x = 0`.

**MPI layer.** Rows are split into contiguous blocks, one per rank, sized so each rank gets about the same number of nonzeros. Each iteration:
1. Halo exchange: each rank receives the entries of the search direction `p` that its rows reference but another rank owns (`MPI_Isend`/`MPI_Irecv`, neighbours only).
2. Local sparse matrix-vector product `Ap`.
3. `MPI_Allreduce` #1: `p·Ap` → step size α.
4. Update `x` and `r`, and compute `r·r` in the same loop.
5. `MPI_Allreduce` #2: `r·r` → convergence check and β.
6. Update `p`.

The handoff said 3 Allreduces per iteration; 2 suffice because one `r·r` gives both the residual norm and β.

**OpenMP layer.** Inside each rank, SpMV and the vector updates are threaded. The SpMV loop schedule comes from `OMP_SCHEDULE` (`static` or `dynamic,64`), so the sweep can switch it without recompiling.

**Fixed-iteration mode.** Every measured run does exactly N iterations (`tol = 0`). Every configuration then does identical arithmetic work, so a configuration can't look cheaper just by converging in fewer iterations. The analysis script still checks that iteration counts are identical.

**RCM reordering.** The original row order of some matrices scatters nonzeros far from the diagonal, so a row-block split makes each rank need a huge halo. Reverse Cuthill–McKee renumbers rows to keep nonzeros near the diagonal. Every matrix is reordered once and the reordered `.rcm.csr` files are used for all runs.

| matrix | rows | nnz | max halo per rank at 8 ranks: original → RCM |
|---|---|---|---|
| thermal2 | 1.23 M | 8.6 M | 219,892 → 1,369 |
| G3_circuit | 1.59 M | 7.7 M | 213,243 → 9,585 |
| ecology2 | 1.00 M | 5.0 M | 2,000 → 1,866 |
| apache2 | 0.72 M | 4.8 M | 4,817 → 6,517 |
| cant | 0.06 M | 4.0 M | 550 → 586 |

The first two were badly ordered; the other three were already banded, and RCM is roughly neutral for them. Our bandwidths are comparable to SciPy's RCM (thermal2: 925 vs 842; G3_circuit: 5,068 vs 8,017). CG on thermal2 converges in 4331 iterations after reordering vs 4333 before.

**Pinning.** `src/bind.sh` gives rank r the CPUs `CPUS[r·T … r·T+T−1]`. It restricts the process with `taskset` and pins each thread with `OMP_PLACES` + `OMP_PROC_BIND=close`. Unpinned runs use no wrapper and `OMP_PROC_BIND=false`.

**Energy metering.** Rank 0 reads the RAPL counters for package, core, uncore and psys (the whole platform) straight after a barrier at the start of the solve and again after a barrier at the end. Setup and file loading are excluded. Counter wraparound is handled. The same snapshots record:
- package temperature;
- the kernel's thermal-throttle event counters (any increase means the run was throttled and is excluded);
- the CPU each thread finished on.

`rapl_idle` measures idle power so idle draw can be subtracted later.

**Sweep.** `sweep.sh` repeats every (matrix, config) pair, shuffling the order within each repetition so slow drift (heat soak, background load) doesn't bias any one config. Before each run it waits at least 5 s and until the package is ≤ 55 °C. It appends one CSV row per run and writes the power settings (governor, EPP, turbo, AC power) to a `.meta.txt`.

**Configurations** (`configs/full.txt`, 51 in total):
- **Single core:** P1 vs E1.
- **4 physical cores:** P4 (0,2,4,6) vs E4 (8–11, one E-module) vs E4s (8,9,12,13, spread over both E-modules), each as 4×1, 2×2 and 1×4.
- **8 hardware threads:** P8ht (4 P-cores + hyper-threads) vs E8 vs M8 (4P+4E), each as 8×1, 4×2, 2×4 and 1×8.
- **All cores:** A12 (all 12 physical cores) and A16 (all 16 threads) at every split.
- **Unpinned:** 12 configurations.
- **Dynamic schedule:** `dynamic,64` for single-rank runs whose threads span different core types.

## 5. Hardware facts (verified on the machine)

- P-cores: CPUs 0–7 (hyper-thread pairs 0-1, 2-3, 4-5, 6-7), 1.25 MB L2 each, up to 4.7 GHz.
- E-cores: CPUs 8–15, up to 3.5 GHz, two modules (8–11 and 12–15), each sharing 2 MB L2.
- L3: 18 MB shared by all cores. All five matrices are larger than L3, so the solver is memory-bound.
- AVX2 on all cores, no AVX-512. One socket, no NUMA.
- RAPL domains: package-0, core, uncore, psys. **No DRAM domain** on this mobile chip, so DRAM energy was dropped from the methodology; psys is logged instead. The core domain covers all cores together; there is no separate P or E reading.
- `energy_uj` is root-only (a deliberate kernel default since CVE-2020-8694). **This is the current blocker.**
- Default power settings: `powersave` governor, `balance_performance` EPP, turbo on. These are recorded per sweep and must stay the same across it.

## 6. Results so far (runtime only, 300 iterations, median of 3 runs)

Full tables: `results/pilot_runtime_report.md`. Plots: `results/pilot_runtime_plots/`.

Solve time in seconds:

| config | ecology2 | apache2 | thermal2 | G3_circuit | cant |
|---|---|---|---|---|---|
| P1 (1 P-core) | 1.84 | 1.53 | 3.78 | 3.09 | 0.78 |
| E1 (1 E-core) | 3.34 | 2.86 | 6.55 | 5.42 | 1.63 |
| P4 4×1 | **0.83** | 0.62 | 1.37 | 1.46 | 0.30 |
| P4 1×4 | 0.85 | **0.61** | 1.37 | **1.44** | **0.28** |
| E4 4×1 | 2.22 | 1.80 | 2.82 | 3.53 | 0.74 |
| M8 8×1 (4P+4E) | 1.13 | 0.90 | 1.63 | 1.86 | 0.39 |
| A12 12×1 (all cores) | 0.90 | 0.71 | **1.36** | 1.56 | 0.30 |
| U4 unpinned 4×1 | 0.84 | 0.65 | 1.37 | 1.54 | 0.31 |
| U12 unpinned 12×1 | 0.90 | 0.73 | 1.37 | 1.56 | 0.30 |

**Data quality:** all 150 runs kept, none throttled, all on AC power, iteration counts identical for every config of each matrix. Run-to-run variation (CV) is under 2% for most configs, but up to 15% for runs shorter than 0.4 s. That's why the full sweep uses 1000 iterations.

**What the numbers say:**

1. **Memory-bandwidth wall at about 4 P-cores.** 4 P-cores already reach 2.1–2.8× over one P-core. Adding the 8 E-cores (A12) gives no further speedup: it's 0.99–1.16× the P4 time. The extra cores add no speed but presumably add power, so RQ1's runtime optimum and energy optimum are likely to differ. That's a hypothesis until energy is measured.
2. **E-cores are much slower than the single-core gap suggests.** One E-core takes 1.7–2.1× as long as one P-core, but 4 E-cores take 2.1–2.9× as long as 4 P-cores. 4 E-cores only get 1.5–2.3× over one E-core. The E4 set (8–11) is one module sharing one L2 and one ring stop, so that module's bandwidth may be the limit. The new E4s config (spread over both modules) tests this.
3. **Mixing P and E is slower than using P alone.** M8 (4P+4E, 8 ranks) takes 1.19–1.46× as long as P4. Every rank gets equal work, so the P-core ranks finish early and wait for the E-core ranks: in M8/A12, 40–50% of the solve time is spent inside `MPI_Allreduce`, mostly waiting. Splitting work evenly across unequal cores is a real flaw of the standard row-block method on hybrid CPUs.
4. **MPI vs OpenMP split barely matters for runtime here.** P4 4×1 vs 1×4 differ by ≤ 6%. On one shared-memory node there is little to choose between them; any difference will have to show up in energy (e.g. MPI ranks busy-wait while waiting for messages).
5. **RQ3 (runtime): the Linux scheduler does fine.** Unpinned runs are within 0–10% of the best pinned run. The CPU map shows that, left alone, 4-thread jobs mostly land on 4 separate P-cores, so Linux already prefers P-cores. 12-thread jobs spread over 4 P + 8 E like A12.

**How this connects to RQ2:** Żytko & Badurowicz report E-cores up to 17% more energy-efficient on memory-intensive microbenchmarks. Here, on a memory-bound sparse solver, E-cores are 2–3× slower at equal core count. To win on energy they'd have to draw less than about ⅓–½ of the P-cores' package power. The package total includes the uncore, ring and L3, which draw power no matter which cores are busy, so that's a high bar. This is exactly what the energy sweep will decide.


## 6b. Full sweep results (1000 iterations, median of 3, package energy) — supersedes §6 where they differ

Ratios are relative to P4 1×4 (4 P-cores, OpenMP only). Full tables: `results/full_report.md`, `results/full_summary.csv`.

| config | thermal2 t / E | G3_circuit t / E | ecology2 t / E | apache2 t / E | cant t / E |
|---|---|---|---|---|---|
| E4 1×4 (one E-module) | 2.09 / 0.94 | 2.63 / 1.06 | 2.88 / 1.13 | 2.75 / 1.06 | 2.45 / 0.97 |
| E4s 1×4 (2 per module) | 1.60 / 0.77 | 1.71 / **0.70** | 1.84 / **0.73** | 1.71 / 0.80 | 1.60 / 0.86 |
| E8 1×8 (all E-cores) | 1.28 / **0.73** | 1.44 / 0.71 | 1.57 / 0.74 | 1.49 / **0.73** | 1.38 / **0.69** |
| P8ht 1×8 (4 P + HT) | 0.96 / 0.90 | 1.06 / 0.90 | 1.02 / 0.89 | 0.90 / 0.92 | 0.82 / 0.94 |
| A12 12×1 (all cores, MPI only) | 0.99 / 1.47 | 1.09 / 1.60 | 1.09 / 1.60 | 1.02 / 1.61 | 0.92 / 1.49 |
| A12 1×12 (all cores, OpenMP only) | 0.99 / 0.96 | 1.07 / 0.95 | 1.11 / 1.01 | 1.03 / 0.98 | 0.91 / 0.98 |
| A16 1×16 (all 16 threads) | **0.90** / 0.93 | **0.98** / 0.89 | **0.99** / 0.89 | **0.89** / 0.89 | **0.71** / 0.96 |
| M8 8×1 (4P+4E, MPI only) | 1.18 / 1.51 | 1.29 / 1.66 | 1.38 / 1.79 | 1.27 / 1.76 | 1.15 / 1.54 |
| U8 1×8 (unpinned) | 1.05 / 0.93 | 1.11 / 0.95 | 1.13 / 0.97 | 1.05 / 0.97 | 0.97 / 1.01 |

Findings:
1. **RQ1 — the optima diverge on every matrix.** Fastest = all 16 threads in one rank (A16 1×16, or unpinned 16). Lowest energy = E-cores only (E8 on 3 matrices, E4s on 2). The fastest config costs 1.22–1.40× the energy of the most frugal one, which is 1.4–1.9× slower.
2. **RQ2 — E-cores win on energy, but only when spread across both E-modules.** E4 packed into one module (8–11) is 2.1–2.9× slower than P4 and about energy-neutral (0.94–1.13×). The same 4 cores spread 2+2 across modules (E4s) are 1.3–1.6× faster than packed and use 0.70–0.86× the energy of P4. All 8 E-cores: 0.69–0.74×. The per-module (shared L2 / ring stop) bandwidth limit confirmed the pilot's hypothesis, and it reverses the pilot's mostly-negative RQ2 result. Single E-core vs single P-core still loses (1.07–1.22×).
3. **New: pure MPI wastes energy on a hybrid CPU.** With P and E cores mixed, MPI-only and OpenMP-only take the same time, but MPI-only uses about 1.5–1.7× the energy (A12 12×1 vs 1×12, M8 8×1 vs 1×8). On P-cores alone the split is energy-neutral. Likely mechanism: fast P-core ranks busy-poll inside `MPI_Allreduce` (38–50% of runtime) waiting for slow E-core ranks, at full power. Mechanism confirmed with hardware counters (§6c): P-core ranks busy-poll Open MPI's shared-memory queues while waiting for E-core ranks, without PAUSE.
4. **Hyper-threading helps** on memory-bound CG: P8ht is 0.82–1.06× the time and 0.89–0.94× the energy of P4.
5. **Dynamic schedule is worse on energy**: `dynamic,64` costs 8–19% more energy than static for mixed 1×8, and is faster only on cant.
6. **RQ3 — Linux optimises for speed, not energy.** Unpinned 16 threads matches pinned A16 exactly. At 4 and 8 threads, Linux puts threads on P-cores. That's ≈ P4/P8ht speed, but 1.16–1.47× the energy of the best pinned E-core config at the same thread count.

**Idle baseline:** the reading taken at the start of the full sweep (13.1 W, 60 °C) had background load. A clean re-measurement with apps closed gave **0.34 W package / 0.81 W psys** at 38 °C (`results/idle_baseline.txt`). `analyze.py` now uses it, so `e_dyn` in `full_summary.csv` is valid. Idle is under 2% of any run's energy, so ratios between configs barely change.

## 6c. Follow-up experiments (2026-10-04)

**Spin test** (`results/spin*`; thermal2, G3_circuit, ecology2; 1000 iterations; 3 reps). Package energy in J:

| config | thermal2 | G3_circuit | ecology2 |
|---|---|---|---|
| A12 12×1 (MPI only) | 185.6 | 191.9 | 111.5 |
| A12 12×1 + `mpi_yield_when_idle` | 180.5 | 183.9 | 107.3 |
| A12 1×12 (OpenMP only, default wait) | 121.2 | 115.0 | 70.4 |
| A12 1×12, `OMP_WAIT_POLICY=active` | 121.6 | 114.9 | 70.7 |
| A12 1×12, `OMP_WAIT_POLICY=passive` | 104.9 (3.2× slower) | 111.8 (3.5× slower) | 70.2 (3.5× slower) |
| M8 8×1 / + yield / 1×8 / 1×8 active | 191 / 182 / 121 / 121 | 200 / 193 / 120 / 120 | 125 / 118 / 72 / 73 |
| control P4 4×1 / 1×4 / 1×4 active | 128 / 127 / 127 | 121 / 122 / 122 | 71 / 71 / 69 |

- **The simple spin hypothesis is not supported.** Forcing OpenMP threads to spin (`active`) changes nothing: their energy stays about 40% below MPI-only. MPI yield trims only 3–5%. The MPI-only premium (1.5–1.7×) exists only when P and E cores are mixed; on P-cores alone, MPI-only and OpenMP-only cost the same.
- **Confirmed with hardware counters** (`perf_check.sh`, `results/perf_summary.md`; thermal2, 2000 iterations, median of 2). The difference is *how* waiting cores spend their cycles:

| config | E_pkg J | P-core instructions (1e9) | P-core IPC | P-core cycles in PAUSE | E-core instructions (1e9) |
|---|---|---|---|---|---|
| A12 MPI-only 12×1 | 372.5 | 228.3 | 1.74 | 0.2% | 120.2 |
| A12 OpenMP-only 1×12 | 245.9 | 59.9 | 0.56 | 38.3% | 115.3 |
| M8 MPI-only 8×1 | 388.3 | 300.1 | 1.93 | 0.1% | 88.4 |
| M8 OpenMP-only 1×8 | 244.4 | 89.1 | 0.68 | 38.1% | 86.4 |
| P4 MPI-only / OpenMP-only (control) | 257.2 / 257.9 | 176.5 / 173.0 | 1.36 / 1.33 | 0.1% / 1.0% | – |

  - With OpenMP, waiting P-cores spend about 38% of their cycles in the low-power PAUSE instruction.
  - With MPI, the P-cores never PAUSE. Instead they execute 3.4–3.8× more instructions at high IPC: 168–211 billion extra instructions that do no useful work, i.e. the shared-memory polling loop.
  - The P-cores also clock about 20% more cycles in the same solve time, which suggests they hold a higher frequency while polling.
  - The E-cores run the same instruction count either way, so the useful work is identical and all the extra energy (1.5–1.6×) comes from P-cores busy-polling.
  - On P-cores alone (no slow ranks to wait for) the counters match, and so does the energy.
- **Passive waiting** (threads sleep) cuts power to 6–8 W but makes the solve 1.3–3.6× slower on mixed cores. Waking threads several times per iteration is too expensive. Net energy ranges from 13% lower to 11% higher, so it is a poor trade-off.

**Convergence check** (`results/converge*`; solve to 1e-8; 1 rep):

| matrix | iterations (range) | lowest energy | vs P4 1×4 | fastest |
|---|---|---|---|---|
| thermal2 | 4330–4332 | E8 1×8, 407 J | 0.73× | A16 1×16, 17.5 s |
| G3_circuit | 6606–6651 | E4s 1×4, 574 J (E8 575 J) | 0.70× | U16/A16, 30.4–30.5 s |
| ecology2 | 6233 (all) | E4s 1×4, 320 J | 0.73× | A16/P4/U16, 16.5–16.6 s |
| apache2 | 4914–4927 | E8 1×8, 218 J | 0.74× | U16/P4/A16, 9.86–9.89 s |
| cant | 9463–9522 | E8 1×8, 190 J | 0.70× | A16 1×16, 7.0 s |

- Full solves reproduce the fixed-1000-iteration energy ratios almost exactly (E-core ratios 0.70–0.74× vs 0.69–0.74× in the sweep). Fixed-iteration measurement is therefore a valid stand-in for time-to-solution and energy-to-solution.
- Iteration counts differ by at most 0.6% between configs, because the order of sums in the dot products changes. That's normal floating-point behaviour and too small to change any ranking.
- One outlier: unpinned U16 on thermal2 took 21.3 s vs 17.5 s for pinned A16, in a single run. In the sweep they matched, so treat this as run-to-run variance of unpinned placement.

## 7. Open issues and risks

- **RAPL permission (blocker):** run the `chmod` in the README after each reboot, before sweeping.
- **No per-core-type energy:** RAPL only gives package/core totals, so RQ2 compares whole-package energy while the other cores sit idle. We'll report both total energy and energy minus measured idle power.
- **RAPL accuracy:** all conclusions are relative comparisons using the same instrument, never absolute energy claims. This limitation must be stated in the report (Lastovetsky & Manumachu 2023; Raffin & Trystram 2025).
- **Power settings:** decide before the full sweep whether to keep the defaults (realistic laptop behaviour; recommended) or pin EPP to `performance`. Don't change them mid-sweep. Stay on AC power.
- **Citations:** 7 corrections are needed in the proposal (e.g. "Kuhn" → Wlotzka & Heuveline, "Onodera" → Nakajima, Wu & Taylor energy paper → Lively et al.). Some claims are still unchecked against the full papers.
- **Possible addition (not built):** split work by measured core speed instead of equally, e.g. give P-core ranks about 2.5× the nonzeros. This directly fixes finding 3. It would give the report a concrete "proposed method" to compare against the existing equal split, and fills the "Comparison with Existing Methods" section.

## 8. Next steps (exact commands)

```bash
cd ~/PCAP_Mini_Project
# 1. allow RAPL reads (until reboot)
sudo chmod o+r /sys/class/powercap/intel-rapl:*/energy_uj /sys/class/powercap/intel-rapl:*:*/energy_uj
# 2. energy pilot (~20 min) -> check energy CV and idle baseline
REPS=3 ITERS=1000 OUT=results/pilot_energy.csv ./sweep.sh configs/pilot.txt
python3 analyze.py results/pilot_energy.csv
# 3. full sweep (~2.5 h, AC power, nothing else running)
REPS=3 ITERS=1000 OUT=results/full.csv ./sweep.sh configs/full.txt
python3 analyze.py results/full.csv
```

## 9. Final report coverage (17 required sections)

| Section | State |
|---|---|
| Title, Abstract, Keywords | title fixed; abstract after results |
| Introduction, Literature Review | in proposal; apply citation fixes |
| Problem Statement, Objectives | in proposal (RQ1–RQ3) |
| Proposed Methodology, System Architecture, Algorithms | built; §4 above is the source text |
| Experimental Setup | §5 + configs; finalise after sweep |
| Results, Performance Analysis | runtime pilot in; energy pending |
| Comparison with Existing Methods | needs either the literature-numbers comparison or the speed-weighted split (§7) |
| Conclusion, Future Scope, References | after results |
