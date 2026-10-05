# Sweep report: `spin.csv`

## Data quality

- runs: 117 total, 0 throttled (excluded), 0 on battery/unknown power (excluded), 117 kept
- iteration count IDENTICAL across configs for G3_circuit.rcm.csr
- iteration count IDENTICAL across configs for thermal2.rcm.csr
- iteration count IDENTICAL across configs for ecology2.rcm.csr
- idle baseline: pkg 0.34 W, core 0.03 W, uncore 0.00 W, psys 0.81 W

## Per-matrix results (median over reps)

### G3_circuit

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4 1x4 | P-cores | 4.679 | 2.6 | nan | 121.8 | nan | 26.0 | 0.0 | 0.0 |
| P4-ompactive 1x4 | P-cores | 4.694 | 1.0 | nan | 121.9 | nan | 26.0 | 0.0 | 0.0 |
| P4 4x1 | P-cores | 4.702 | 0.5 | nan | 121.1 | nan | 25.8 | 0.7 | 1.0 |
| A12-ompactive 1x12 | Mixed P+E | 5.016 | 1.4 | nan | 114.9 | nan | 22.9 | 0.1 | 0.0 |
| A12 1x12 | Mixed P+E | 5.019 | 0.3 | nan | 115.0 | nan | 22.9 | 0.1 | 0.0 |
| A12 12x1 | Mixed P+E | 5.059 | 0.4 | nan | 191.9 | nan | 37.9 | 6.9 | 40.4 |
| A12-yield 12x1 | Mixed P+E | 5.065 | 0.2 | nan | 183.9 | nan | 36.3 | 6.5 | 40.2 |
| M8 8x1 | Mixed P+E | 6.002 | 0.3 | nan | 200.0 | nan | 33.3 | 5.1 | 40.5 |
| M8-yield 8x1 | Mixed P+E | 6.037 | 0.1 | nan | 192.8 | nan | 31.9 | 5.3 | 40.2 |
| M8 1x8 | Mixed P+E | 6.129 | 0.1 | nan | 119.7 | nan | 19.5 | 0.0 | 0.0 |
| M8-ompactive 1x8 | Mixed P+E | 6.148 | 0.9 | nan | 120.0 | nan | 19.5 | 0.0 | 0.0 |
| A12-omppassive 1x12 | Mixed P+E | 17.406 | 0.6 | nan | 111.8 | nan | 6.4 | 1.7 | 0.1 |
| M8-omppassive 1x8 | Mixed P+E | 21.026 | 0.1 | nan | 123.3 | nan | 5.9 | 1.1 | 0.1 |

- **RQ1** fastest: `P4 1x4` (4.679 s)
  - lowest energy: `A12-omppassive 1x12` (111.8 J) -> DIVERGE: fastest costs 1.09x the energy, frugal is 3.72x slower

### ecology2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| P4-ompactive 1x4 | P-cores | 2.621 | 0.9 | nan | 68.8 | nan | 26.2 | 0.1 | 0.0 |
| P4 4x1 | P-cores | 2.643 | 0.5 | nan | 71.1 | nan | 26.9 | 0.6 | 1.3 |
| P4 1x4 | P-cores | 2.666 | 1.7 | nan | 71.3 | nan | 26.7 | 0.0 | 0.0 |
| A12-yield 12x1 | Mixed P+E | 2.876 | 0.5 | nan | 107.3 | nan | 37.3 | 5.5 | 44.3 |
| A12 12x1 | Mixed P+E | 2.882 | 0.3 | nan | 111.5 | nan | 38.7 | 5.1 | 43.6 |
| A12 1x12 | Mixed P+E | 2.932 | 0.4 | nan | 70.4 | nan | 24.0 | 0.1 | 0.0 |
| A12-ompactive 1x12 | Mixed P+E | 2.932 | 0.3 | nan | 70.7 | nan | 24.1 | 0.1 | 0.0 |
| M8 8x1 | Mixed P+E | 3.649 | 0.3 | nan | 125.2 | nan | 34.3 | 5.7 | 47.1 |
| M8-yield 8x1 | Mixed P+E | 3.659 | 0.3 | nan | 118.4 | nan | 32.4 | 5.6 | 47.1 |
| M8-ompactive 1x8 | Mixed P+E | 3.718 | 0.2 | nan | 72.7 | nan | 19.5 | 0.1 | 0.0 |
| M8 1x8 | Mixed P+E | 3.720 | 0.2 | nan | 72.2 | nan | 19.4 | 0.1 | 0.0 |
| A12-omppassive 1x12 | Mixed P+E | 10.264 | 28.4 | nan | 70.2 | nan | 6.8 | 2.1 | 0.1 |
| M8-omppassive 1x8 | Mixed P+E | 13.558 | 0.5 | nan | 80.0 | nan | 5.9 | 1.7 | 0.1 |

- **RQ1** fastest: `P4-ompactive 1x4` (2.621 s)
  - lowest energy: `P4-ompactive 1x4` (68.8 J) -> SAME config

### thermal2

| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |
|---|---|---|---|---|---|---|---|---|---|
| A12 1x12 | Mixed P+E | 4.392 | 0.5 | nan | 121.2 | nan | 27.6 | 0.1 | 0.0 |
| A12-ompactive 1x12 | Mixed P+E | 4.397 | 0.1 | nan | 121.6 | nan | 27.7 | 0.1 | 0.0 |
| A12-yield 12x1 | Mixed P+E | 4.400 | 0.2 | nan | 180.5 | nan | 41.0 | 3.9 | 40.9 |
| P4-ompactive 1x4 | P-cores | 4.405 | 2.4 | nan | 127.1 | nan | 28.8 | 0.0 | 0.0 |
| A12 12x1 | Mixed P+E | 4.407 | 0.4 | nan | 185.6 | nan | 42.1 | 3.9 | 40.4 |
| P4 4x1 | P-cores | 4.417 | 1.0 | nan | 127.6 | nan | 28.9 | 0.4 | 1.4 |
| P4 1x4 | P-cores | 4.420 | 1.1 | nan | 126.7 | nan | 28.7 | 0.0 | 0.0 |
| M8-yield 8x1 | Mixed P+E | 5.231 | 0.4 | nan | 181.6 | nan | 34.7 | 2.9 | 39.7 |
| M8 8x1 | Mixed P+E | 5.234 | 0.3 | nan | 191.1 | nan | 36.5 | 2.9 | 39.7 |
| M8 1x8 | Mixed P+E | 5.341 | 0.3 | nan | 121.2 | nan | 22.7 | 0.0 | 0.0 |
| M8-ompactive 1x8 | Mixed P+E | 5.345 | 0.4 | nan | 120.8 | nan | 22.6 | 0.0 | 0.0 |
| M8-omppassive 1x8 | Mixed P+E | 6.703 | 0.4 | nan | 120.6 | nan | 18.0 | 1.0 | 0.1 |
| A12-omppassive 1x12 | Mixed P+E | 13.900 | 0.2 | nan | 104.9 | nan | 7.5 | 1.8 | 0.1 |

- **RQ1** fastest: `A12 1x12` (4.392 s)
  - lowest energy: `A12-omppassive 1x12` (104.9 J) -> DIVERGE: fastest costs 1.16x the energy, frugal is 3.17x slower

