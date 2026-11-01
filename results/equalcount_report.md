# Sweep report: `equalcount.csv`

## Data quality

- runs: 183 total, 0 throttled (excluded), 0 on battery/unknown power (excluded), 183 kept
- G3_circuit.rcm.csr: tol 1e-08; 35/35 runs converged with true relative residual <= tol (max 9.99e-09); iterations 6602-6678 (spread 1.2%)
- apache2.rcm.csr: tol 1e-08; 39/39 runs converged with true relative residual <= tol (max 9.70e-09); iterations 4923-4932 (spread 0.2%)
- cant.rcm.csr: tol 1e-08; 37/37 runs converged with true relative residual <= tol (max 1.00e-08); iterations 9498-9584 (spread 0.9%)
- ecology2.rcm.csr: tol 1e-08; 37/37 runs converged with true relative residual <= tol (max 9.95e-09); iterations 6233-6233 (spread 0.0%)
- thermal2.rcm.csr: tol 1e-08; 35/35 runs converged with true relative residual <= tol (max 1.00e-08); iterations 4330-4333 (spread 0.1%)
- idle baseline: pkg 0.34 W, core 0.03 W, uncore 0.00 W, psys 0.81 W

## Per-matrix results (median over reps)

### G3_circuit

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 31.203 | 0.8 | 2.06 | 820.8 | 0.82 | 26.3 | 0.0 | 0.0 |
| P3 1x3 | P-cores | 35.158 | 0.4 | 1.83 | 808.9 | 0.81 | 23.0 | 0.0 | 0.0 |
| P2 1x2 | P-cores | 41.749 | 1.1 | 1.54 | 802.7 | 0.80 | 19.2 | 0.0 | 0.0 |
| E4s 1x4 | E-cores | 53.302 | 0.5 | 1.21 | 580.4 | 0.58 | 10.9 | 0.0 | 0.1 |
| E3s 1x3 | E-cores | 63.662 | 0.4 | 1.01 | 653.8 | 0.65 | 10.3 | 0.0 | 0.1 |
| P1 1x1 | P-cores | 64.309 | 0.1 | 1.00 | 1001.4 | 1.00 | 15.6 | 0.0 | 0.0 |
| E2s 1x2 | E-cores | 69.886 | 0.9 | 0.92 | 713.7 | 0.71 | 10.2 | 0.0 | 0.1 |
| E4 1x4 | E-cores | 81.070 | 0.2 | 0.79 | 878.3 | 0.88 | 10.8 | 0.0 | 0.1 |
| E3 1x3 | E-cores | 81.578 | 0.1 | 0.79 | 853.5 | 0.85 | 10.5 | 0.0 | 0.1 |
| E2 1x2 | E-cores | 86.247 | 0.2 | 0.75 | 875.7 | 0.87 | 10.2 | 0.0 | 0.0 |
| E1 1x1 | E-cores | 119.714 | 1.0 | 0.54 | 1106.9 | 1.11 | 9.2 | 0.0 | 0.0 |

- **RQ1** fastest: `P4 1x4` (31.203 s)
  - lowest energy: `E4s 1x4` (580.4 J) -> DIVERGE: fastest costs 1.41x the energy, frugal is 1.71x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.86x the time, 1.11x the package energy
- **RQ2** P2 1x2 vs E2 1x2: E-cores take 2.07x the time, 1.09x the package energy
- **RQ2** P2 1x2 vs E2s 1x2: E-cores take 1.67x the time, 0.89x the package energy
- **RQ2** P3 1x3 vs E3 1x3: E-cores take 2.32x the time, 1.06x the package energy
- **RQ2** P3 1x3 vs E3s 1x3: E-cores take 1.81x the time, 0.81x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.60x the time, 1.07x the package energy
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.71x the time, 0.71x the package energy

### apache2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 9.912 | 2.4 | 2.49 | 298.3 | 0.77 | 30.1 | 0.1 | 0.0 |
| P3 1x3 | P-cores | 11.707 | 1.8 | 2.11 | 297.7 | 0.77 | 25.4 | 0.0 | 0.0 |
| P2 1x2 | P-cores | 14.679 | 0.6 | 1.68 | 305.5 | 0.79 | 20.8 | 0.0 | 0.0 |
| E4s 1x4 | E-cores | 19.284 | 1.5 | 1.28 | 238.2 | 0.62 | 12.4 | 0.1 | 0.1 |
| E3s 1x3 | E-cores | 22.990 | 0.1 | 1.07 | 283.3 | 0.73 | 12.3 | 0.0 | 0.1 |
| E2s 1x2 | E-cores | 24.645 | 0.6 | 1.00 | 296.4 | 0.77 | 12.0 | 0.0 | 0.1 |
| P1 1x1 | P-cores | 24.704 | 0.1 | 1.00 | 387.0 | 1.00 | 15.7 | 0.0 | 0.0 |
| E3 1x3 | E-cores | 30.301 | 4.9 | 0.82 | 318.6 | 0.82 | 10.5 | 0.0 | 0.1 |
| E4 1x4 | E-cores | 30.967 | 0.2 | 0.80 | 328.7 | 0.85 | 10.6 | 0.0 | 0.1 |
| E2 1x2 | E-cores | 34.721 | 6.2 | 0.71 | 335.9 | 0.87 | 9.7 | 0.0 | 0.1 |
| E1 1x1 | E-cores | 46.085 | 1.2 | 0.54 | 429.2 | 1.11 | 9.3 | 0.0 | 0.1 |

