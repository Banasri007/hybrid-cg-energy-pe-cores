#!/usr/bin/env python3
"""Summarise a sweep CSV: per-config medians, data-quality checks, RQ1-RQ3
answers, and per-matrix plots.

    python3 analyze.py results/sweep.csv

Writes <csv>_summary.csv, <csv>_report.md and <csv>_plots/<matrix>_{time,energy}.png
"""
import csv
import os
import re
import sys
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# fixed categorical order (core-type class -> colour), never cycled
CLASSES = ["P-cores", "E-cores", "Mixed P+E", "Unpinned"]
COLOR = dict(zip(CLASSES, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]))
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def core_class(label):
    return {"P": "P-cores", "E": "E-cores", "M": "Mixed P+E", "A": "Mixed P+E", "U": "Unpinned"}[label[0]]


def fnum(x):
    try:
        return float(x)
    except ValueError:
        return float("nan")


def idle_baseline(meta_path):
    """last idle_baseline line in the .meta.txt -> {'pkg': W, ...} (None if -1)"""
    if not os.path.exists(meta_path):
        return {}
    lines = [l for l in open(meta_path) if l.startswith("idle_baseline:")]
    if not lines:
        return {}
    d = dict(re.findall(r"p_(\w+)_w=([-0-9.]+)", lines[-1]))
    return {k: float(v) for k, v in d.items() if float(v) >= 0}


