# Sweep report: `full.csv`

## Data quality

- runs: 765 total, 0 throttled (excluded), 0 on battery/unknown power (excluded), 765 kept
- iteration count IDENTICAL across configs for thermal2.rcm.csr
- iteration count IDENTICAL across configs for cant.rcm.csr
- iteration count IDENTICAL across configs for apache2.rcm.csr
- iteration count IDENTICAL across configs for G3_circuit.rcm.csr
- iteration count IDENTICAL across configs for ecology2.rcm.csr
- idle baseline: pkg 0.34 W, core 0.03 W, uncore 0.00 W, psys 0.81 W

## Per-matrix results (median over reps)

### G3_circuit

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| U16 1x16 | Unpinned | 4.570 | 0.3 | 2.06 | 107.5 | 0.74 | 23.5 | 0.1 | 0.0 |
| A16 1x16 | Mixed P+E | 4.583 | 0.1 | 2.05 | 107.3 | 0.74 | 23.4 | 0.1 | 0.0 |
| A16 2x8 | Mixed P+E | 4.613 | 0.1 | 2.04 | 108.2 | 0.74 | 23.5 | 2.0 | 2.5 |
| A16 4x4 | Mixed P+E | 4.622 | 0.2 | 2.03 | 108.8 | 0.75 | 23.5 | 2.4 | 4.3 |
| A16 8x2 | Mixed P+E | 4.632 | 0.2 | 2.03 | 112.8 | 0.78 | 24.4 | 3.0 | 4.7 |
| P4 1x4 | P-cores | 4.654 | 0.7 | 2.02 | 120.7 | 0.83 | 25.9 | 0.0 | 0.0 |
| U16 16x1 | Unpinned | 4.693 | 0.2 | 2.00 | 115.5 | 0.79 | 24.6 | 3.9 | 5.0 |
| U4 1x4 | Unpinned | 4.701 | 1.4 | 2.00 | 120.9 | 0.83 | 25.7 | 0.0 | 0.0 |
| P4 2x2 | P-cores | 4.710 | 1.1 | 2.00 | 122.2 | 0.84 | 26.0 | 0.6 | 1.3 |
| U4 2x2 | Unpinned | 4.723 | 0.5 | 1.99 | 121.6 | 0.84 | 25.8 | 0.5 | 2.0 |
| A16 16x1 | Mixed P+E | 4.761 | 0.9 | 1.98 | 116.3 | 0.80 | 24.4 | 3.9 | 6.1 |
| P4 4x1 | P-cores | 4.779 | 1.6 | 1.97 | 124.0 | 0.85 | 25.9 | 0.8 | 3.7 |
| U4 4x1 | Unpinned | 4.824 | 2.3 | 1.95 | 124.2 | 0.85 | 25.8 | 0.7 | 3.0 |
| P8ht 1x8 | P-cores | 4.935 | 0.6 | 1.91 | 108.6 | 0.75 | 22.0 | 0.0 | 0.0 |
| P8ht 4x2 | P-cores | 4.994 | 0.3 | 1.88 | 109.7 | 0.75 | 22.0 | 0.8 | 0.6 |
| P8ht 2x4 | P-cores | 4.994 | 0.8 | 1.88 | 108.5 | 0.75 | 21.7 | 0.5 | 0.3 |
| U12 1x12 | Unpinned | 4.996 | 0.4 | 1.88 | 115.2 | 0.79 | 23.1 | 0.1 | 0.1 |
| A12 1x12 | Mixed P+E | 5.003 | 0.0 | 1.88 | 115.1 | 0.79 | 23.0 | 0.1 | 0.0 |
| A12 4x3 | Mixed P+E | 5.005 | 0.2 | 1.88 | 156.0 | 1.07 | 31.2 | 4.0 | 35.0 |
| A12 6x2 | Mixed P+E | 5.029 | 0.2 | 1.87 | 170.4 | 1.17 | 33.9 | 5.4 | 40.4 |
| A12 3x4 | Mixed P+E | 5.029 | 0.1 | 1.87 | 156.2 | 1.07 | 31.0 | 4.1 | 35.2 |
| U12 12x1 | Unpinned | 5.049 | 0.2 | 1.86 | 194.1 | 1.34 | 38.4 | 5.9 | 41.0 |
| P8ht 8x1 | P-cores | 5.053 | 0.2 | 1.86 | 112.5 | 0.77 | 22.3 | 1.2 | 2.4 |
| A12 2x6 | Mixed P+E | 5.060 | 0.4 | 1.86 | 115.4 | 0.79 | 22.8 | 0.8 | 1.0 |
| A12 12x1 | Mixed P+E | 5.074 | 1.0 | 1.85 | 192.8 | 1.33 | 38.0 | 6.5 | 40.5 |
| A16 1x16 dyn | Mixed P+E | 5.088 | 0.4 | 1.85 | 125.5 | 0.86 | 24.7 | 0.1 | 0.0 |
| U8 4x2 | Unpinned | 5.133 | 0.3 | 1.83 | 138.8 | 0.96 | 27.0 | 2.3 | 24.1 |
| U8 8x1 | Unpinned | 5.147 | 0.2 | 1.83 | 160.8 | 1.11 | 31.2 | 3.1 | 23.8 |
| U8 1x8 | Unpinned | 5.151 | 0.1 | 1.83 | 115.1 | 0.79 | 22.3 | 0.1 | 0.1 |
| U8 2x4 | Unpinned | 5.158 | 0.2 | 1.82 | 114.0 | 0.78 | 22.1 | 0.5 | 0.6 |
| U16 4x4 | Unpinned | 5.241 | 2.8 | 1.79 | 132.2 | 0.91 | 25.2 | 5.5 | 14.9 |
| A12 1x12 dyn | Mixed P+E | 5.411 | 0.4 | 1.74 | 130.8 | 0.90 | 24.2 | 0.1 | 0.0 |
| M8 4x2 | Mixed P+E | 5.974 | 0.3 | 1.57 | 175.6 | 1.21 | 29.4 | 4.3 | 40.7 |
| M8 8x1 | Mixed P+E | 6.024 | 0.1 | 1.56 | 199.9 | 1.38 | 33.2 | 4.8 | 40.6 |
| M8 2x4 | Mixed P+E | 6.051 | 0.4 | 1.55 | 160.5 | 1.10 | 26.5 | 3.6 | 35.8 |
| M8 1x8 | Mixed P+E | 6.138 | 0.3 | 1.53 | 118.8 | 0.82 | 19.3 | 0.0 | 0.0 |
| M8 1x8 dyn | Mixed P+E | 6.289 | 0.4 | 1.50 | 141.9 | 0.98 | 22.6 | 0.0 | 0.0 |
| E8 1x8 | E-cores | 6.708 | 0.1 | 1.40 | 85.5 | 0.59 | 12.7 | 0.1 | 0.1 |
| E8 4x2 | E-cores | 6.785 | 0.2 | 1.39 | 86.9 | 0.60 | 12.8 | 1.1 | 1.9 |
| E8 2x4 | E-cores | 6.811 | 0.2 | 1.38 | 86.6 | 0.60 | 12.7 | 0.9 | 1.5 |
| E8 8x1 | E-cores | 6.925 | 0.7 | 1.36 | 87.1 | 0.60 | 12.6 | 1.4 | 2.1 |
| P4 1x4 dyn | P-cores | 7.046 | 0.4 | 1.33 | 166.8 | 1.15 | 23.7 | 0.0 | 0.0 |
| E8 1x8 dyn | E-cores | 7.546 | 0.1 | 1.25 | 105.7 | 0.73 | 14.0 | 0.1 | 0.1 |
| E4s 1x4 | E-cores | 7.943 | 0.2 | 1.18 | 84.9 | 0.58 | 10.7 | 0.1 | 0.1 |
| E4s 2x2 | E-cores | 7.949 | 0.3 | 1.18 | 85.2 | 0.59 | 10.7 | 0.7 | 1.1 |
| E4s 4x1 | E-cores | 8.013 | 0.1 | 1.17 | 85.8 | 0.59 | 10.7 | 1.0 | 2.0 |
| P1 1x1 | P-cores | 9.403 | 1.0 | 1.00 | 145.4 | 1.00 | 15.5 | 0.0 | 0.0 |
| E4 2x2 | E-cores | 12.236 | 0.1 | 0.77 | 128.4 | 0.88 | 10.5 | 0.4 | 0.6 |
| E4 1x4 | E-cores | 12.240 | 0.5 | 0.77 | 127.5 | 0.88 | 10.4 | 0.0 | 0.1 |
| E4 4x1 | E-cores | 12.281 | 0.2 | 0.77 | 128.4 | 0.88 | 10.5 | 0.7 | 1.0 |
| E1 1x1 | E-cores | 17.593 | 0.3 | 0.53 | 160.1 | 1.10 | 9.1 | 0.0 | 0.0 |

