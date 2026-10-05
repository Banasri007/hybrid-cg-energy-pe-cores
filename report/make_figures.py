#!/usr/bin/env python3
"""Report figures (PNG, 200 dpi, black text on white for print).

    python3 report/make_figures.py      # from the project root
"""
import csv
import os
import re
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "report", "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
                     "font.size": 9, "axes.edgecolor": "#888888", "axes.linewidth": 0.6,
                     "xtick.color": "#333333", "ytick.color": "#333333"})
# fixed categorical order, never cycled
SER = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
CLASS_COL = {"P-cores": SER[0], "E-cores": SER[1], "Mixed P+E": SER[2], "Unpinned": SER[3]}
GRID = "#e4e3df"
MATRICES = ["thermal2", "G3_circuit", "ecology2", "apache2", "cant"]


def load_summary(name):
    by = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(ROOT, "results", f"{name}_summary.csv"))):
        by[r["matrix"]][r["cfg"]] = r
    return by


def style(ax, grid_axis="y"):
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


# ---------- Fig 1: system architecture ----------
def fig_architecture():
    layers = [
        ("Input layer", "SuiteSparse SPD matrices (.mtx) → CSR → RCM reordering → binary .csr"),
        ("MPI layer", "nnz-balanced row-block partition  ·  halo exchange of p (Isend/Irecv)\n2 × MPI_Allreduce per CG iteration"),
        ("OpenMP layer", "threaded SpMV (static / dynamic schedule)\nfused vector updates and reductions"),
        ("Placement layer", "per-rank CPU sets (taskset)  ·  OMP_PLACES + OMP_PROC_BIND\nP-only / E-only / mixed / unpinned"),
        ("Instrumentation", "RAPL package/core/uncore/psys around the solve loop\ntemperature  ·  throttle counters  ·  perf hardware counters"),
        ("Output layer", "one CSV row per run → medians, quality checks,\nRQ1–RQ3 analysis, plots"),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, len(layers) * 1.0 + 0.1); ax.axis("off")
    for i, (name, desc) in enumerate(layers):
        y = len(layers) - 1 - i + 0.12
        ax.add_patch(FancyBboxPatch((0.05, y), 2.3, 0.72, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc="#dbe8f8", ec="#2a78d6", lw=0.9))
        ax.text(1.2, y + 0.36, name, ha="center", va="center", fontsize=8.5, weight="bold")
        ax.add_patch(FancyBboxPatch((2.55, y), 7.4, 0.72, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc="white", ec="#888888", lw=0.7))
        ax.text(6.25, y + 0.36, desc, ha="center", va="center", fontsize=7.6, linespacing=1.4)
        if i < len(layers) - 1:
            ax.annotate("", xy=(1.2, y - 0.26), xytext=(1.2, y - 0.02),
                        arrowprops=dict(arrowstyle="-|>", color="#555555", lw=0.8))
    save(fig, "fig1_architecture.png")