def main(path):
    base = path[:-4]
    rows = list(csv.DictReader(open(path)))
    # a clean, separately measured baseline beats the one taken at sweep start
    clean = os.path.join(os.path.dirname(path), "idle_baseline.txt")
    idle = idle_baseline(clean) or idle_baseline(base + ".meta.txt")
    notes = []

    # ---- data quality ----
    bad_ac = [r for r in rows if r["ac_online"] != "1"]
    throttled = [r for r in rows if fnum(r["throttle_delta"]) > 0]
    keep = [r for r in rows if r not in bad_ac and r not in throttled]
    notes.append(f"runs: {len(rows)} total, {len(throttled)} throttled (excluded), "
                 f"{len(bad_ac)} on battery/unknown power (excluded), {len(keep)} kept")
    iters_by_m = defaultdict(set)
    for r in keep:
        iters_by_m[r["matrix"]].add(r["iters"])
    for m, s in iters_by_m.items():
        notes.append(f"iteration count {'IDENTICAL' if len(s) == 1 else 'MISMATCH ' + str(sorted(s))} "
                     f"across configs for {os.path.basename(m)}")
    have_energy = any(fnum(r["e_pkg_j"]) >= 0 for r in keep)
    if not have_energy:
        notes.append("RAPL energy not available in this CSV (all -1): runtime-only analysis")

    # ---- per-config aggregation ----
    groups = defaultdict(list)
    for r in keep:
        dyn = "" if r["sched"].startswith("static") else " dyn"
        key = (r["matrix"], r["label"], int(r["ranks"]), int(r["threads"]), dyn)
        groups[key].append(r)

    summary = []
    for (m, label, R, T, dyn), rs in groups.items():
        t = np.array([fnum(r["time_s"]) for r in rs])
        e = np.array([fnum(r["e_pkg_j"]) for r in rs])
        e = e[e >= 0]
        it = int(rs[0]["iters"])
        s = dict(matrix=os.path.basename(m).replace(".rcm.csr", ""), label=label,
                 cls=core_class(label), ranks=R, threads=T, cfg=f"{label} {R}x{T}{dyn}",
                 n=len(rs), time_med=float(np.median(t)),
                 time_cv=float(100 * t.std(ddof=1) / t.mean()) if len(t) > 1 else float("nan"),
                 e_pkg_med=float(np.median(e)) if len(e) else float("nan"),
                 e_cv=float(100 * e.std(ddof=1) / e.mean()) if len(e) > 1 else float("nan"),
                 iters=it,
                 halo_frac=float(np.median([fnum(r["halo_s"]) / fnum(r["time_s"]) for r in rs])),
                 allred_frac=float(np.median([fnum(r["allreduce_s"]) / fnum(r["time_s"]) for r in rs])))
        s["power_w"] = s["e_pkg_med"] / s["time_med"]
        s["iters_per_j"] = it / s["e_pkg_med"]
        s["e_dyn_med"] = s["e_pkg_med"] - idle["pkg"] * s["time_med"] if "pkg" in idle else float("nan")
        summary.append(s)

    by_m = defaultdict(list)
    for s in summary:
        by_m[s["matrix"]].append(s)
    for m, ss in by_m.items():
        ref = next((s for s in ss if s["cfg"] == "P1 1x1"), None)
        for s in ss:
            s["speedup_vs_P1"] = ref["time_med"] / s["time_med"] if ref else float("nan")
            s["energy_vs_P1"] = s["e_pkg_med"] / ref["e_pkg_med"] if ref else float("nan")

    cols = ["matrix", "cfg", "cls", "ranks", "threads", "n", "iters", "time_med", "time_cv",
            "speedup_vs_P1", "e_pkg_med", "e_cv", "e_dyn_med", "energy_vs_P1", "power_w",
            "iters_per_j", "halo_frac", "allred_frac"]
    with open(base + "_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for s in sorted(summary, key=lambda s: (s["matrix"], s["time_med"])):
            w.writerow({k: (f"{v:.4g}" if isinstance(v, float) else v) for k, v in s.items()})

    # ---- report ----
    out = [f"# Sweep report: `{os.path.basename(path)}`", "", "## Data quality", ""]
    out += [f"- {n}" for n in notes]
    if idle:
        out.append(f"- idle baseline: " + ", ".join(f"{k} {v:.2f} W" for k, v in idle.items()))
    out += ["", "## Per-matrix results (median over reps)", ""]
    for m in sorted(by_m):
        ss = sorted(by_m[m], key=lambda s: s["time_med"])
        out += [f"### {m}", "",
                "| config | class | time (s) | CV % | speedup vs P1 | E_pkg (J) | E vs P1 | power (W) | halo % | allreduce % |",
                "|---|---|---|---|---|---|---|---|---|---|"]
        for s in ss:
            out.append(f"| {s['cfg']} | {s['cls']} | {s['time_med']:.3f} | {s['time_cv']:.1f} | "
                       f"{s['speedup_vs_P1']:.2f} | {s['e_pkg_med']:.1f} | {s['energy_vs_P1']:.2f} | "
                       f"{s['power_w']:.1f} | {100*s['halo_frac']:.1f} | {100*s['allred_frac']:.1f} |")
        out.append("")

        # RQ1: runtime-optimal vs energy-optimal
        fastest = ss[0]
        out.append(f"- **RQ1** fastest: `{fastest['cfg']}` ({fastest['time_med']:.3f} s)")
        if have_energy:
            frugal = min(ss, key=lambda s: s["e_pkg_med"])
            out.append(f"  - lowest energy: `{frugal['cfg']}` ({frugal['e_pkg_med']:.1f} J) -> "
                       + ("SAME config" if frugal is fastest else
                          "TIE within 3% (noise level)" if fastest["e_pkg_med"] <= 1.03 * frugal["e_pkg_med"] else
                          f"DIVERGE: fastest costs {fastest['e_pkg_med']/frugal['e_pkg_med']:.2f}x the energy, "
                          f"frugal is {frugal['time_med']/fastest['time_med']:.2f}x slower"))
        # RQ2: P vs E at matched core counts, same split
        idx = {s["cfg"]: s for s in ss}
        pairs = [(p, e) for p, e in [("P1", "E1"), ("P4", "E4"), ("P8ht", "E8")]]
        for p, e in pairs:
            for s in ss:
                if s["label"] == p and not s["cfg"].endswith("dyn"):
                    o = idx.get(s["cfg"].replace(p, e, 1))
                    if o:
                        line = (f"- **RQ2** {s['cfg']} vs {o['cfg']}: E-cores take "
                                f"{o['time_med']/s['time_med']:.2f}x the time")
                        if have_energy:
                            line += f", {o['e_pkg_med']/s['e_pkg_med']:.2f}x the package energy"
                        out.append(line)
        # RQ3: unpinned vs best pinned at same total thread count
        for tot in sorted({s["ranks"] * s["threads"] for s in ss if s["cls"] == "Unpinned"}):
            un = [s for s in ss if s["cls"] == "Unpinned" and s["ranks"] * s["threads"] == tot]
            pin = [s for s in ss if s["cls"] != "Unpinned" and s["ranks"] * s["threads"] == tot]
            if un and pin:
                bu, bp = min(un, key=lambda s: s["time_med"]), min(pin, key=lambda s: s["time_med"])
                line = (f"- **RQ3** {tot} threads: best unpinned `{bu['cfg']}` {bu['time_med']:.3f} s vs "
                        f"best pinned `{bp['cfg']}` {bp['time_med']:.3f} s ({bu['time_med']/bp['time_med']:.2f}x)")
                if have_energy:
                    eu = min(un, key=lambda s: s["e_pkg_med"])["e_pkg_med"]
                    ep = min(pin, key=lambda s: s["e_pkg_med"])["e_pkg_med"]
                    line += f"; energy {eu:.1f} vs {ep:.1f} J ({eu/ep:.2f}x)"
                out.append(line)
        out.append("")
    open(base + "_report.md", "w").write("\n".join(out) + "\n")

    # ---- plots: one measure per chart (no dual axes) ----
    pdir = base + "_plots"
    os.makedirs(pdir, exist_ok=True)
    metrics = [("time_med", "Solve time (s), median", "time")]
    if have_energy:
        metrics.append(("e_pkg_med", "Package energy (J), median", "energy"))
    for m, ss in by_m.items():
        ss = sorted(ss, key=lambda s: (CLASSES.index(s["cls"]), s["ranks"] * s["threads"], -s["ranks"]))
        for key, xlabel, tag in metrics:
            fig, ax = plt.subplots(figsize=(7, 0.32 * len(ss) + 1.2), facecolor=SURFACE)
            ax.set_facecolor(SURFACE)
            y = np.arange(len(ss))[::-1]
            ax.barh(y, [s[key] for s in ss], height=0.7, color=[COLOR[s["cls"]] for s in ss],
                    edgecolor=SURFACE, linewidth=2)
            ax.set_yticks(y, [s["cfg"] for s in ss], fontsize=8, color=INK)
            ax.set_xlabel(xlabel, color=INK2, fontsize=9)
            ax.set_title(f"{m}: {xlabel.split(',')[0].lower()} by configuration", color=INK,
                         fontsize=10, loc="left")
            ax.grid(axis="x", color=GRID, linewidth=0.8)
            ax.set_axisbelow(True)
            for sp in ["top", "right", "left"]:
                ax.spines[sp].set_visible(False)
            ax.spines["bottom"].set_color(GRID)
            ax.tick_params(axis="x", colors=INK2, labelsize=8)
            ax.tick_params(axis="y", length=0)
            present = [c for c in CLASSES if any(s["cls"] == c for s in ss)]
            ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=COLOR[c]) for c in present],
                      labels=present, frameon=False, fontsize=8, loc="lower right")
            fig.tight_layout()
            fig.savefig(os.path.join(pdir, f"{m}_{tag}.png"), dpi=150)
            plt.close(fig)

    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/sweep.csv")
