# Sweep report: `converge.csv`

## Data quality

- runs: 30 total, 0 throttled (excluded), 0 on battery/unknown power (excluded), 30 kept
- G3_circuit.rcm.csr: tol 1e-08; 6/6 runs converged with true relative residual <= tol (max 9.81e-09); iterations 6606-6651 (spread 0.7%)
- apache2.rcm.csr: tol 1e-08; 6/6 runs converged with true relative residual <= tol (max 9.96e-09); iterations 4914-4927 (spread 0.3%)
- cant.rcm.csr: tol 1e-08; 6/6 runs converged with true relative residual <= tol (max 9.89e-09); iterations 9463-9522 (spread 0.6%)
- ecology2.rcm.csr: tol 1e-08; 6/6 runs converged with true relative residual <= tol (max 9.95e-09); iterations 6233-6233 (spread 0.0%)
- thermal2.rcm.csr: tol 1e-08; 6/6 runs converged with true relative residual <= tol (max 1.00e-08); iterations 4330-4332 (spread 0.0%)
- idle baseline: pkg 0.34 W, core 0.03 W, uncore 0.00 W, psys 0.81 W

## Per-matrix results (median over reps)

### G3_circuit

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| U16 1x16 | Unpinned | 30.439 | nan | nan | 718.4 | nan | 23.6 | 0.1 | 0.0 |
| A16 1x16 | Mixed P+E | 30.531 | nan | nan | 720.3 | nan | 23.6 | 0.1 | 0.0 |
| P4 1x4 | P-cores | 31.002 | nan | nan | 816.6 | nan | 26.3 | 0.0 | 0.0 |
| P8ht 1x8 | P-cores | 32.612 | nan | nan | 722.4 | nan | 22.2 | 0.0 | 0.0 |
| E8 1x8 | E-cores | 44.284 | nan | nan | 575.3 | nan | 13.0 | 0.1 | 0.1 |
| E4s 1x4 | E-cores | 53.255 | nan | nan | 574.3 | nan | 10.8 | 0.0 | 0.1 |

- **RQ1** fastest: `U16 1x16` (30.439 s)
  - lowest energy: `E4s 1x4` (574.3 J) -> DIVERGE: fastest costs 1.25x the energy, frugal is 1.75x slower
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.72x the time, 0.70x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.36x the time, 0.80x the package energy
- **RQ3** 16 threads: best unpinned `U16 1x16` 30.439 s vs best pinned `A16 1x16` 30.531 s (1.00x); energy 718.4 vs 720.3 J (1.00x)

### apache2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| U16 1x16 | Unpinned | 9.863 | nan | nan | 272.7 | nan | 27.6 | 0.1 | 0.0 |
| P4 1x4 | P-cores | 9.881 | nan | nan | 294.4 | nan | 29.8 | 0.1 | 0.0 |
| A16 1x16 | Mixed P+E | 9.893 | nan | nan | 272.6 | nan | 27.6 | 0.1 | 0.0 |
| P8ht 1x8 | P-cores | 10.057 | nan | nan | 274.5 | nan | 27.3 | 0.1 | 0.0 |
| E8 1x8 | E-cores | 16.497 | nan | nan | 217.8 | nan | 13.2 | 0.1 | 0.2 |
| E4s 1x4 | E-cores | 19.256 | nan | nan | 234.6 | nan | 12.2 | 0.1 | 0.1 |

- **RQ1** fastest: `U16 1x16` (9.863 s)
  - lowest energy: `E8 1x8` (217.8 J) -> DIVERGE: fastest costs 1.25x the energy, frugal is 1.67x slower
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.95x the time, 0.80x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.64x the time, 0.79x the package energy
- **RQ3** 16 threads: best unpinned `U16 1x16` 9.863 s vs best pinned `A16 1x16` 9.893 s (1.00x); energy 272.7 vs 272.6 J (1.00x)

