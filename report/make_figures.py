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
    """Experiments A+B (solve to tolerance) when available, else the fixed-iteration survey."""
    a, b = (os.path.join(ROOT, "results", f"{n}_summary.csv") for n in ("equalcount", "mixed"))
    tol_mode = os.path.exists(a) and os.path.exists(b)
    if tol_mode:
        ea, eb = load_summary("equalcount"), load_summary("mixed")
        full = {m: {**ea.get(m, {}), **eb.get(m, {})} for m in MATRICES}
        title = "Energy-to-solution vs. time-to-solution, Experiments A and B (tolerance 1e-8, mean of 3)"
        tk, ek = "time_mean", "e_mean"
    else:
        title = "Energy vs. time for all 51 configurations (1000 CG iterations, median of 3)"
        tk, ek = "time_med", "e_pkg_med"
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 5.2))
    for ax, m in zip(axes.flat, MATRICES):
        rows = list(full[m].values())
        for cls, c in CLASS_COL.items():
            pts = [r for r in rows if r["cls"] == cls]
            ax.scatter([float(r[tk]) for r in pts], [float(r[ek]) for r in pts],
                       s=14, color=c, edgecolor="white", linewidth=0.5, label=cls, zorder=3)
        fast = min(rows, key=lambda r: float(r[tk]))
        frug = min(rows, key=lambda r: float(r[ek]))
        for r, tag, dx in [(fast, "fastest", 6), (frug, "min energy", 6)]:
            ax.annotate(f"{tag}\n{r['cfg']}", (float(r[tk]), float(r[ek])),
                        xytext=(dx, 8), textcoords="offset points", fontsize=6.4, color="#111111",
                        arrowprops=dict(arrowstyle="-", color="#777777", lw=0.5))
        ax.set_title(m, fontsize=9, loc="left")
        ax.set_xlabel("solve time (s)", fontsize=7.5); ax.set_ylabel("package energy (J)", fontsize=7.5)
        ax.tick_params(labelsize=7)
        style(ax, "both")
    ax = axes.flat[5]; ax.axis("off")
    ax.legend(handles=[plt.Line2D([], [], marker="o", ls="", color=c, label=k) for k, c in CLASS_COL.items()],
              loc="center", frameon=False, fontsize=8, title="core-type class", title_fontsize=8)
    fig.suptitle(title, fontsize=9.5, x=0.02, ha="left")
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
        ax.set_ylabel("instructions (×10⁹)" if col == 3 else "share of P-core cycles (%)", fontsize=7.5)
        style(ax)
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.tight_layout()
    save(fig, "fig6_perf_counters.png")


