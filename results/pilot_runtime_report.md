# Sweep report: `pilot_runtime.csv`

## Data quality

- runs: 150 total, 0 throttled (excluded), 0 on battery/unknown power (excluded), 150 kept
- iteration count IDENTICAL across configs for ecology2.rcm.csr
- iteration count IDENTICAL across configs for cant.rcm.csr
- iteration count IDENTICAL across configs for thermal2.rcm.csr
- iteration count IDENTICAL across configs for G3_circuit.rcm.csr
- iteration count IDENTICAL across configs for apache2.rcm.csr
- RAPL energy not available in this CSV (all -1): runtime-only analysis

## Per-matrix results (median over reps)

### G3_circuit

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 1.443 | 0.7 | 2.14 | nan | nan | nan | 0.0 | 0.0 |
| P4 4x1 | P-cores | 1.455 | 0.6 | 2.12 | nan | nan | nan | 0.8 | 1.7 |
| U4 4x1 | Unpinned | 1.542 | 4.8 | 2.00 | nan | nan | nan | 0.8 | 5.3 |
| A12 12x1 | Mixed P+E | 1.556 | 0.2 | 1.98 | nan | nan | nan | 5.9 | 39.7 |
| U12 12x1 | Unpinned | 1.556 | 0.6 | 1.98 | nan | nan | nan | 5.3 | 38.9 |
| M8 8x1 | Mixed P+E | 1.855 | 0.1 | 1.66 | nan | nan | nan | 4.2 | 39.8 |
| P1 1x1 | P-cores | 3.085 | 0.4 | 1.00 | nan | nan | nan | 0.0 | 0.0 |
| E4 1x4 | E-cores | 3.530 | 0.4 | 0.87 | nan | nan | nan | 0.0 | 0.1 |
| E4 4x1 | E-cores | 3.534 | 0.5 | 0.87 | nan | nan | nan | 0.9 | 2.5 |
| E1 1x1 | E-cores | 5.417 | 0.2 | 0.57 | nan | nan | nan | 0.0 | 0.0 |