- **RQ1** fastest: `P4 1x4` (9.912 s)
  - lowest energy: `E4s 1x4` (238.2 J) -> DIVERGE: fastest costs 1.25x the energy, frugal is 1.95x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.87x the time, 1.11x the package energy
- **RQ2** P2 1x2 vs E2 1x2: E-cores take 2.37x the time, 1.10x the package energy
- **RQ2** P2 1x2 vs E2s 1x2: E-cores take 1.68x the time, 0.97x the package energy
- **RQ2** P3 1x3 vs E3 1x3: E-cores take 2.59x the time, 1.07x the package energy
- **RQ2** P3 1x3 vs E3s 1x3: E-cores take 1.96x the time, 0.95x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 3.12x the time, 1.10x the package energy
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.95x the time, 0.80x the package energy

### cant

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 8.935 | 2.7 | 2.71 | 271.2 | 0.75 | 30.4 | 0.1 | 0.1 |
| P3 1x3 | P-cores | 10.495 | 2.0 | 2.30 | 269.1 | 0.75 | 25.6 | 0.1 | 0.1 |
| P2 1x2 | P-cores | 12.732 | 1.7 | 1.90 | 282.8 | 0.79 | 22.2 | 0.0 | 0.0 |
| E4s 1x4 | E-cores | 16.057 | 0.1 | 1.51 | 238.9 | 0.66 | 14.9 | 0.1 | 0.2 |
| E3s 1x3 | E-cores | 19.792 | 1.1 | 1.22 | 269.6 | 0.75 | 13.6 | 0.1 | 0.1 |
| P1 1x1 | P-cores | 24.176 | 1.4 | 1.00 | 359.9 | 1.00 | 14.9 | 0.0 | 0.0 |
| E4 1x4 | E-cores | 24.446 | 11.5 | 0.99 | 277.9 | 0.77 | 11.4 | 0.1 | 0.1 |
| E3 1x3 | E-cores | 24.877 | 0.6 | 0.97 | 281.9 | 0.78 | 11.3 | 0.1 | 0.1 |
| E2s 1x2 | E-cores | 26.442 | 0.1 | 0.91 | 306.7 | 0.85 | 11.6 | 0.1 | 0.1 |
| E2 1x2 | E-cores | 28.765 | 0.1 | 0.84 | 321.4 | 0.89 | 11.2 | 0.0 | 0.1 |
| E1 1x1 | E-cores | 50.824 | 0.3 | 0.48 | 447.4 | 1.24 | 8.8 | 0.0 | 0.1 |

- **RQ1** fastest: `P4 1x4` (8.935 s)
  - lowest energy: `E4s 1x4` (238.9 J) -> DIVERGE: fastest costs 1.14x the energy, frugal is 1.80x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 2.10x the time, 1.24x the package energy
- **RQ2** P2 1x2 vs E2 1x2: E-cores take 2.26x the time, 1.14x the package energy
- **RQ2** P2 1x2 vs E2s 1x2: E-cores take 2.08x the time, 1.08x the package energy
- **RQ2** P3 1x3 vs E3 1x3: E-cores take 2.37x the time, 1.05x the package energy
- **RQ2** P3 1x3 vs E3s 1x3: E-cores take 1.89x the time, 1.00x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.74x the time, 1.02x the package energy
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.80x the time, 0.88x the package energy

