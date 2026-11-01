# Sweep report: `mixed.csv`

## Data quality

- runs: 165 total, 0 throttled (excluded), 0 on battery/unknown power (excluded), 165 kept
- G3_circuit.rcm.csr: tol 1e-08; 33/33 runs converged with true relative residual <= tol (max 9.98e-09); iterations 6605-6651 (spread 0.7%)
- apache2.rcm.csr: tol 1e-08; 33/33 runs converged with true relative residual <= tol (max 9.97e-09); iterations 4914-4927 (spread 0.3%)
- cant.rcm.csr: tol 1e-08; 33/33 runs converged with true relative residual <= tol (max 9.99e-09); iterations 9464-9531 (spread 0.7%)
- ecology2.rcm.csr: tol 1e-08; 33/33 runs converged with true relative residual <= tol (max 9.95e-09); iterations 6233-6233 (spread 0.0%)
- thermal2.rcm.csr: tol 1e-08; 33/33 runs converged with true relative residual <= tol (max 1.00e-08); iterations 4330-4332 (spread 0.0%)
- idle baseline: pkg 0.34 W, core 0.03 W, uncore 0.00 W, psys 0.81 W

## Per-matrix results (median over reps)

### G3_circuit

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| A16 1x16 | Mixed P+E | 30.607 | 0.2 | nan | 720.5 | nan | 23.5 | 0.1 | 0.0 |
| P4 1x4 | P-cores | 30.924 | 0.2 | nan | 819.2 | nan | 26.5 | 0.0 | 0.0 |
| U4 1x4 | Unpinned | 31.152 | 0.5 | nan | 820.1 | nan | 26.3 | 0.0 | 0.0 |
| U16 1x16 | Unpinned | 31.537 | 2.4 | nan | 733.6 | nan | 23.3 | 0.7 | 0.1 |
| P8ht 1x8 | P-cores | 32.839 | 0.1 | nan | 726.9 | nan | 22.1 | 0.0 | 0.0 |
| A12 1x12 | Mixed P+E | 33.466 | 0.2 | nan | 769.3 | nan | 23.0 | 0.1 | 0.0 |
| A12 12x1 | Mixed P+E | 33.764 | 0.1 | nan | 1301.8 | nan | 38.6 | 6.8 | 40.2 |
| U8 1x8 | Unpinned | 34.182 | 0.2 | nan | 771.2 | nan | 22.6 | 0.0 | 0.0 |
| M8 8x1 | Mixed P+E | 40.144 | 0.0 | nan | 1362.2 | nan | 33.9 | 4.9 | 40.2 |
| M8 1x8 | Mixed P+E | 40.821 | 0.1 | nan | 801.8 | nan | 19.6 | 0.0 | 0.0 |
| E8 1x8 | E-cores | 44.616 | 0.1 | nan | 578.8 | nan | 13.0 | 0.1 | 0.1 |

