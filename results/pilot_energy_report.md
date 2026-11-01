# Sweep report: `pilot_energy.csv`

## Data quality

- runs: 150 total, 0 throttled (excluded), 0 on battery/unknown power (excluded), 150 kept
- G3_circuit.rcm.csr: fixed 1000-1000 iterations per run (work-normalised mode)
- apache2.rcm.csr: fixed 1000-1000 iterations per run (work-normalised mode)
- cant.rcm.csr: fixed 1000-1000 iterations per run (work-normalised mode)
- ecology2.rcm.csr: fixed 1000-1000 iterations per run (work-normalised mode)
- thermal2.rcm.csr: fixed 1000-1000 iterations per run (work-normalised mode)
- idle baseline: pkg 0.34 W, core 0.03 W, uncore 0.00 W, psys 0.81 W

## Per-matrix results (median over reps)

### G3_circuit

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 4.631 | 0.9 | 2.08 | 120.9 | 0.83 | 26.1 | 0.0 | 0.0 |
| U4 4x1 | Unpinned | 4.673 | 0.6 | 2.06 | 120.8 | 0.83 | 25.9 | 0.8 | 1.1 |
| P4 4x1 | P-cores | 4.674 | 0.6 | 2.06 | 121.1 | 0.83 | 25.9 | 0.7 | 1.1 |
| A12 12x1 | Mixed P+E | 5.075 | 0.5 | 1.90 | 191.9 | 1.31 | 37.8 | 6.8 | 40.5 |
| U12 12x1 | Unpinned | 5.077 | 0.4 | 1.90 | 193.3 | 1.32 | 38.1 | 5.3 | 36.1 |
| M8 8x1 | Mixed P+E | 6.035 | 0.5 | 1.60 | 198.3 | 1.36 | 32.9 | 4.8 | 40.5 |
| P1 1x1 | P-cores | 9.638 | 1.3 | 1.00 | 146.1 | 1.00 | 15.2 | 0.0 | 0.0 |
| E4 1x4 | E-cores | 12.194 | 0.2 | 0.79 | 128.3 | 0.88 | 10.5 | 0.0 | 0.1 |
| E4 4x1 | E-cores | 12.312 | 0.5 | 0.78 | 129.8 | 0.89 | 10.5 | 0.7 | 1.0 |
| E1 1x1 | E-cores | 17.574 | 0.4 | 0.55 | 161.5 | 1.11 | 9.2 | 0.0 | 0.0 |