# ---------- Fig 2: flowchart ----------
def fig_flowchart():
    steps = [
        ("Start: MPI_Init_thread (FUNNELED); load own row block (.csr)", "io"),
        ("Halo setup: find off-block columns, exchange index lists, renumber columns", "proc"),
        ("b = A·1,  x = 0,  r = p = b;  rr = r·r (Allreduce)", "proc"),
        ("Barrier → read RAPL, temperature, throttle counters → start timer", "meas"),
        ("Halo exchange: receive ghost entries of p from neighbour ranks", "mpi"),
        ("Threaded SpMV: Ap = A·p  (OpenMP, OMP_SCHEDULE)", "omp"),
        ("α = rr / (p·Ap)   [local dot + MPI_Allreduce #1]", "mpi"),
        ("x += αp,  r −= αAp,  rr_new = r·r   [fused loop + MPI_Allreduce #2]", "mpi"),
        ("β = rr_new / rr;  p = r + βp  (OpenMP)", "omp"),
        ("it < maxit and (tol = 0 or ‖r‖ > tol‖b‖) ?", "dec"),
        ("Barrier → read RAPL, temperature, throttle counters → stop timer", "meas"),
        ("Verify ‖b − Ax‖, ‖x − 1‖∞; rank 0 writes one result line", "io"),
    ]
    col = {"io": "#eeeeee", "proc": "white", "meas": "#fde8cc", "mpi": "#dbe8f8", "omp": "#d6f0e5", "dec": "#fff4cc"}
    fig, ax = plt.subplots(figsize=(6.6, 8.6))
    n = len(steps); ax.set_xlim(0, 10.8); ax.set_ylim(-0.4, n); ax.axis("off")
    ys = []
    for i, (txt, kind) in enumerate(steps):
        y = n - 1 - i
        ys.append(y)
        ax.add_patch(FancyBboxPatch((0.2, y + 0.12), 8.6, 0.62,
                                    boxstyle="round,pad=0.02,rounding_size=0.25" if kind == "dec" else "round,pad=0.02,rounding_size=0.06",
                                    fc=col[kind], ec="#555555", lw=0.7))
        ax.text(4.5, y + 0.43, txt, ha="center", va="center", fontsize=7.2)
        if i < n - 1:
            ax.annotate("", xy=(4.5, y - 0.26), xytext=(4.5, y + 0.12),
                        arrowprops=dict(arrowstyle="-|>", color="#555555", lw=0.8))
    # loop-back arrow from decision to halo exchange
    yd, yh = ys[9], ys[4]
    ax.annotate("", xy=(8.85, yh + 0.43), xytext=(8.85, yd + 0.43),
                arrowprops=dict(arrowstyle="-|>", color="#2a78d6", lw=1.0, connectionstyle="bar,fraction=-0.09"))
    ax.text(10.15, (yd + yh) / 2 + 0.4, "yes:\nnext\niteration", fontsize=7.4, color="#2a78d6", ha="center")
    ax.text(4.75, yd - 0.05, "no", fontsize=7.4, color="#555555")
    leg = [("MPI communication", "mpi"), ("OpenMP compute", "omp"), ("energy / timing", "meas")]
    for k, (lab, kind) in enumerate(leg):
        ax.add_patch(plt.Rectangle((0.2 + 3.3 * k, -0.35), 0.3, 0.22, fc=col[kind], ec="#555555", lw=0.6))
        ax.text(0.6 + 3.3 * k, -0.24, lab, va="center", fontsize=7.4)
    save(fig, "fig2_flowchart.png")


# ---------- Fig 3: energy vs time (RQ1) ----------
def fig_energy_vs_time(full):
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 5.2))
    for ax, m in zip(axes.flat, MATRICES):
        rows = list(full[m].values())
        for cls, c in CLASS_COL.items():
            pts = [r for r in rows if r["cls"] == cls]
            ax.scatter([float(r["time_med"]) for r in pts], [float(r["e_pkg_med"]) for r in pts],
                       s=14, color=c, edgecolor="white", linewidth=0.5, label=cls, zorder=3)
        fast = min(rows, key=lambda r: float(r["time_med"]))
        frug = min(rows, key=lambda r: float(r["e_pkg_med"]))
        for r, tag, dx in [(fast, "fastest", 6), (frug, "min energy", 6)]:
            ax.annotate(f"{tag}\n{r['cfg']}", (float(r["time_med"]), float(r["e_pkg_med"])),
                        xytext=(dx, 8), textcoords="offset points", fontsize=6.4, color="#111111",
                        arrowprops=dict(arrowstyle="-", color="#777777", lw=0.5))
        ax.set_title(m, fontsize=9, loc="left")
        ax.set_xlabel("solve time (s)", fontsize=7.5); ax.set_ylabel("package energy (J)", fontsize=7.5)
        ax.tick_params(labelsize=7)
        style(ax, "both")
    ax = axes.flat[5]; ax.axis("off")
    ax.legend(handles=[plt.Line2D([], [], marker="o", ls="", color=c, label=k) for k, c in CLASS_COL.items()],
              loc="center", frameon=False, fontsize=8, title="core-type class", title_fontsize=8)
    fig.suptitle("Energy vs. time for all 51 configurations (1000 CG iterations, median of 3)", fontsize=9.5, x=0.02, ha="left")
    fig.tight_layout()
    save(fig, "fig3_energy_vs_time.png")


