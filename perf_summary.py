#!/usr/bin/env python3
"""Summarise perf_check.sh output: per config, P-core vs E-core cycles,
instructions, PAUSE cycles and average active frequency (median over reps)."""
import glob, os, re, sys
from collections import defaultdict
from statistics import median

d = sys.argv[1] if len(sys.argv) > 1 else "results/perf"
P = set(range(8))
runs = defaultdict(list)
for f in sorted(glob.glob(os.path.join(d, "*.perf.csv"))):
    label = re.sub(r"_r\d+\.perf\.csv$", "", os.path.basename(f))
    run = dict(re.findall(r"(\w+)=([^ ]+)", open(f.replace(".perf.csv", ".run.txt")).read()))
    acc = defaultdict(float)
    for line in open(f):
        x = line.strip().split(",")
        if len(x) < 4 or not x[0].startswith("CPU"):
            continue
        try:
            v = float(x[1])
        except ValueError:
            continue                      # <not counted> / <not supported>
        cpu = int(x[0][3:])
        ev = x[3].split("/")[1] if "/" in x[3] else x[3]
        acc[("P" if cpu in P else "E", ev)] += v
    acc["time"] = float(run["time_s"]); acc["e_pkg"] = float(run["e_pkg_j"])
    acc["wall"] = acc["time"]
    runs[label].append(acc)

def med(rs, k): return median(r.get(k, 0.0) for r in rs)

print(f"# perf counter check ({d})\n")
print("Counts cover the whole mpirun (setup + solve); solve is ~90% of it.\n")
print("| config | solve s | E_pkg J | P instr (1e9) | P cycles (1e9) | P IPC | P PAUSE % of cycles | P C0-wait % | E instr (1e9) | E cycles (1e9) |")
print("|---|---|---|---|---|---|---|---|---|---|")
order = ["P4-mpi", "P4-omp", "M8-mpi", "M8-omp", "A12-mpi", "A12-omp", "A12-ompactive"]
for lab in [l for l in order if l in runs] + [l for l in runs if l not in order]:
    rs = runs[lab]
    pc, pi = med(rs, ("P", "cycles")), med(rs, ("P", "instructions"))
    pp, pw = med(rs, ("P", "cpu_clk_unhalted.pause")), med(rs, ("P", "cpu_clk_unhalted.c0_wait"))
    ec, ei = med(rs, ("E", "cycles")), med(rs, ("E", "instructions"))
    print(f"| {lab} | {med(rs,'time'):.2f} | {med(rs,'e_pkg'):.1f} | {pi/1e9:.1f} | {pc/1e9:.1f} | "
          f"{pi/pc if pc else 0:.2f} | {100*pp/pc if pc else 0:.1f} | {100*pw/pc if pc else 0:.1f} | "
          f"{ei/1e9:.1f} | {ec/1e9:.1f} |")