# ---------- design: CPU topology and process/thread mapping ----------
def fig_topology():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.set_xlim(0, 16); ax.set_ylim(0, 8); ax.axis("off")
    # P-cores: 4 cores x 2 HT threads
    for c in range(4):
        x = 0.3 + c * 1.85
        ax.add_patch(FancyBboxPatch((x, 4.2), 1.65, 2.6, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc="#dbe8f8", ec=SER[0], lw=0.9))
        ax.text(x + 0.82, 6.45, f"P-core {c}", ha="center", fontsize=7.5, weight="bold")
        for h in range(2):
            cpu = 2 * c + h
            ax.add_patch(plt.Rectangle((x + 0.15 + h * 0.72, 5.25), 0.62, 0.75, fc="white", ec="#555555", lw=0.6))
            ax.text(x + 0.46 + h * 0.72, 5.62, f"{cpu}", ha="center", va="center", fontsize=7.5)
        ax.text(x + 0.82, 4.55, "L2 1.25 MB", ha="center", fontsize=6.5)
    ax.text(3.9, 7.25, "4 P-cores (HT): CPUs 0–7, ≤ 4.7 GHz", ha="center", fontsize=8)
    # E-modules
    for mdl in range(2):
        x = 7.9 + mdl * 4.0
        ax.add_patch(FancyBboxPatch((x, 4.2), 3.8, 2.6, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc="#fde3d6", ec=SER[1], lw=0.9))
        ax.text(x + 1.9, 6.45, f"E-module {mdl}", ha="center", fontsize=7.5, weight="bold")
        for k in range(4):
            cpu = 8 + 4 * mdl + k
            ax.add_patch(plt.Rectangle((x + 0.2 + k * 0.88, 5.25), 0.75, 0.75, fc="white", ec="#555555", lw=0.6))
            ax.text(x + 0.57 + k * 0.88, 5.62, f"{cpu}", ha="center", va="center", fontsize=7.5)
        ax.text(x + 1.9, 4.55, "shared L2 2 MB", ha="center", fontsize=6.5)
    ax.text(11.85, 7.25, "8 E-cores (no HT): CPUs 8–15, ≤ 3.5 GHz", ha="center", fontsize=8)
    ax.add_patch(plt.Rectangle((0.3, 3.2), 15.4, 0.6, fc="#eeeeee", ec="#555555", lw=0.6))
    ax.text(8.0, 3.5, "ring interconnect  ·  shared L3 18 MB  ·  memory controller (RAPL: package-0, core, uncore, psys)",
            ha="center", va="center", fontsize=7.5)
    rows = [("P4", "0, 2, 4, 6", "one thread per P-core"), ("E4 (packed)", "8, 9, 10, 11", "one E-module"),
            ("E4s (spread)", "8, 9, 12, 13", "two per E-module"), ("M8", "0, 2, 4, 6, 8–11", "4P + 4E, mixed"),
            ("A16", "0–15", "all hardware threads")]
    ax.text(0.3, 2.55, "Example CPU sets (rank r with T threads gets entries r·T … r·T+T−1):", fontsize=7.5, weight="bold")
    for i, (a, b, c) in enumerate(rows):
        y = 2.0 - i * 0.42
        ax.text(0.5, y, a, fontsize=7.3); ax.text(3.0, y, b, fontsize=7.3); ax.text(6.2, y, c, fontsize=7.3, color="#444444")
    save(fig, "fig_topology_mapping.png")