# ---------- Fig 4: P vs E energy relative to P4 (RQ2) ----------
def fig_core_type(full):
    cfgs = [("E4 1x4", "4 E-cores, one module"), ("E4s 1x4", "4 E-cores, two modules"), ("E8 1x8", "8 E-cores"),
            ("P8ht 1x8", "4 P-cores + HT"), ("A16 1x16", "all 16 threads"), ("A12 12x1", "12 cores, MPI-only")]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    w = 0.13
    for k, (cfg, lab) in enumerate(cfgs):
        xs, ys = [], []
        for i, m in enumerate(MATRICES):
            ref = float(full[m]["P4 1x4"]["e_pkg_med"])
            xs.append(i + (k - 2.5) * w); ys.append(float(full[m][cfg]["e_pkg_med"]) / ref)
        ax.bar(xs, ys, width=w - 0.015, color=SER[k], label=f"{cfg} ({lab})", zorder=3)
    ax.axhline(1.0, color="#111111", lw=0.8, zorder=4)
    ax.text(4.62, 1.02, "P4 1×4 = 1.0", fontsize=7, ha="right")
    ax.set_xticks(range(len(MATRICES)), MATRICES)
    ax.set_ylabel("package energy relative to\n4 P-cores (P4 1×4)")
    ax.legend(frameon=False, fontsize=7, ncol=2, loc="upper left", bbox_to_anchor=(0, -0.12))
    style(ax)
    save(fig, "fig4_core_type_energy.png")


# ---------- Fig 5: MPI-only vs OpenMP-only energy (spin test) ----------
def fig_mpi_vs_omp(spin):
    m = "thermal2"
    groups = [("P4 (4 P-cores)", {"MPI-only": "P4 4x1", "OpenMP-only": "P4 1x4", "OpenMP-only, forced spin": "P4-ompactive 1x4"}),
              ("M8 (4P + 4E)", {"MPI-only": "M8 8x1", "MPI-only + yield": "M8-yield 8x1", "OpenMP-only": "M8 1x8",
                                "OpenMP-only, forced spin": "M8-ompactive 1x8"}),
              ("A12 (4P + 8E)", {"MPI-only": "A12 12x1", "MPI-only + yield": "A12-yield 12x1", "OpenMP-only": "A12 1x12",
                                 "OpenMP-only, forced spin": "A12-ompactive 1x12"})]
    series = ["MPI-only", "MPI-only + yield", "OpenMP-only", "OpenMP-only, forced spin"]
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    w = 0.2
    for k, s in enumerate(series):
        xs, ys = [], []
        for i, (_, g) in enumerate(groups):
            if s in g:
                xs.append(i + (k - 1.5) * w); ys.append(float(spin[m][g[s]]["e_pkg_med"]))
        ax.bar(xs, ys, width=w - 0.02, color=SER[k], label=s, zorder=3)
    ax.set_xticks(range(len(groups)), [g for g, _ in groups])
    ax.set_ylabel("package energy (J), thermal2")
    ax.legend(frameon=False, fontsize=7.5, ncol=2, loc="upper left", bbox_to_anchor=(0, -0.1))
    style(ax)
    save(fig, "fig5_mpi_vs_openmp_energy.png")


# ---------- Fig 6: perf counters ----------
def fig_perf():
    rows = {}
    for line in open(os.path.join(ROOT, "results", "perf_summary.md")):
        x = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(x) == 10 and re.match(r"^[A-Z]\w*-", x[0]):
            rows[x[0]] = x
    labels = [("P4", "P4 (4P)"), ("M8", "M8 (4P+4E)"), ("A12", "A12 (4P+8E)")]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7))
    for ax, col, ttl in [(axes[0], 3, "P-core instructions (billions)"), (axes[1], 6, "P-core cycles spent in PAUSE (%)")]:
        for k, (suf, name) in enumerate([("mpi", "MPI-only"), ("omp", "OpenMP-only")]):
            xs = [i + (k - 0.5) * 0.36 for i in range(len(labels))]
            ys = [float(rows[f"{p}-{suf}"][col]) for p, _ in labels]
            ax.bar(xs, ys, width=0.34, color=SER[0] if k == 0 else SER[2], label=name, zorder=3)
            for xx, yy in zip(xs, ys):
                ax.text(xx, yy, f"{yy:.0f}" if col == 3 else f"{yy:.1f}", ha="center", va="bottom", fontsize=6.5)
        ax.set_xticks(range(len(labels)), [n for _, n in labels], fontsize=7.5)
        ax.set_title(ttl, fontsize=8.5, loc="left")
        style(ax)
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.tight_layout()
    save(fig, "fig6_perf_counters.png")


if __name__ == "__main__":
    full, spin = load_summary("full"), load_summary("spin")
    fig_architecture(); fig_flowchart(); fig_energy_vs_time(full)
    fig_core_type(full); fig_mpi_vs_omp(spin); fig_perf()