### cant

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| A16 1x16 | Mixed P+E | 7.010 | nan | nan | 263.8 | nan | 37.6 | 0.3 | 0.1 |
| U16 1x16 | Unpinned | 7.048 | nan | nan | 266.3 | nan | 37.8 | 0.3 | 0.1 |
| P8ht 1x8 | P-cores | 8.125 | nan | nan | 262.9 | nan | 32.4 | 0.1 | 0.1 |
| P4 1x4 | P-cores | 9.009 | nan | nan | 270.8 | nan | 30.1 | 0.1 | 0.1 |
| E8 1x8 | E-cores | 13.733 | nan | nan | 189.5 | nan | 13.8 | 0.2 | 0.2 |
| E4s 1x4 | E-cores | 15.989 | nan | nan | 236.3 | nan | 14.8 | 0.1 | 0.2 |

- **RQ1** fastest: `A16 1x16` (7.010 s)
  - lowest energy: `E8 1x8` (189.5 J) -> DIVERGE: fastest costs 1.39x the energy, frugal is 1.96x slower
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.77x the time, 0.87x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.69x the time, 0.72x the package energy
- **RQ3** 16 threads: best unpinned `U16 1x16` 7.048 s vs best pinned `A16 1x16` 7.010 s (1.01x); energy 266.3 vs 263.8 J (1.01x)

### ecology2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| A16 1x16 | Mixed P+E | 16.501 | nan | nan | 391.9 | nan | 23.8 | 0.1 | 0.0 |
| U16 1x16 | Unpinned | 16.541 | nan | nan | 393.5 | nan | 23.8 | 0.1 | 0.0 |
| P4 1x4 | P-cores | 16.590 | nan | nan | 440.5 | nan | 26.6 | 0.1 | 0.0 |
| P8ht 1x8 | P-cores | 16.940 | nan | nan | 398.0 | nan | 23.5 | 0.1 | 0.0 |
| E8 1x8 | E-cores | 26.089 | nan | nan | 330.2 | nan | 12.7 | 0.1 | 0.2 |
| E4s 1x4 | E-cores | 30.566 | nan | nan | 320.4 | nan | 10.5 | 0.1 | 0.1 |

- **RQ1** fastest: `A16 1x16` (16.501 s)
  - lowest energy: `E4s 1x4` (320.4 J) -> DIVERGE: fastest costs 1.22x the energy, frugal is 1.85x slower
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.84x the time, 0.73x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.54x the time, 0.83x the package energy
- **RQ3** 16 threads: best unpinned `U16 1x16` 16.541 s vs best pinned `A16 1x16` 16.501 s (1.00x); energy 393.5 vs 391.9 J (1.00x)

### thermal2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| A16 1x16 | Mixed P+E | 17.495 | nan | nan | 512.0 | nan | 29.3 | 0.1 | 0.0 |
| P8ht 1x8 | P-cores | 18.798 | nan | nan | 503.0 | nan | 26.8 | 0.0 | 0.0 |
| P4 1x4 | P-cores | 19.287 | nan | nan | 555.9 | nan | 28.8 | 0.0 | 0.0 |
| U16 1x16 | Unpinned | 21.337 | nan | nan | 569.5 | nan | 26.7 | 3.4 | 0.1 |
| E8 1x8 | E-cores | 24.916 | nan | nan | 407.2 | nan | 16.3 | 0.1 | 0.1 |
| E4s 1x4 | E-cores | 31.183 | nan | nan | 425.1 | nan | 13.6 | 0.0 | 0.1 |

- **RQ1** fastest: `A16 1x16` (17.495 s)
  - lowest energy: `E8 1x8` (407.2 J) -> DIVERGE: fastest costs 1.26x the energy, frugal is 1.42x slower
- **RQ2** P4 1x4 vs E4s 1x4: E-cores take 1.62x the time, 0.76x the package energy
- **RQ2** P8ht 1x8 vs E8 1x8: E-cores take 1.33x the time, 0.81x the package energy
- **RQ3** 16 threads: best unpinned `U16 1x16` 21.337 s vs best pinned `A16 1x16` 17.495 s (1.22x); energy 569.5 vs 512.0 J (1.11x)