- **RQ1** fastest: `P4 1x4` (1.443 s)
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.76x the time
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.45x the time
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.43x the time
- **RQ3** 4 threads: best unpinned `U4 4x1` 1.542 s vs best pinned `P4 1x4` 1.443 s (1.07x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 1.556 s vs best pinned `A12 12x1` 1.556 s (1.00x)

### apache2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 0.613 | 7.2 | 2.50 | nan | nan | nan | 0.1 | 0.0 |
| P4 4x1 | P-cores | 0.624 | 3.0 | 2.46 | nan | nan | nan | 1.0 | 2.0 |
| U4 4x1 | Unpinned | 0.654 | 7.7 | 2.35 | nan | nan | nan | 1.1 | 6.0 |
| A12 12x1 | Mixed P+E | 0.714 | 1.5 | 2.15 | nan | nan | nan | 6.8 | 46.5 |
| U12 12x1 | Unpinned | 0.727 | 2.6 | 2.11 | nan | nan | nan | 6.0 | 39.9 |
| M8 8x1 | Mixed P+E | 0.895 | 1.7 | 1.71 | nan | nan | nan | 6.3 | 49.7 |
| P1 1x1 | P-cores | 1.534 | 1.3 | 1.00 | nan | nan | nan | 0.0 | 0.0 |
| E4 1x4 | E-cores | 1.794 | 0.8 | 0.86 | nan | nan | nan | 0.0 | 0.1 |
| E4 4x1 | E-cores | 1.799 | 0.9 | 0.85 | nan | nan | nan | 1.2 | 3.2 |
| E1 1x1 | E-cores | 2.863 | 1.8 | 0.54 | nan | nan | nan | 0.0 | 0.1 |

- **RQ1** fastest: `P4 1x4` (0.613 s)
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.87x the time
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.93x the time
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.88x the time
- **RQ3** 4 threads: best unpinned `U4 4x1` 0.654 s vs best pinned `P4 1x4` 0.613 s (1.07x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 0.727 s vs best pinned `A12 12x1` 0.714 s (1.02x)

### cant

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 0.281 | 8.8 | 2.76 | nan | nan | nan | 0.1 | 0.1 |
| P4 4x1 | P-cores | 0.298 | 3.7 | 2.60 | nan | nan | nan | 0.4 | 5.1 |
| A12 12x1 | Mixed P+E | 0.300 | 12.6 | 2.58 | nan | nan | nan | 1.9 | 48.7 |
| U12 12x1 | Unpinned | 0.304 | 7.2 | 2.55 | nan | nan | nan | 1.8 | 46.9 |
| U4 4x1 | Unpinned | 0.309 | 14.8 | 2.50 | nan | nan | nan | 0.4 | 9.7 |
| M8 8x1 | Mixed P+E | 0.391 | 0.5 | 1.98 | nan | nan | nan | 1.5 | 49.0 |
| E4 1x4 | E-cores | 0.729 | 1.7 | 1.06 | nan | nan | nan | 0.1 | 0.1 |
| E4 4x1 | E-cores | 0.744 | 1.8 | 1.04 | nan | nan | nan | 0.5 | 3.1 |
| P1 1x1 | P-cores | 0.775 | 0.6 | 1.00 | nan | nan | nan | 0.0 | 0.0 |
| E1 1x1 | E-cores | 1.626 | 0.4 | 0.48 | nan | nan | nan | 0.0 | 0.1 |

- **RQ1** fastest: `P4 1x4` (0.281 s)
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 2.10x the time
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.59x the time
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.50x the time
- **RQ3** 4 threads: best unpinned `U4 4x1` 0.309 s vs best pinned `P4 1x4` 0.281 s (1.10x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 0.304 s vs best pinned `A12 12x1` 0.300 s (1.01x)

### ecology2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 4x1 | P-cores | 0.828 | 4.7 | 2.22 | nan | nan | nan | 0.8 | 2.9 |
| U4 4x1 | Unpinned | 0.844 | 1.7 | 2.18 | nan | nan | nan | 0.7 | 3.6 |
| P4 1x4 | P-cores | 0.850 | 3.5 | 2.17 | nan | nan | nan | 0.1 | 0.0 |
| U12 12x1 | Unpinned | 0.896 | 2.6 | 2.06 | nan | nan | nan | 4.7 | 42.1 |
| A12 12x1 | Mixed P+E | 0.904 | 0.1 | 2.04 | nan | nan | nan | 5.0 | 43.8 |
| M8 8x1 | Mixed P+E | 1.130 | 0.4 | 1.63 | nan | nan | nan | 5.5 | 47.3 |
| P1 1x1 | P-cores | 1.841 | 1.5 | 1.00 | nan | nan | nan | 0.0 | 0.0 |
| E4 1x4 | E-cores | 2.215 | 0.1 | 0.83 | nan | nan | nan | 0.0 | 0.1 |
| E4 4x1 | E-cores | 2.217 | 0.8 | 0.83 | nan | nan | nan | 0.8 | 2.7 |
| E1 1x1 | E-cores | 3.344 | 0.7 | 0.55 | nan | nan | nan | 0.0 | 0.1 |

- **RQ1** fastest: `P4 4x1` (0.828 s)
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.82x the time
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.68x the time
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.61x the time
- **RQ3** 4 threads: best unpinned `U4 4x1` 0.844 s vs best pinned `P4 4x1` 0.828 s (1.02x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 0.896 s vs best pinned `A12 12x1` 0.904 s (0.99x)

### thermal2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| A12 12x1 | Mixed P+E | 1.361 | 1.5 | 2.78 | nan | nan | nan | 3.3 | 40.5 |
| U12 12x1 | Unpinned | 1.365 | 2.4 | 2.77 | nan | nan | nan | 3.0 | 38.7 |
| U4 4x1 | Unpinned | 1.366 | 0.6 | 2.77 | nan | nan | nan | 0.5 | 2.4 |
| P4 4x1 | P-cores | 1.370 | 0.6 | 2.76 | nan | nan | nan | 0.4 | 2.0 |
| P4 1x4 | P-cores | 1.370 | 1.3 | 2.76 | nan | nan | nan | 0.0 | 0.0 |
| M8 8x1 | Mixed P+E | 1.633 | 1.8 | 2.31 | nan | nan | nan | 2.7 | 38.5 |
| E4 4x1 | E-cores | 2.823 | 1.1 | 1.34 | nan | nan | nan | 0.5 | 2.3 |
| E4 1x4 | E-cores | 2.839 | 0.2 | 1.33 | nan | nan | nan | 0.0 | 0.1 |
| P1 1x1 | P-cores | 3.779 | 0.5 | 1.00 | nan | nan | nan | 0.0 | 0.0 |
| E1 1x1 | E-cores | 6.550 | 0.9 | 0.58 | nan | nan | nan | 0.0 | 0.0 |

- **RQ1** fastest: `A12 12x1` (1.361 s)
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.73x the time
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.06x the time
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.07x the time
- **RQ3** 4 threads: best unpinned `U4 4x1` 1.366 s vs best pinned `P4 4x1` 1.370 s (1.00x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 1.365 s vs best pinned `A12 12x1` 1.361 s (1.00x)