### ecology2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 16.611 | 0.5 | 2.22 | 443.0 | 0.78 | 26.7 | 0.1 | 0.0 |
| P3 1x3 | P-cores | 19.202 | 0.6 | 1.92 | 437.2 | 0.77 | 22.8 | 0.0 | 0.0 |
| P2 1x2 | P-cores | 23.565 | 0.6 | 1.56 | 444.4 | 0.78 | 18.9 | 0.0 | 0.0 |
| E4s 1x4 | E-cores | 30.574 | 0.3 | 1.21 | 330.4 | 0.58 | 10.8 | 0.1 | 0.1 |
| E3s 1x3 | E-cores | 35.331 | 0.2 | 1.04 | 430.9 | 0.76 | 12.2 | 0.0 | 0.1 |
| P1 1x1 | P-cores | 36.845 | 1.1 | 1.00 | 567.0 | 1.00 | 15.4 | 0.0 | 0.0 |
| E2s 1x2 | E-cores | 37.390 | 0.2 | 0.99 | 447.3 | 0.79 | 12.0 | 0.0 | 0.1 |
| E4 1x4 | E-cores | 48.150 | 2.2 | 0.77 | 509.3 | 0.90 | 10.6 | 0.0 | 0.1 |
| E3 1x3 | E-cores | 48.493 | 0.5 | 0.76 | 496.1 | 0.88 | 10.2 | 0.0 | 0.1 |
| E2 1x2 | E-cores | 53.402 | 5.4 | 0.69 | 516.1 | 0.91 | 9.7 | 0.0 | 0.1 |
| E1 1x1 | E-cores | 69.773 | 0.3 | 0.53 | 641.0 | 1.13 | 9.2 | 0.0 | 0.1 |

- **RQ1** fastest: `P4 1x4` (16.611 s)
  - lowest energy: `E4s 1x4` (330.4 J) -> DIVERGE: fastest costs 1.34x the energy, frugal is 1.84x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.89x the time, 1.13x the package energy
- **RQ2** P2 1x2 vs E2 1x2: E-cores take 2.27x the time, 1.16x the package energy
- **RQ2** P2 1x2 vs E2s 1x2: E-cores take 1.59x the time, 1.01x the package energy
- **RQ2** P3 1x3 vs E3 1x3: E-cores take 2.53x the time, 1.13x the package energy
- **RQ2** P3 1x3 vs E3s 1x3: E-cores take 1.84x the time, 0.99x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.90x the time, 1.15x the package energy
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.84x the time, 0.75x the package energy

### thermal2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 19.274 | 0.4 | 2.77 | 556.2 | 0.70 | 28.9 | 0.0 | 0.0 |
| P3 1x3 | P-cores | 22.371 | 0.1 | 2.39 | 548.4 | 0.69 | 24.5 | 0.0 | 0.0 |
| P2 1x2 | P-cores | 30.353 | 0.8 | 1.76 | 575.2 | 0.72 | 18.9 | 0.0 | 0.0 |
| E4s 1x4 | E-cores | 31.240 | 0.1 | 1.71 | 427.8 | 0.54 | 13.7 | 0.0 | 0.1 |
| E3s 1x3 | E-cores | 38.563 | 0.4 | 1.38 | 484.9 | 0.61 | 12.6 | 0.0 | 0.1 |
| E4 1x4 | E-cores | 40.069 | 0.1 | 1.33 | 524.2 | 0.66 | 13.1 | 0.0 | 0.1 |
| E3 1x3 | E-cores | 43.835 | 0.0 | 1.22 | 551.8 | 0.69 | 12.6 | 0.0 | 0.1 |
| E2s 1x2 | E-cores | 49.616 | 1.4 | 1.08 | 590.8 | 0.74 | 11.9 | 0.0 | 0.0 |
| P1 1x1 | P-cores | 53.366 | 0.3 | 1.00 | 794.9 | 1.00 | 14.9 | 0.0 | 0.0 |
| E2 1x2 | E-cores | 54.130 | 0.1 | 0.99 | 618.7 | 0.78 | 11.4 | 0.0 | 0.0 |
| E1 1x1 | E-cores | 94.439 | 0.5 | 0.57 | 863.5 | 1.09 | 9.1 | 0.0 | 0.0 |

- **RQ1** fastest: `P4 1x4` (19.274 s)
  - lowest energy: `E4s 1x4` (427.8 J) -> DIVERGE: fastest costs 1.30x the energy, frugal is 1.62x slower
- **RQ2** P1 1x1 vs E1 1x1: E-cores take 1.77x the time, 1.09x the package energy
- **RQ2** P2 1x2 vs E2 1x2: E-cores take 1.78x the time, 1.08x the package energy
- **RQ2** P2 1x2 vs E2s 1x2: E-cores take 1.63x the time, 1.03x the package energy
- **RQ2** P3 1x3 vs E3 1x3: E-cores take 1.96x the time, 1.01x the package energy
- **RQ2** P3 1x3 vs E3s 1x3: E-cores take 1.72x the time, 0.88x the package energy
- **RQ2** P4 1x4 vs E4 1x4: E-cores take 2.08x the time, 0.94x the package energy
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.62x the time, 0.77x the package energy