- **RQ1** fastest: `U16 1x16` (4.570 s)
  - lowest energy: `E4s 1x4` (84.9 J) -> DIVERGE: fastest costs 1.27x the energy, frugal is 1.74x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.87x the time, 1.10x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.63x the time, 1.06x the package energy
- **RQ2** P4 2x2 vs E4 2x2: E-cores take 2.60x the time, 1.05x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.57x the time, 1.04x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.36x the time, 0.79x the package energy
- **RQ2** P8ht 4x2 vs E8 4x2: E-cores take 1.36x the time, 0.79x the package energy
- **RQ2** P8ht 2x4 vs E8 2x4: E-cores take 1.36x the time, 0.80x the package energy
- **RQ2** P8ht 8x1 vs E8 8x1: E-cores take 1.37x the time, 0.77x the package energy
- **RQ3** 4 threads: best unpinned `U4 1x4` 4.701 s vs best pinned `P4 1x4` 4.654 s (1.01x); energy 120.9 vs 84.9 J (1.42x)
- **RQ3** 8 threads: best unpinned `U8 4x2` 5.133 s vs best pinned `P8ht 1x8` 4.935 s (1.04x); energy 114.0 vs 85.5 J (1.33x)
- **RQ3** 12 threads: best unpinned `U12 1x12` 4.996 s vs best pinned `A12 1x12` 5.003 s (1.00x); energy 115.2 vs 115.1 J (1.00x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 4.570 s vs best pinned `A16 1x16` 4.583 s (1.00x); energy 107.5 vs 107.3 J (1.00x)

### apache2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| U16 1x16 | Unpinned | 2.001 | 0.4 | 2.44 | 54.6 | 0.73 | 27.3 | 0.1 | 0.1 |
| A16 1x16 | Mixed P+E | 2.004 | 0.1 | 2.44 | 54.5 | 0.73 | 27.2 | 0.1 | 0.1 |
| P8ht 1x8 | P-cores | 2.022 | 0.3 | 2.41 | 56.0 | 0.75 | 27.7 | 0.1 | 0.0 |
| U4 4x1 | Unpinned | 2.031 | 4.7 | 2.40 | 60.8 | 0.81 | 30.0 | 1.0 | 2.0 |
| P8ht 2x4 | P-cores | 2.035 | 0.4 | 2.40 | 57.1 | 0.76 | 28.1 | 0.8 | 0.5 |
| A16 2x8 | Mixed P+E | 2.040 | 0.1 | 2.39 | 55.4 | 0.74 | 27.1 | 2.9 | 2.0 |
| A16 4x4 | Mixed P+E | 2.041 | 0.2 | 2.39 | 57.0 | 0.76 | 27.9 | 3.1 | 5.0 |
| A16 8x2 | Mixed P+E | 2.050 | 0.2 | 2.38 | 58.2 | 0.78 | 28.4 | 3.3 | 4.5 |
| P8ht 4x2 | P-cores | 2.059 | 0.1 | 2.37 | 56.5 | 0.75 | 27.4 | 1.1 | 0.7 |
| P8ht 8x1 | P-cores | 2.093 | 0.2 | 2.33 | 57.1 | 0.76 | 27.3 | 1.5 | 2.0 |
| U16 16x1 | Unpinned | 2.121 | 0.3 | 2.30 | 58.1 | 0.77 | 27.4 | 3.9 | 5.3 |
| A16 16x1 | Mixed P+E | 2.135 | 1.4 | 2.29 | 57.3 | 0.76 | 26.8 | 3.8 | 5.5 |
| U4 1x4 | Unpinned | 2.216 | 6.9 | 2.20 | 60.1 | 0.80 | 27.1 | 0.1 | 0.0 |
| P4 2x2 | P-cores | 2.233 | 5.8 | 2.19 | 64.0 | 0.85 | 28.7 | 0.7 | 12.0 |
| P4 4x1 | P-cores | 2.240 | 3.7 | 2.18 | 67.1 | 0.89 | 29.9 | 1.0 | 12.9 |
| P4 1x4 | P-cores | 2.242 | 4.3 | 2.18 | 61.1 | 0.81 | 27.2 | 0.1 | 0.0 |
| A12 6x2 | Mixed P+E | 2.261 | 0.1 | 2.16 | 85.0 | 1.13 | 37.6 | 6.2 | 49.5 |
| U4 2x2 | Unpinned | 2.268 | 3.9 | 2.15 | 62.4 | 0.83 | 27.5 | 0.7 | 6.4 |
| A16 1x16 dyn | Mixed P+E | 2.293 | 0.6 | 2.13 | 60.6 | 0.81 | 26.4 | 0.1 | 0.0 |
| A12 12x1 | Mixed P+E | 2.294 | 0.7 | 2.13 | 98.2 | 1.31 | 42.8 | 7.1 | 47.4 |
| A12 1x12 | Mixed P+E | 2.307 | 0.3 | 2.12 | 59.9 | 0.80 | 26.0 | 0.1 | 0.0 |
| A12 4x3 | Mixed P+E | 2.310 | 0.2 | 2.11 | 81.0 | 1.08 | 35.1 | 5.1 | 39.8 |
| A12 3x4 | Mixed P+E | 2.312 | 0.1 | 2.11 | 80.1 | 1.07 | 34.6 | 5.4 | 38.5 |
| U12 1x12 | Unpinned | 2.320 | 0.1 | 2.10 | 60.6 | 0.81 | 26.1 | 0.1 | 0.1 |
| U12 12x1 | Unpinned | 2.339 | 0.7 | 2.09 | 99.4 | 1.33 | 42.5 | 6.3 | 40.5 |
| A12 2x6 | Mixed P+E | 2.351 | 0.2 | 2.08 | 61.6 | 0.82 | 26.2 | 1.1 | 0.9 |
| U8 1x8 | Unpinned | 2.363 | 0.3 | 2.07 | 59.2 | 0.79 | 25.1 | 0.1 | 0.1 |
| U8 2x4 | Unpinned | 2.384 | 0.6 | 2.05 | 60.9 | 0.81 | 25.5 | 0.8 | 0.6 |
| U8 4x2 | Unpinned | 2.391 | 1.0 | 2.04 | 74.4 | 0.99 | 31.1 | 2.7 | 31.8 |
| U8 8x1 | Unpinned | 2.392 | 0.6 | 2.04 | 91.1 | 1.21 | 38.1 | 4.0 | 36.8 |
| A12 1x12 dyn | Mixed P+E | 2.522 | 0.2 | 1.94 | 68.0 | 0.91 | 27.0 | 0.1 | 0.0 |
| M8 4x2 | Mixed P+E | 2.800 | 0.2 | 1.74 | 91.1 | 1.21 | 32.5 | 6.4 | 51.0 |
| M8 8x1 | Mixed P+E | 2.855 | 0.2 | 1.71 | 107.6 | 1.43 | 37.7 | 6.8 | 50.0 |
| M8 1x8 | Mixed P+E | 2.863 | 0.7 | 1.71 | 62.2 | 0.83 | 21.7 | 0.1 | 0.0 |
| M8 2x4 | Mixed P+E | 2.869 | 0.3 | 1.70 | 84.8 | 1.13 | 29.6 | 5.7 | 41.8 |
| M8 1x8 dyn | Mixed P+E | 2.991 | 1.0 | 1.63 | 71.6 | 0.95 | 23.9 | 0.1 | 0.0 |
| P4 1x4 dyn | P-cores | 3.195 | 0.7 | 1.53 | 83.0 | 1.11 | 26.0 | 0.0 | 0.0 |
| E8 1x8 | E-cores | 3.337 | 0.4 | 1.46 | 44.3 | 0.59 | 13.3 | 0.1 | 0.2 |
| E8 4x2 | E-cores | 3.398 | 0.6 | 1.44 | 43.7 | 0.58 | 12.9 | 1.8 | 1.9 |
| E8 2x4 | E-cores | 3.408 | 0.1 | 1.43 | 43.4 | 0.58 | 12.7 | 1.2 | 1.0 |
| E8 8x1 | E-cores | 3.422 | 2.6 | 1.43 | 44.7 | 0.60 | 13.1 | 2.0 | 2.3 |
| E8 1x8 dyn | E-cores | 3.630 | 0.4 | 1.35 | 50.5 | 0.67 | 13.9 | 0.1 | 0.1 |
| E4s 1x4 | E-cores | 3.826 | 0.2 | 1.28 | 48.6 | 0.65 | 12.7 | 0.1 | 0.1 |
| E4s 2x2 | E-cores | 3.878 | 1.4 | 1.26 | 48.6 | 0.65 | 12.5 | 1.0 | 1.0 |
| E4s 4x1 | E-cores | 3.881 | 1.6 | 1.26 | 49.1 | 0.66 | 12.7 | 1.4 | 2.0 |
| P1 1x1 | P-cores | 4.883 | 0.5 | 1.00 | 75.0 | 1.00 | 15.4 | 0.0 | 0.0 |
| U16 4x4 | Unpinned | 5.140 | 53.6 | 0.95 | 147.7 | 1.97 | 28.7 | 25.1 | 43.3 |
| E4 1x4 | E-cores | 6.169 | 0.6 | 0.79 | 64.6 | 0.86 | 10.5 | 0.0 | 0.1 |
| E4 4x1 | E-cores | 6.268 | 0.5 | 0.78 | 65.6 | 0.87 | 10.5 | 1.0 | 1.7 |
| E4 2x2 | E-cores | 6.335 | 1.3 | 0.77 | 64.3 | 0.86 | 10.2 | 0.5 | 0.5 |
| E1 1x1 | E-cores | 9.222 | 0.4 | 0.53 | 84.1 | 1.12 | 9.1 | 0.0 | 0.1 |

- **RQ1** fastest: `U16 1x16` (2.001 s)
  - lowest energy: `E8 2x4` (43.4 J) -> DIVERGE: fastest costs 1.26x the energy, frugal is 1.70x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.89x the time, 1.12x the package energy
- **RQ2** P4 2x2 vs E4 2x2: E-cores take 2.84x the time, 1.00x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.80x the time, 0.98x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.75x the time, 1.06x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.65x the time, 0.79x the package energy
- **RQ2** P8ht 2x4 vs E8 2x4: E-cores take 1.67x the time, 0.76x the package energy
- **RQ2** P8ht 4x2 vs E8 4x2: E-cores take 1.65x the time, 0.77x the package energy
- **RQ2** P8ht 8x1 vs E8 8x1: E-cores take 1.64x the time, 0.78x the package energy
- **RQ3** 4 threads: best unpinned `U4 4x1` 2.031 s vs best pinned `P4 2x2` 2.233 s (0.91x); energy 60.1 vs 48.6 J (1.24x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 2.363 s vs best pinned `P8ht 1x8` 2.022 s (1.17x); energy 59.2 vs 43.4 J (1.37x)
- **RQ3** 12 threads: best unpinned `U12 1x12` 2.320 s vs best pinned `A12 6x2` 2.261 s (1.03x); energy 60.6 vs 59.9 J (1.01x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 2.001 s vs best pinned `A16 1x16` 2.004 s (1.00x); energy 54.6 vs 54.5 J (1.00x)

### cant

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| A16 1x16 | Mixed P+E | 0.741 | 0.3 | 3.36 | 27.7 | 0.75 | 37.4 | 0.3 | 0.1 |
| U16 1x16 | Unpinned | 0.742 | 0.5 | 3.35 | 27.7 | 0.75 | 37.3 | 0.3 | 0.1 |
| A16 2x8 | Mixed P+E | 0.748 | 0.5 | 3.32 | 28.0 | 0.76 | 37.4 | 1.4 | 2.3 |
| A16 4x4 | Mixed P+E | 0.748 | 0.0 | 3.32 | 28.2 | 0.76 | 37.6 | 1.4 | 3.3 |
| A16 8x2 | Mixed P+E | 0.752 | 0.5 | 3.31 | 28.7 | 0.78 | 38.2 | 1.5 | 4.9 |
| U16 16x1 | Unpinned | 0.768 | 0.3 | 3.24 | 27.8 | 0.76 | 36.3 | 1.7 | 5.3 |
| A16 16x1 | Mixed P+E | 0.791 | 2.4 | 3.14 | 27.6 | 0.75 | 34.9 | 1.6 | 6.0 |
| A16 1x16 dyn | Mixed P+E | 0.792 | 0.1 | 3.14 | 29.4 | 0.80 | 37.1 | 0.3 | 0.1 |
| A12 1x12 dyn | Mixed P+E | 0.841 | 0.4 | 2.96 | 31.5 | 0.85 | 37.4 | 0.3 | 0.1 |
| P8ht 1x8 | P-cores | 0.848 | 0.0 | 2.93 | 27.1 | 0.74 | 32.0 | 0.1 | 0.1 |
| P8ht 4x2 | P-cores | 0.849 | 0.2 | 2.93 | 27.4 | 0.74 | 32.3 | 0.5 | 1.2 |
| P8ht 2x4 | P-cores | 0.851 | 0.2 | 2.92 | 27.3 | 0.74 | 32.0 | 0.4 | 0.7 |
| P8ht 8x1 | P-cores | 0.861 | 0.3 | 2.89 | 28.0 | 0.76 | 32.5 | 0.5 | 2.0 |
| M8 1x8 dyn | Mixed P+E | 0.907 | 2.4 | 2.74 | 31.5 | 0.86 | 34.8 | 0.2 | 0.1 |
| A12 4x3 | Mixed P+E | 0.946 | 0.2 | 2.63 | 34.0 | 0.92 | 36.0 | 1.1 | 41.4 |
| A12 1x12 | Mixed P+E | 0.947 | 0.3 | 2.63 | 28.3 | 0.77 | 29.9 | 0.2 | 0.1 |
| U12 1x12 | Unpinned | 0.948 | 0.5 | 2.62 | 28.3 | 0.77 | 29.8 | 0.3 | 0.2 |
| A12 3x4 | Mixed P+E | 0.952 | 0.2 | 2.61 | 32.8 | 0.89 | 34.5 | 1.3 | 32.7 |
| U4 2x2 | Unpinned | 0.953 | 6.4 | 2.61 | 28.6 | 0.77 | 30.0 | 0.4 | 3.8 |
| A12 6x2 | Mixed P+E | 0.955 | 0.4 | 2.60 | 37.5 | 1.02 | 39.2 | 1.6 | 47.0 |
| A12 2x6 | Mixed P+E | 0.956 | 0.2 | 2.60 | 28.3 | 0.77 | 29.6 | 0.7 | 1.2 |
| A12 12x1 | Mixed P+E | 0.958 | 0.3 | 2.60 | 42.8 | 1.16 | 44.7 | 1.8 | 49.6 |
| U12 12x1 | Unpinned | 0.961 | 0.6 | 2.59 | 42.8 | 1.16 | 44.5 | 1.6 | 48.2 |
| P4 1x4 dyn | P-cores | 0.983 | 1.4 | 2.53 | 29.5 | 0.80 | 30.0 | 0.1 | 0.1 |
| U8 1x8 | Unpinned | 1.003 | 0.8 | 2.48 | 29.2 | 0.79 | 29.1 | 0.2 | 0.1 |
| U8 8x1 | Unpinned | 1.015 | 0.9 | 2.45 | 39.8 | 1.08 | 39.2 | 1.2 | 37.1 |
| U8 2x4 | Unpinned | 1.017 | 2.0 | 2.45 | 29.6 | 0.80 | 29.1 | 0.4 | 1.1 |
| U4 4x1 | Unpinned | 1.022 | 6.7 | 2.43 | 30.7 | 0.83 | 30.0 | 0.4 | 13.2 |
| U8 4x2 | Unpinned | 1.034 | 2.4 | 2.40 | 31.1 | 0.84 | 30.1 | 0.7 | 4.1 |
| P4 1x4 | P-cores | 1.039 | 8.0 | 2.39 | 28.8 | 0.78 | 27.7 | 0.1 | 0.1 |
| P4 4x1 | P-cores | 1.082 | 2.4 | 2.30 | 33.5 | 0.91 | 30.9 | 0.4 | 20.7 |
| P4 2x2 | P-cores | 1.109 | 4.4 | 2.24 | 29.6 | 0.80 | 26.7 | 0.3 | 1.0 |
| U4 1x4 | Unpinned | 1.111 | 4.6 | 2.24 | 29.6 | 0.80 | 26.6 | 0.1 | 0.1 |
| M8 4x2 | Mixed P+E | 1.164 | 0.0 | 2.14 | 38.8 | 1.05 | 33.3 | 1.3 | 45.4 |
| M8 2x4 | Mixed P+E | 1.164 | 0.3 | 2.14 | 35.5 | 0.96 | 30.5 | 1.3 | 32.6 |
| M8 1x8 | Mixed P+E | 1.165 | 0.2 | 2.13 | 29.2 | 0.79 | 25.0 | 0.1 | 0.0 |
| M8 8x1 | Mixed P+E | 1.196 | 0.3 | 2.08 | 44.4 | 1.20 | 37.1 | 1.6 | 47.4 |
| E8 1x8 | E-cores | 1.439 | 0.3 | 1.73 | 19.9 | 0.54 | 13.8 | 0.2 | 0.2 |
| E8 8x1 | E-cores | 1.453 | 0.3 | 1.71 | 20.1 | 0.54 | 13.8 | 0.8 | 2.1 |
| E8 4x2 | E-cores | 1.458 | 0.3 | 1.71 | 19.9 | 0.54 | 13.7 | 0.8 | 2.3 |
| E8 2x4 | E-cores | 1.458 | 0.2 | 1.71 | 19.9 | 0.54 | 13.7 | 0.7 | 1.5 |
| E8 1x8 dyn | E-cores | 1.477 | 0.2 | 1.68 | 21.1 | 0.57 | 14.3 | 0.2 | 0.2 |
| E4s 1x4 | E-cores | 1.660 | 0.2 | 1.50 | 24.7 | 0.67 | 14.9 | 0.1 | 0.2 |
| E4s 4x1 | E-cores | 1.672 | 0.4 | 1.49 | 25.0 | 0.68 | 15.0 | 0.6 | 1.5 |
| E4s 2x2 | E-cores | 1.677 | 0.3 | 1.48 | 24.6 | 0.67 | 14.7 | 0.5 | 1.3 |
| U16 4x4 | Unpinned | 2.063 | 26.6 | 1.21 | 64.0 | 1.74 | 31.0 | 17.0 | 44.7 |
| P1 1x1 | P-cores | 2.487 | 3.6 | 1.00 | 36.8 | 1.00 | 14.8 | 0.0 | 0.0 |
| E4 1x4 | E-cores | 2.549 | 2.0 | 0.98 | 28.0 | 0.76 | 11.0 | 0.1 | 0.1 |
| E4 4x1 | E-cores | 2.564 | 0.3 | 0.97 | 28.1 | 0.76 | 11.0 | 0.4 | 1.1 |
| E4 2x2 | E-cores | 2.576 | 0.4 | 0.97 | 28.2 | 0.77 | 11.0 | 0.3 | 1.2 |
| E1 1x1 | E-cores | 5.202 | 0.4 | 0.48 | 45.0 | 1.22 | 8.7 | 0.0 | 0.1 |

- **RQ1** fastest: `A16 1x16` (0.741 s)
  - lowest energy: `E8 1x8` (19.9 J) -> DIVERGE: fastest costs 1.40x the energy, frugal is 1.94x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 2.09x the time, 1.22x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.45x the time, 0.97x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.37x the time, 0.84x the package energy
- **RQ2** P4 2x2 vs E4 2x2: E-cores take 2.32x the time, 0.95x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.70x the time, 0.73x the package energy
- **RQ2** P8ht 4x2 vs E8 4x2: E-cores take 1.72x the time, 0.73x the package energy
- **RQ2** P8ht 2x4 vs E8 2x4: E-cores take 1.71x the time, 0.73x the package energy
- **RQ2** P8ht 8x1 vs E8 8x1: E-cores take 1.69x the time, 0.72x the package energy
- **RQ3** 4 threads: best unpinned `U4 2x2` 0.953 s vs best pinned `P4 1x4 dyn` 0.983 s (0.97x); energy 28.6 vs 24.6 J (1.16x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 1.003 s vs best pinned `P8ht 1x8` 0.848 s (1.18x); energy 29.2 vs 19.9 J (1.47x)
- **RQ3** 12 threads: best unpinned `U12 1x12` 0.948 s vs best pinned `A12 1x12 dyn` 0.841 s (1.13x); energy 28.3 vs 28.3 J (1.00x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 0.742 s vs best pinned `A16 1x16` 0.741 s (1.00x); energy 27.7 vs 27.6 J (1.00x)

### ecology2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| A16 1x16 | Mixed P+E | 2.627 | 0.1 | 2.20 | 62.1 | 0.72 | 23.6 | 0.1 | 0.0 |
| U16 1x16 | Unpinned | 2.631 | 0.5 | 2.19 | 62.2 | 0.72 | 23.7 | 0.1 | 0.0 |
| P4 4x1 | P-cores | 2.640 | 0.4 | 2.18 | 70.6 | 0.81 | 26.8 | 0.7 | 1.1 |
| A16 4x4 | Mixed P+E | 2.644 | 0.3 | 2.18 | 63.1 | 0.73 | 23.8 | 1.2 | 2.2 |
| P4 1x4 | P-cores | 2.645 | 5.1 | 2.18 | 69.8 | 0.80 | 26.4 | 0.1 | 0.0 |
| A16 2x8 | Mixed P+E | 2.649 | 0.3 | 2.18 | 62.9 | 0.73 | 23.7 | 1.3 | 2.3 |
| A16 8x2 | Mixed P+E | 2.657 | 0.3 | 2.17 | 64.4 | 0.74 | 24.2 | 1.4 | 3.9 |
| U4 1x4 | Unpinned | 2.676 | 1.4 | 2.16 | 69.5 | 0.80 | 26.0 | 0.0 | 0.0 |
| A16 16x1 | Mixed P+E | 2.682 | 1.6 | 2.15 | 64.5 | 0.74 | 24.1 | 1.5 | 5.3 |
| U16 16x1 | Unpinned | 2.685 | 9.8 | 2.15 | 65.1 | 0.75 | 24.3 | 1.5 | 5.2 |
| P8ht 1x8 | P-cores | 2.695 | 0.1 | 2.14 | 62.3 | 0.72 | 23.1 | 0.1 | 0.0 |
| P8ht 2x4 | P-cores | 2.718 | 0.4 | 2.12 | 63.1 | 0.73 | 23.2 | 0.7 | 0.5 |
| P8ht 4x2 | P-cores | 2.736 | 0.4 | 2.11 | 63.7 | 0.73 | 23.3 | 0.7 | 0.8 |
| P8ht 8x1 | P-cores | 2.738 | 0.3 | 2.11 | 64.3 | 0.74 | 23.5 | 0.9 | 2.0 |
| U4 2x2 | Unpinned | 2.788 | 2.5 | 2.07 | 70.7 | 0.82 | 25.4 | 0.5 | 1.2 |
| U4 4x1 | Unpinned | 2.825 | 4.6 | 2.04 | 75.0 | 0.87 | 26.6 | 0.6 | 8.0 |
| P4 2x2 | P-cores | 2.833 | 3.3 | 2.04 | 72.8 | 0.84 | 25.7 | 0.5 | 8.2 |
| A12 6x2 | Mixed P+E | 2.863 | 0.2 | 2.01 | 98.4 | 1.13 | 34.4 | 4.8 | 45.3 |
| A12 12x1 | Mixed P+E | 2.873 | 0.3 | 2.01 | 111.3 | 1.28 | 38.7 | 5.1 | 44.3 |
| A12 4x3 | Mixed P+E | 2.900 | 0.2 | 1.99 | 93.0 | 1.07 | 32.1 | 4.4 | 38.7 |
| A12 3x4 | Mixed P+E | 2.910 | 0.3 | 1.98 | 92.6 | 1.07 | 31.8 | 4.4 | 37.0 |
| U12 12x1 | Unpinned | 2.930 | 0.2 | 1.97 | 112.4 | 1.30 | 38.4 | 4.9 | 38.4 |
| U12 1x12 | Unpinned | 2.931 | 0.1 | 1.97 | 70.0 | 0.81 | 23.9 | 0.1 | 0.1 |
| A12 1x12 | Mixed P+E | 2.937 | 0.2 | 1.96 | 70.7 | 0.81 | 24.1 | 0.1 | 0.0 |
| A12 2x6 | Mixed P+E | 2.953 | 0.1 | 1.95 | 71.0 | 0.82 | 24.0 | 0.8 | 1.0 |
| A16 1x16 dyn | Mixed P+E | 2.965 | 0.3 | 1.95 | 71.3 | 0.82 | 24.0 | 0.1 | 0.0 |
| U8 1x8 | Unpinned | 2.977 | 0.1 | 1.94 | 67.5 | 0.78 | 22.7 | 0.1 | 0.0 |
| U8 8x1 | Unpinned | 3.002 | 0.3 | 1.92 | 101.8 | 1.17 | 33.9 | 3.3 | 31.6 |
| U8 2x4 | Unpinned | 3.007 | 0.0 | 1.92 | 68.3 | 0.79 | 22.7 | 0.6 | 0.9 |
| U8 4x2 | Unpinned | 3.011 | 0.3 | 1.92 | 86.9 | 1.00 | 28.8 | 2.8 | 28.0 |
| A12 1x12 dyn | Mixed P+E | 3.210 | 0.2 | 1.80 | 79.3 | 0.91 | 24.7 | 0.1 | 0.0 |
| M8 4x2 | Mixed P+E | 3.622 | 0.5 | 1.59 | 106.9 | 1.23 | 29.5 | 5.5 | 47.5 |
| M8 8x1 | Mixed P+E | 3.659 | 0.3 | 1.58 | 124.9 | 1.44 | 34.1 | 5.4 | 47.3 |
| M8 2x4 | Mixed P+E | 3.677 | 0.2 | 1.57 | 96.8 | 1.12 | 26.3 | 5.0 | 39.6 |
| M8 1x8 | Mixed P+E | 3.701 | 0.3 | 1.56 | 71.6 | 0.83 | 19.3 | 0.1 | 0.0 |
| M8 1x8 dyn | Mixed P+E | 3.821 | 0.9 | 1.51 | 84.7 | 0.98 | 22.2 | 0.1 | 0.0 |
| E8 1x8 | E-cores | 4.151 | 0.3 | 1.39 | 51.9 | 0.60 | 12.5 | 0.1 | 0.1 |
| E8 2x4 | E-cores | 4.208 | 0.2 | 1.37 | 52.0 | 0.60 | 12.4 | 1.0 | 1.1 |
| E8 4x2 | E-cores | 4.213 | 0.1 | 1.37 | 52.8 | 0.61 | 12.5 | 1.1 | 1.7 |
| E8 8x1 | E-cores | 4.213 | 1.2 | 1.37 | 52.8 | 0.61 | 12.5 | 1.2 | 3.4 |
| P4 1x4 dyn | P-cores | 4.224 | 0.6 | 1.37 | 100.9 | 1.16 | 23.9 | 0.0 | 0.0 |
| U16 4x4 | Unpinned | 4.311 | 51.0 | 1.34 | 126.7 | 1.46 | 29.4 | 15.0 | 31.5 |
| E8 1x8 dyn | E-cores | 4.682 | 0.1 | 1.23 | 61.0 | 0.70 | 13.0 | 0.1 | 0.1 |
| E4s 1x4 | E-cores | 4.854 | 0.2 | 1.19 | 50.9 | 0.59 | 10.5 | 0.1 | 0.1 |
| E4s 4x1 | E-cores | 4.899 | 0.3 | 1.18 | 51.2 | 0.59 | 10.5 | 0.9 | 1.1 |
| E4s 2x2 | E-cores | 4.923 | 0.4 | 1.17 | 51.6 | 0.59 | 10.5 | 0.8 | 1.1 |
| P1 1x1 | P-cores | 5.767 | 0.2 | 1.00 | 86.7 | 1.00 | 15.0 | 0.0 | 0.0 |
| E4 1x4 | E-cores | 7.610 | 1.2 | 0.76 | 78.9 | 0.91 | 10.4 | 0.0 | 0.1 |
| E4 4x1 | E-cores | 7.659 | 0.9 | 0.75 | 78.9 | 0.91 | 10.3 | 0.5 | 1.0 |
| E4 2x2 | E-cores | 7.704 | 0.6 | 0.75 | 78.3 | 0.90 | 10.2 | 0.4 | 0.7 |
| E1 1x1 | E-cores | 10.868 | 0.5 | 0.53 | 98.2 | 1.13 | 9.0 | 0.0 | 0.1 |

- **RQ1** fastest: `A16 1x16` (2.627 s)
  - lowest energy: `E4s 1x4` (50.9 J) -> DIVERGE: fastest costs 1.22x the energy, frugal is 1.85x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.88x the time, 1.13x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.90x the time, 1.12x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.88x the time, 1.13x the package energy
- **RQ2** P4 2x2 vs E4 2x2: E-cores take 2.72x the time, 1.08x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.54x the time, 0.83x the package energy
- **RQ2** P8ht 2x4 vs E8 2x4: E-cores take 1.55x the time, 0.82x the package energy
- **RQ2** P8ht 4x2 vs E8 4x2: E-cores take 1.54x the time, 0.83x the package energy
- **RQ2** P8ht 8x1 vs E8 8x1: E-cores take 1.54x the time, 0.82x the package energy
- **RQ3** 4 threads: best unpinned `U4 1x4` 2.676 s vs best pinned `P4 4x1` 2.640 s (1.01x); energy 69.5 vs 50.9 J (1.37x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 2.977 s vs best pinned `P8ht 1x8` 2.695 s (1.10x); energy 67.5 vs 51.9 J (1.30x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 2.930 s vs best pinned `A12 6x2` 2.863 s (1.02x); energy 70.0 vs 70.7 J (0.99x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 2.631 s vs best pinned `A16 1x16` 2.627 s (1.00x); energy 62.2 vs 62.1 J (1.00x)

### thermal2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| U16 1x16 | Unpinned | 4.009 | 0.2 | 3.03 | 117.3 | 0.66 | 29.3 | 0.1 | 0.0 |
| A16 1x16 | Mixed P+E | 4.013 | 0.2 | 3.02 | 117.3 | 0.66 | 29.2 | 0.1 | 0.0 |
| A16 4x4 | Mixed P+E | 4.026 | 0.1 | 3.01 | 118.8 | 0.67 | 29.5 | 0.9 | 4.9 |
| A16 8x2 | Mixed P+E | 4.032 | 2.0 | 3.01 | 121.0 | 0.68 | 30.0 | 1.3 | 5.1 |
| A16 2x8 | Mixed P+E | 4.047 | 0.1 | 3.00 | 118.8 | 0.67 | 29.3 | 1.0 | 4.6 |
| U16 16x1 | Unpinned | 4.086 | 5.0 | 2.97 | 121.2 | 0.68 | 29.7 | 2.1 | 6.8 |
| A16 16x1 | Mixed P+E | 4.098 | 0.6 | 2.96 | 121.4 | 0.68 | 29.6 | 1.5 | 5.9 |
| P8ht 1x8 | P-cores | 4.280 | 0.3 | 2.83 | 113.7 | 0.64 | 26.6 | 0.0 | 0.0 |
| P8ht 2x4 | P-cores | 4.286 | 0.6 | 2.83 | 114.4 | 0.64 | 26.7 | 0.4 | 0.4 |
| P8ht 8x1 | P-cores | 4.290 | 0.5 | 2.83 | 115.6 | 0.65 | 27.0 | 0.6 | 1.7 |
| P8ht 4x2 | P-cores | 4.310 | 0.1 | 2.82 | 114.3 | 0.64 | 26.5 | 0.5 | 0.8 |
| A12 6x2 | Mixed P+E | 4.370 | 0.0 | 2.78 | 166.8 | 0.94 | 38.2 | 3.4 | 40.1 |
| A16 1x16 dyn | Mixed P+E | 4.371 | 0.3 | 2.78 | 128.9 | 0.72 | 29.5 | 0.1 | 0.0 |
| A12 4x3 | Mixed P+E | 4.374 | 0.3 | 2.77 | 156.8 | 0.88 | 35.8 | 2.5 | 37.2 |
| A12 3x4 | Mixed P+E | 4.383 | 0.2 | 2.77 | 155.5 | 0.87 | 35.5 | 2.7 | 36.5 |
| A12 12x1 | Mixed P+E | 4.389 | 0.3 | 2.76 | 185.7 | 1.04 | 42.3 | 3.5 | 40.4 |
| U4 4x1 | Unpinned | 4.401 | 3.3 | 2.76 | 127.8 | 0.72 | 29.0 | 0.4 | 1.9 |
| U12 12x1 | Unpinned | 4.402 | 0.2 | 2.76 | 187.9 | 1.06 | 42.7 | 3.2 | 38.2 |
| A12 1x12 | Mixed P+E | 4.406 | 0.2 | 2.75 | 121.5 | 0.68 | 27.6 | 0.1 | 0.0 |
| U12 1x12 | Unpinned | 4.409 | 0.0 | 2.75 | 121.5 | 0.68 | 27.5 | 0.1 | 0.1 |
| P4 2x2 | P-cores | 4.417 | 1.9 | 2.75 | 126.0 | 0.71 | 28.5 | 0.3 | 1.0 |
| U4 2x2 | Unpinned | 4.428 | 1.6 | 2.74 | 126.4 | 0.71 | 28.5 | 0.3 | 0.9 |
| A12 2x6 | Mixed P+E | 4.435 | 0.2 | 2.74 | 121.3 | 0.68 | 27.3 | 0.5 | 0.7 |
| P4 1x4 | P-cores | 4.445 | 0.5 | 2.73 | 126.2 | 0.71 | 28.4 | 0.0 | 0.0 |
| P4 4x1 | P-cores | 4.461 | 1.1 | 2.72 | 127.8 | 0.72 | 28.6 | 0.5 | 2.2 |
| A12 1x12 dyn | Mixed P+E | 4.626 | 0.1 | 2.62 | 131.1 | 0.74 | 28.3 | 0.1 | 0.0 |
| U4 1x4 | Unpinned | 4.636 | 2.6 | 2.62 | 126.1 | 0.71 | 27.2 | 0.0 | 0.0 |
| U8 1x8 | Unpinned | 4.686 | 0.1 | 2.59 | 117.0 | 0.66 | 25.0 | 0.0 | 0.0 |
| U8 8x1 | Unpinned | 4.701 | 0.1 | 2.58 | 170.8 | 0.96 | 36.3 | 1.8 | 31.3 |
| U8 4x2 | Unpinned | 4.726 | 0.2 | 2.57 | 118.5 | 0.67 | 25.1 | 0.6 | 0.9 |
| U8 2x4 | Unpinned | 4.727 | 0.3 | 2.57 | 117.8 | 0.66 | 24.9 | 0.4 | 0.8 |
| U16 4x4 | Unpinned | 5.076 | 34.7 | 2.39 | 154.5 | 0.87 | 30.4 | 8.9 | 18.1 |
| M8 4x2 | Mixed P+E | 5.235 | 0.2 | 2.32 | 167.3 | 0.94 | 32.0 | 3.0 | 38.7 |
| M8 8x1 | Mixed P+E | 5.236 | 0.0 | 2.32 | 191.1 | 1.07 | 36.5 | 3.1 | 39.8 |
| M8 2x4 | Mixed P+E | 5.259 | 0.2 | 2.31 | 157.5 | 0.89 | 30.0 | 2.8 | 35.6 |
| M8 1x8 | Mixed P+E | 5.329 | 0.2 | 2.28 | 119.1 | 0.67 | 22.4 | 0.0 | 0.0 |
| M8 1x8 dyn | Mixed P+E | 5.421 | 0.2 | 2.24 | 136.0 | 0.76 | 25.1 | 0.0 | 0.0 |
| E8 1x8 | E-cores | 5.705 | 0.1 | 2.13 | 92.3 | 0.52 | 16.2 | 0.1 | 0.1 |
| E8 4x2 | E-cores | 5.758 | 0.2 | 2.11 | 93.2 | 0.52 | 16.2 | 0.7 | 1.0 |
| E8 8x1 | E-cores | 5.771 | 1.0 | 2.10 | 95.0 | 0.53 | 16.5 | 0.7 | 1.1 |
| E8 2x4 | E-cores | 5.778 | 0.1 | 2.10 | 93.1 | 0.52 | 16.1 | 0.6 | 0.7 |
| P4 1x4 dyn | P-cores | 6.053 | 0.4 | 2.00 | 155.1 | 0.87 | 25.6 | 0.0 | 0.0 |
| E8 1x8 dyn | E-cores | 6.383 | 0.3 | 1.90 | 101.7 | 0.57 | 15.9 | 0.1 | 0.1 |
| E4s 1x4 | E-cores | 7.115 | 0.1 | 1.71 | 97.7 | 0.55 | 13.7 | 0.0 | 0.1 |
| E4s 2x2 | E-cores | 7.181 | 0.1 | 1.69 | 97.0 | 0.55 | 13.5 | 0.5 | 1.0 |
| E4s 4x1 | E-cores | 7.219 | 0.5 | 1.68 | 97.9 | 0.55 | 13.6 | 0.5 | 1.2 |
| E4 1x4 | E-cores | 9.273 | 0.1 | 1.31 | 118.2 | 0.66 | 12.7 | 0.0 | 0.1 |
| E4 2x2 | E-cores | 9.353 | 0.2 | 1.30 | 118.7 | 0.67 | 12.7 | 0.3 | 0.5 |
| E4 4x1 | E-cores | 9.446 | 0.2 | 1.28 | 118.5 | 0.67 | 12.5 | 0.4 | 0.7 |
| P1 1x1 | P-cores | 12.134 | 0.3 | 1.00 | 177.9 | 1.00 | 14.7 | 0.0 | 0.0 |
| E1 1x1 | E-cores | 21.446 | 0.1 | 0.57 | 190.3 | 1.07 | 8.9 | 0.0 | 0.0 |

- **RQ1** fastest: `U16 1x16` (4.009 s)
  - lowest energy: `E8 1x8` (92.3 J) -> DIVERGE: fastest costs 1.27x the energy, frugal is 1.42x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.77x the time, 1.07x the package energy
- **RQ2** P4 2x2 vs E4 2x2: E-cores take 2.12x the time, 0.94x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.09x the time, 0.94x the package energy
- **RQ2** P4 4x1 vs E4 4x1: E-cores take 2.12x the time, 0.93x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.33x the time, 0.81x the package energy
- **RQ2** P8ht 2x4 vs E8 2x4: E-cores take 1.35x the time, 0.81x the package energy
- **RQ2** P8ht 8x1 vs E8 8x1: E-cores take 1.35x the time, 0.82x the package energy
- **RQ2** P8ht 4x2 vs E8 4x2: E-cores take 1.34x the time, 0.82x the package energy
- **RQ3** 4 threads: best unpinned `U4 4x1` 4.401 s vs best pinned `P4 2x2` 4.417 s (1.00x); energy 126.1 vs 97.0 J (1.30x)
- **RQ3** 8 threads: best unpinned `U8 1x8` 4.686 s vs best pinned `P8ht 1x8` 4.280 s (1.09x); energy 117.0 vs 92.3 J (1.27x)
- **RQ3** 12 threads: best unpinned `U12 12x1` 4.402 s vs best pinned `A12 6x2` 4.370 s (1.01x); energy 121.5 vs 121.3 J (1.00x)
- **RQ3** 16 threads: best unpinned `U16 1x16` 4.009 s vs best pinned `A16 1x16` 4.013 s (1.00x); energy 117.3 vs 117.3 J (1.00x)