- **RQ1** fastest: `A16 1x16` (30.607 s)
  - lowest energy: `E8 1x8` (578.8 J) -> DIVERGE: fastest costs 1.24x the energy, frugal is 1.46x slower
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.36x the time, 0.80x the package energy
- **RQ3** 4 threads: best unpinned `U4 1x4` 31.152 s vs best pinned `P4 1x4` 30.924 s (1.01x); energy 820.1 vs 819.2 J (1.00x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 34.182 s vs best pinned `P8ht 1x8` 32.839 s (1.04x); energy 771.2 vs 578.8 J (1.33x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 31.537 s vs best pinned `A16 1x16` 30.607 s (1.03x); energy 733.6 vs 720.5 J (1.02x)

### apache2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 9.869 | 0.4 | nan | 296.7 | nan | 30.1 | 0.1 | 0.0 |
| A16 1x16 | Mixed P+E | 9.989 | 0.4 | nan | 272.6 | nan | 27.3 | 0.1 | 0.0 |
| U4 1x4 | Unpinned | 10.008 | 0.8 | nan | 299.5 | nan | 29.9 | 0.1 | 0.0 |
| U16 1x16 | Unpinned | 10.009 | 7.2 | nan | 273.7 | nan | 27.3 | 0.1 | 0.0 |
| P8ht 1x8 | P-cores | 10.067 | 0.3 | nan | 276.4 | nan | 27.5 | 0.1 | 0.0 |
| A12 12x1 | Mixed P+E | 11.379 | 0.2 | nan | 493.8 | nan | 43.4 | 7.2 | 47.6 |
| A12 1x12 | Mixed P+E | 11.468 | 0.2 | nan | 304.2 | nan | 26.5 | 0.1 | 0.0 |
| U8 1x8 | Unpinned | 11.749 | 0.2 | nan | 303.0 | nan | 25.8 | 0.1 | 0.0 |
| M8 8x1 | Mixed P+E | 14.081 | 0.2 | nan | 544.6 | nan | 38.7 | 6.8 | 49.8 |
| M8 1x8 | Mixed P+E | 14.233 | 0.0 | nan | 312.3 | nan | 21.9 | 0.1 | 0.0 |
| E8 1x8 | E-cores | 16.564 | 0.2 | nan | 215.8 | nan | 13.0 | 0.1 | 0.2 |

- **RQ1** fastest: `P4 1x4` (9.869 s)
  - lowest energy: `E8 1x8` (215.8 J) -> DIVERGE: fastest costs 1.37x the energy, frugal is 1.68x slower
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.65x the time, 0.78x the package energy
- **RQ3** 4 threads: best unpinned `U4 1x4` 10.008 s vs best pinned `P4 1x4` 9.869 s (1.01x); energy 299.5 vs 296.7 J (1.01x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 11.749 s vs best pinned `P8ht 1x8` 10.067 s (1.17x); energy 303.0 vs 215.8 J (1.40x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 10.009 s vs best pinned `A16 1x16` 9.989 s (1.00x); energy 273.7 vs 272.6 J (1.00x)

### cant

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| U16 1x16 | Unpinned | 7.080 | 0.3 | nan | 266.9 | nan | 37.7 | 0.3 | 0.1 |
| A16 1x16 | Mixed P+E | 7.129 | 0.2 | nan | 267.5 | nan | 37.5 | 0.3 | 0.1 |
| P8ht 1x8 | P-cores | 8.134 | 0.1 | nan | 262.5 | nan | 32.3 | 0.1 | 0.1 |
| P4 1x4 | P-cores | 8.813 | 0.9 | nan | 270.6 | nan | 30.7 | 0.1 | 0.1 |
| U4 1x4 | Unpinned | 9.062 | 0.4 | nan | 271.9 | nan | 30.0 | 0.1 | 0.1 |
| A12 1x12 | Mixed P+E | 9.068 | 0.1 | nan | 276.6 | nan | 30.5 | 0.2 | 0.1 |
| A12 12x1 | Mixed P+E | 9.216 | 0.6 | nan | 415.0 | nan | 45.0 | 1.8 | 49.8 |
| U8 1x8 | Unpinned | 9.548 | 0.2 | nan | 287.8 | nan | 30.1 | 0.2 | 0.1 |
| M8 1x8 | Mixed P+E | 11.237 | 0.3 | nan | 294.4 | nan | 26.2 | 0.1 | 0.0 |
| M8 8x1 | Mixed P+E | 11.263 | 0.1 | nan | 442.6 | nan | 39.3 | 1.5 | 46.8 |
| E8 1x8 | E-cores | 13.807 | 0.1 | nan | 193.7 | nan | 14.0 | 0.2 | 0.2 |

- **RQ1** fastest: `U16 1x16` (7.080 s)
  - lowest energy: `E8 1x8` (193.7 J) -> DIVERGE: fastest costs 1.38x the energy, frugal is 1.95x slower
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.70x the time, 0.74x the package energy
- **RQ3** 4 threads: best unpinned `U4 1x4` 9.062 s vs best pinned `P4 1x4` 8.813 s (1.03x); energy 271.9 vs 270.6 J (1.01x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 9.548 s vs best pinned `P8ht 1x8` 8.134 s (1.17x); energy 287.8 vs 193.7 J (1.49x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 7.080 s vs best pinned `A16 1x16` 7.129 s (0.99x); energy 266.9 vs 267.5 J (1.00x)

### ecology2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 16.426 | 0.8 | nan | 442.8 | nan | 27.0 | 0.0 | 0.0 |
| U4 1x4 | Unpinned | 16.550 | 0.3 | nan | 444.9 | nan | 26.9 | 0.0 | 0.0 |
| A16 1x16 | Mixed P+E | 16.653 | 0.1 | nan | 395.4 | nan | 23.7 | 0.1 | 0.0 |
| P8ht 1x8 | P-cores | 17.004 | 0.2 | nan | 401.2 | nan | 23.6 | 0.1 | 0.0 |
| A12 12x1 | Mixed P+E | 18.051 | 0.2 | nan | 713.6 | nan | 39.5 | 5.5 | 44.6 |
| A12 1x12 | Mixed P+E | 18.391 | 0.1 | nan | 446.6 | nan | 24.3 | 0.1 | 0.0 |
| U16 1x16 | Unpinned | 18.419 | 6.8 | nan | 421.2 | nan | 22.9 | 2.2 | 0.0 |
| U8 1x8 | Unpinned | 18.837 | 0.3 | nan | 440.1 | nan | 23.4 | 0.1 | 0.0 |
| M8 8x1 | Mixed P+E | 22.886 | 0.1 | nan | 807.5 | nan | 35.3 | 5.8 | 47.2 |
| M8 1x8 | Mixed P+E | 23.415 | 0.4 | nan | 461.0 | nan | 19.7 | 0.1 | 0.0 |
| E8 1x8 | E-cores | 26.093 | 0.3 | nan | 332.8 | nan | 12.8 | 0.1 | 0.1 |

- **RQ1** fastest: `P4 1x4` (16.426 s)
  - lowest energy: `E8 1x8` (332.8 J) -> DIVERGE: fastest costs 1.33x the energy, frugal is 1.59x slower
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.53x the time, 0.83x the package energy
- **RQ3** 4 threads: best unpinned `U4 1x4` 16.550 s vs best pinned `P4 1x4` 16.426 s (1.01x); energy 444.9 vs 442.8 J (1.00x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 18.837 s vs best pinned `P8ht 1x8` 17.004 s (1.11x); energy 440.1 vs 332.8 J (1.32x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 18.419 s vs best pinned `A16 1x16` 16.653 s (1.11x); energy 421.2 vs 395.4 J (1.07x)

### thermal2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| U16 1x16 | Unpinned | 17.562 | 0.2 | nan | 513.0 | nan | 29.2 | 0.1 | 0.0 |
| A16 1x16 | Mixed P+E | 17.624 | 0.4 | nan | 514.2 | nan | 29.2 | 0.1 | 0.0 |
| P8ht 1x8 | P-cores | 18.613 | 0.1 | nan | 496.8 | nan | 26.7 | 0.0 | 0.0 |
| A12 12x1 | Mixed P+E | 19.161 | 0.1 | nan | 820.2 | nan | 42.8 | 3.8 | 40.7 |
| A12 1x12 | Mixed P+E | 19.177 | 0.0 | nan | 530.6 | nan | 27.7 | 0.1 | 0.0 |
| P4 1x4 | P-cores | 19.186 | 0.1 | nan | 555.6 | nan | 29.0 | 0.0 | 0.0 |
| U4 1x4 | Unpinned | 19.251 | 0.5 | nan | 555.6 | nan | 28.9 | 0.0 | 0.0 |
| U8 1x8 | Unpinned | 20.495 | 0.2 | nan | 517.2 | nan | 25.2 | 0.1 | 0.0 |
| M8 8x1 | Mixed P+E | 22.858 | 0.1 | nan | 849.9 | nan | 37.2 | 3.1 | 39.7 |
| M8 1x8 | Mixed P+E | 23.334 | 0.0 | nan | 527.3 | nan | 22.6 | 0.0 | 0.0 |
| E8 1x8 | E-cores | 24.906 | 0.1 | nan | 407.2 | nan | 16.4 | 0.1 | 0.1 |

- **RQ1** fastest: `U16 1x16` (17.562 s)
  - lowest energy: `E8 1x8` (407.2 J) -> DIVERGE: fastest costs 1.26x the energy, frugal is 1.42x slower
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.34x the time, 0.82x the package energy
- **RQ3** 4 threads: best unpinned `U4 1x4` 19.251 s vs best pinned `P4 1x4` 19.186 s (1.00x); energy 555.6 vs 555.6 J (1.00x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 20.495 s vs best pinned `P8ht 1x8` 18.613 s (1.10x); energy 517.2 vs 407.2 J (1.27x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 17.562 s vs best pinned `A16 1x16` 17.624 s (1.00x); energy 513.0 vs 514.2 J (1.00x)