# ---------- design: task decomposition and communication pattern ----------
def fig_decomposition():
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.set_xlim(0, 16); ax.set_ylim(0, 8.4); ax.axis("off")
    cols = [SER[0], SER[2], SER[3], SER[1]]
    ax.add_patch(plt.Rectangle((0.4, 0.6), 5.2, 7.2, fc="white", ec="#333333", lw=0.8))
    import numpy as _np
    rng = _np.random.default_rng(3)
    for r in range(4):
        y0 = 0.6 + (3 - r) * 1.8
        ax.add_patch(plt.Rectangle((0.4, y0), 5.2, 1.8, fc=cols[r], alpha=0.18, ec="none"))
        ax.text(5.8, y0 + 0.9, f"rank {r}", va="center", fontsize=7.5, color="#111111")
        # band of nonzeros around the diagonal (after RCM)
        for _ in range(55):
            yy = y0 + rng.uniform(0.05, 1.75)
            d = (7.8 - yy) / 7.2 * 5.2 + 0.4
            xx = d + rng.normal(0, 0.35)
            if 0.45 < xx < 5.55:
                inside = (0.4 + (r) * 1.3) <= xx <= (0.4 + (r + 1) * 1.3)
                ax.plot(xx, yy, "s", ms=1.6, color="#333333" if inside else "#d43c3c")
    ax.text(3.0, 8.05, "A after RCM: row blocks with ≈ equal nonzeros", ha="center", fontsize=7.5)
    ax.text(3.0, 0.2, "black = owned column · red = halo (ghost) column", ha="center", fontsize=6.8)
    # communication side
    xs = [8.2, 10.3, 12.4, 14.5]
    for r, x in enumerate(xs):
        ax.add_patch(FancyBboxPatch((x - 0.75, 5.7), 1.5, 1.2, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=cols[r], alpha=0.35, ec="#333333", lw=0.7))
        ax.text(x, 6.55, f"rank {r}", ha="center", fontsize=7.5, weight="bold")
        ax.text(x, 6.05, "T OpenMP\nthreads", ha="center", fontsize=6.3, linespacing=1.1)
    for a, b in zip(xs[:-1], xs[1:]):
        ax.annotate("", xy=(b - 0.78, 6.3), xytext=(a + 0.78, 6.3), arrowprops=dict(arrowstyle="<|-|>", color="#d43c3c", lw=1.0))
    ax.text(11.35, 7.35, "(1) halo exchange of p (Isend/Irecv, neighbours only)", ha="center", fontsize=7.3, color="#d43c3c")
    ax.add_patch(FancyBboxPatch((7.4, 3.3), 7.9, 0.9, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#dbe8f8", ec=SER[0], lw=0.8))
    ax.text(11.35, 3.75, "(2)(3) MPI_Allreduce: p·Ap → α  and  r·r → convergence test, β", ha="center", va="center", fontsize=7.3)
    for x in xs:
        ax.annotate("", xy=(x, 4.25), xytext=(x, 5.65), arrowprops=dict(arrowstyle="<|-|>", color=SER[0], lw=0.8))
    ax.text(11.35, 2.4, "per iteration: 1 halo exchange + 1 SpMV (threaded)\n"
                        "+ 2 Allreduce + 3 vector updates (threaded)", ha="center", fontsize=7.3, linespacing=1.4)
    save(fig, "fig_decomposition_comm.png")


# ---------- Experiment A: equal-core-count P vs E (needs results/equalcount_summary.csv) ----------
def fig_equalcount():
    path = os.path.join(ROOT, "results", "equalcount_summary.csv")
    if not os.path.exists(path):
        print("skip fig_equalcount (run revision_runs.sh first)")
        return
    eq = load_summary("equalcount")
    fam = [("P-cores", ["P1", "P2", "P3", "P4"], SER[0], "o"),
           ("E-cores, packed in one module", ["E1", "E2", "E3", "E4"], SER[1], "s"),
           ("E-cores, spread over two modules", ["E1", "E2s", "E3s", "E4s"], SER[2], "^")]
    fig, axes = plt.subplots(2, 5, figsize=(7.4, 3.9), sharex=True)
    for j, m in enumerate(MATRICES):
        for row, (key, sd, lab) in enumerate([("e_mean", "e_sd", "energy-to-solution (J)"), ("time_mean", "time_sd", "time-to-solution (s)")]):
            ax = axes[row, j]
            for name, labels, c, mk in fam:
                pts = [(k + 1, eq[m].get(f"{l} 1x{k+1}")) for k, l in enumerate(labels)]
                pts = [(x, r) for x, r in pts if r]
                ax.errorbar([x for x, _ in pts], [float(r[key]) for _, r in pts], yerr=[float(r[sd]) for _, r in pts],
                            color=c, marker=mk, ms=3.5, lw=1.2, capsize=2, label=name)
            ax.set_xticks([1, 2, 3, 4]); ax.tick_params(labelsize=6.5)
            if j == 0: ax.set_ylabel(lab, fontsize=7)
            if row == 0: ax.set_title(m, fontsize=8, loc="left")
            if row == 1: ax.set_xlabel("physical cores", fontsize=7)
            style(ax, "both")
    axes[0, 0].legend(frameon=False, fontsize=6.5, loc="upper left", bbox_to_anchor=(0, -1.55), ncol=3)
    fig.tight_layout()
    save(fig, "fig_equalcount.png")


if __name__ == "__main__":
    full, spin = load_summary("full"), load_summary("spin")
    fig_architecture(); fig_flowchart(); fig_energy_vs_time(full)
    fig_core_type(full); fig_mpi_vs_omp(spin); fig_perf()
    fig_topology(); fig_decomposition(); fig_equalcount()