- **RQ1** fastest: `P4 1x4` (4.631 s)
  - lowest energy: `U4 4x1` (120.8 J) -> TIE within 3% (noise level)
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.82x the time, 1.11x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.63x the time, 1.06x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.63x the time, 1.07x the package energy
- **RQ3** 4 threads: best unpinned `U4 4x1` 4.673 s vs best pinned `P4 1x4` 4.631 s (1.01x); energy 120.8 vs 120.9 J (1.00x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 5.077 s vs best pinned `A12 12x1` 5.075 s (1.00x); energy 193.3 vs 191.9 J (1.01x)

### apache2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 1.994 | 0.8 | 2.45 | 59.1 | 0.78 | 29.6 | 0.1 | 0.0 |
| P4 4x1 | P-cores | 2.027 | 3.9 | 2.41 | 61.5 | 0.82 | 30.4 | 1.0 | 1.7 |
| U4 4x1 | Unpinned | 2.041 | 0.8 | 2.40 | 62.1 | 0.82 | 30.4 | 1.0 | 3.7 |
| A12 12x1 | Mixed P+E | 2.295 | 0.6 | 2.13 | 98.1 | 1.30 | 42.8 | 7.1 | 47.7 |
| U12 12x1 | Unpinned | 2.344 | 0.3 | 2.09 | 100.0 | 1.33 | 42.7 | 6.6 | 40.4 |
| M8 8x1 | Mixed P+E | 2.865 | 1.4 | 1.71 | 108.7 | 1.44 | 37.9 | 6.8 | 49.8 |
| P1 1x1 | P-cores | 4.892 | 1.0 | 1.00 | 75.4 | 1.00 | 15.4 | 0.0 | 0.0 |
| E4 1x4 | E-cores | 6.277 | 4.6 | 0.78 | 64.6 | 0.86 | 10.3 | 0.0 | 0.1 |
| E4 4x1 | E-cores | 6.345 | 0.3 | 0.77 | 66.1 | 0.88 | 10.4 | 1.0 | 1.9 |
| E1 1x1 | E-cores | 9.211 | 0.3 | 0.53 | 83.6 | 1.11 | 9.1 | 0.0 | 0.1 |

- **RQ1** fastest: `P4 1x4` (1.994 s)
  - lowest energy: `P4 1x4` (59.1 J) -> SAME config
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.88x the time, 1.11x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 3.15x the time, 1.09x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 3.13x the time, 1.07x the package energy
- **RQ3** 4 threads: best unpinned `U4 4x1` 2.041 s vs best pinned `P4 1x4` 1.994 s (1.02x); energy 62.1 vs 59.1 J (1.05x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 2.344 s vs best pinned `A12 12x1` 2.295 s (1.02x); energy 100.0 vs 98.1 J (1.02x)

### cant

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 4x1 | P-cores | 0.949 | 12.3 | 2.63 | 29.1 | 0.79 | 30.6 | 0.4 | 5.7 |
| A12 12x1 | Mixed P+E | 0.951 | 0.6 | 2.62 | 42.6 | 1.15 | 44.7 | 1.8 | 49.5 |
| U12 12x1 | Unpinned | 0.957 | 0.3 | 2.61 | 43.3 | 1.17 | 45.3 | 1.7 | 48.0 |
| P4 1x4 | P-cores | 0.962 | 2.8 | 2.59 | 28.4 | 0.77 | 29.6 | 0.1 | 0.1 |
| U4 4x1 | Unpinned | 1.001 | 3.4 | 2.49 | 30.3 | 0.82 | 30.3 | 0.4 | 11.7 |
| M8 8x1 | Mixed P+E | 1.197 | 0.3 | 2.08 | 44.8 | 1.22 | 37.5 | 1.5 | 47.7 |
| P1 1x1 | P-cores | 2.494 | 0.6 | 1.00 | 36.9 | 1.00 | 14.8 | 0.0 | 0.0 |
| E4 4x1 | E-cores | 2.529 | 1.6 | 0.99 | 28.2 | 0.77 | 11.2 | 0.4 | 1.1 |
| E4 1x4 | E-cores | 2.550 | 1.6 | 0.98 | 27.7 | 0.75 | 10.9 | 0.1 | 0.1 |
| E1 1x1 | E-cores | 5.232 | 0.6 | 0.48 | 45.6 | 1.24 | 8.7 | 0.0 | 0.1 |

- **RQ1** fastest: `P4 4x1` (0.949 s)
  - lowest energy: `E4 1x4` (27.7 J) -> DIVERGE: fastest costs 1.05x the energy, frugal is 2.69x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 2.10x the time, 1.24x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.67x the time, 0.97x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.65x the time, 0.97x the package energy
- **RQ3** 4 threads: best unpinned `U4 4x1` 1.001 s vs best pinned `P4 4x1` 0.949 s (1.05x); energy 30.3 vs 27.7 J (1.09x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 0.957 s vs best pinned `A12 12x1` 0.951 s (1.01x); energy 43.3 vs 42.6 J (1.02x)

### ecology2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 4x1 | P-cores | 2.639 | 0.7 | 2.18 | 70.5 | 0.81 | 26.7 | 0.6 | 1.5 |
| U4 4x1 | Unpinned | 2.650 | 1.2 | 2.18 | 70.8 | 0.81 | 26.7 | 0.6 | 1.5 |
| P4 1x4 | P-cores | 2.691 | 2.0 | 2.14 | 69.6 | 0.80 | 25.8 | 0.0 | 0.0 |
| A12 12x1 | Mixed P+E | 2.877 | 0.4 | 2.00 | 110.7 | 1.27 | 38.5 | 5.1 | 43.8 |
| U12 12x1 | Unpinned | 2.881 | 1.0 | 2.00 | 113.3 | 1.30 | 39.3 | 4.9 | 46.9 |
| M8 8x1 | Mixed P+E | 3.644 | 0.2 | 1.58 | 124.4 | 1.43 | 34.2 | 5.7 | 47.0 |
| P1 1x1 | P-cores | 5.765 | 0.3 | 1.00 | 87.1 | 1.00 | 15.1 | 0.0 | 0.0 |
| E4 1x4 | E-cores | 7.621 | 1.1 | 0.76 | 80.1 | 0.92 | 10.5 | 0.0 | 0.1 |
| E4 4x1 | E-cores | 7.675 | 1.0 | 0.75 | 79.9 | 0.92 | 10.4 | 0.5 | 0.9 |
| E1 1x1 | E-cores | 10.946 | 0.9 | 0.53 | 100.3 | 1.15 | 9.2 | 0.0 | 0.1 |

- **RQ1** fastest: `P4 4x1` (2.639 s)
  - lowest energy: `P4 1x4` (69.6 J) -> TIE within 3% (noise level)
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.90x the time, 1.15x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.91x the time, 1.13x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.83x the time, 1.15x the package energy
- **RQ3** 4 threads: best unpinned `U4 4x1` 2.650 s vs best pinned `P4 4x1` 2.639 s (1.00x); energy 70.8 vs 69.6 J (1.02x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 2.881 s vs best pinned `A12 12x1` 2.877 s (1.00x); energy 113.3 vs 110.7 J (1.02x)

### thermal2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| U12 12x1 | Unpinned | 4.392 | 0.2 | 2.75 | 186.9 | 1.05 | 42.6 | 3.2 | 41.3 |
| P4 1x4 | P-cores | 4.394 | 0.2 | 2.75 | 126.0 | 0.71 | 28.7 | 0.0 | 0.0 |
| A12 12x1 | Mixed P+E | 4.394 | 0.1 | 2.75 | 185.7 | 1.04 | 42.3 | 3.6 | 40.6 |
| P4 4x1 | P-cores | 4.399 | 1.1 | 2.75 | 126.3 | 0.71 | 28.7 | 0.4 | 1.3 |
| U4 4x1 | Unpinned | 4.412 | 0.3 | 2.74 | 126.9 | 0.71 | 28.8 | 0.4 | 1.6 |
| M8 8x1 | Mixed P+E | 5.237 | 0.1 | 2.31 | 190.6 | 1.07 | 36.4 | 3.3 | 39.8 |
| E4 1x4 | E-cores | 9.214 | 0.4 | 1.31 | 118.1 | 0.66 | 12.8 | 0.0 | 0.1 |
| E4 4x1 | E-cores | 9.452 | 1.1 | 1.28 | 118.5 | 0.67 | 12.5 | 0.4 | 0.6 |
| P1 1x1 | P-cores | 12.090 | 0.5 | 1.00 | 178.2 | 1.00 | 14.7 | 0.0 | 0.0 |
| E1 1x1 | E-cores | 21.477 | 0.3 | 0.56 | 191.3 | 1.07 | 8.9 | 0.0 | 0.0 |

- **RQ1** fastest: `U12 12x1` (4.392 s)
  - lowest energy: `E4 1x4` (118.1 J) -> DIVERGE: fastest costs 1.58x the energy, frugal is 2.10x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.78x the time, 1.07x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.10x the time, 0.94x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.15x the time, 0.94x the package energy
- **RQ3** 4 threads: best unpinned `U4 4x1` 4.412 s vs best pinned `P4 1x4` 4.394 s (1.00x); energy 126.9 vs 118.1 J (1.07x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 4.392 s vs best pinned `A12 12x1` 4.394 s (1.00x); energy 186.9 vs 185.7 J (1.01x)

