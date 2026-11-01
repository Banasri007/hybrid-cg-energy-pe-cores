#!/usr/bin/env python3
"""Renumber citations in order of first appearance (IEEE) and append the reference list.

    python3 report/build_report.py      # report_src.md -> PCAP_Final_Report.md

In report_src.md, citations are written with fixed source ids [1]..[24] (see REFS);
the formatting comment block at the top is skipped when determining citation order.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

REFS = {
    1: 'Intel Corporation, "Optimizing software for x86 hybrid architecture," white paper, https://www.intel.com/content/www/us/en/content-details/818776/optimizing-software-for-x86-hybrid-architecture.html (accessed October 28, 2026).',
    2: 'L. Brown and R. Neri, "Bringing energy-aware scheduling to x86," presented at the Linux Plumbers Conf., Real-time and Scheduling Microconference, Dublin, Ireland, Sep. 13, 2022, https://lpc.events/event/16/contributions/1275/ (accessed October 28, 2026).',
    3: 'M. R. Hestenes and E. Stiefel, "Methods of conjugate gradients for solving linear systems," *J. Res. Natl. Bur. Stand.*, vol. 49, no. 6, pp. 409–436, 1952, doi: 10.6028/jres.049.044.',
    4: 'D. Żytko and M. Badurowicz, "Analysis of performance and energy efficiency of processors with hybrid architecture," *J. Comput. Sci. Inst.*, vol. 34, pp. 54–59, Mar. 2025, doi: 10.35784/jcsi.6690.',
    5: 'C. Lively, X. Wu, V. Taylor, S. Moore, H.-C. Chang, and K. W. Cameron, "Energy and performance characteristics of different parallel implementations of scientific applications on multicore systems," *Int. J. High Perform. Comput. Appl.*, vol. 25, no. 3, pp. 342–350, Aug. 2011, doi: 10.1177/1094342011414749.',
    6: 'M. Wlotzka and V. Heuveline, "Energy-efficient multigrid smoothers and grid transfer operators on multi-core and GPU clusters," *J. Parallel Distrib. Comput.*, vol. 100, pp. 181–192, Feb. 2017, doi: 10.1016/j.jpdc.2016.05.006.',
    7: 'L. Oliker, X. Li, P. Husbands, and R. Biswas, "Effects of ordering strategies and programming paradigms on sparse matrix computations," *SIAM Rev.*, vol. 44, no. 3, pp. 373–393, 2002, doi: 10.1137/S00361445003820.',
    8: 'G. Schubert, H. Fehske, G. Hager, and G. Wellein, "Hybrid-parallel sparse matrix-vector multiplication with explicit communication overlap on current multicore-based systems," *Parallel Process. Lett.*, vol. 21, no. 3, pp. 339–358, Sep. 2011, doi: 10.1142/S0129626411000254.',
    9: 'K. Nakajima, "Optimization of communication-computation overlapping in parallel multigrid methods by process/thread allocation," *Japan J. Ind. Appl. Math.*, vol. 42, no. 3, pp. 1029–1062, Sep. 2025, doi: 10.1007/s13160-025-00732-3.',
    10: 'N. Velugoti, J. Manzano, N. Tallent, and K. Hale, "Effects of hybrid CPU and cache architectures on parallel HPC and cloud applications," arXiv:2608.23165 [cs.DC], Aug. 2026, doi: 10.48550/arXiv.2608.23165.',
    11: 'T. Smejkal, R. Khasanov, J. Castrillon, and H. Härtig, "E-Mapper: Energy-efficient resource allocation for traditional operating systems on heterogeneous processors," arXiv:2406.18980, Jun. 2024.',
    12: 'T. Smejkal, R. Khasanov, J. Castrillon, and H. Härtig, "HARP: Energy-aware and adaptive management of heterogeneous processors," in *Proc. 26th Int. Middleware Conf. (Middleware \'25)*, Nashville, TN, USA, 2025, pp. 270–284, doi: 10.1145/3721462.3770774.',
    13: 'D. Li, B. R. de Supinski, M. Schulz, K. Cameron, and D. S. Nikolopoulos, "Hybrid MPI/OpenMP power-aware computing," in *Proc. IEEE Int. Symp. Parallel Distrib. Process. (IPDPS)*, Atlanta, GA, USA, 2010, pp. 1–12, doi: 10.1109/IPDPS.2010.5470463.',
    14: 'R. Iakymchuk, M. Barreda Vayá, S. Graillat, J. I. Aliaga, and E. S. Quintana-Ortí, "Reproducibility of parallel preconditioned conjugate gradient in hybrid programming environments," *Int. J. High Perform. Comput. Appl.*, vol. 34, no. 5, pp. 502–518, 2020, doi: 10.1177/1094342020932650.',
    15: 'O. Yu. Milyukova, "MPI+OpenMP methods for implementing the conjugate gradient method with the IC(0) preconditioner based on the use of grid node reordering," *Keldysh Inst. Preprints*, no. 35, pp. 1–32, 2023, doi: 10.20948/prepr-2023-35.',
    17: 'A. Krzywaniak, J. Proficz, and P. Czarnul, "Analyzing energy/performance trade-offs with power capping for parallel applications on modern multi and many core processors," in *Proc. Federated Conf. Comput. Sci. Inf. Syst. (FedCSIS)*, Poznań, Poland, 2018, Ann. Comput. Sci. Inf. Syst., vol. 15, pp. 339–346, doi: 10.15439/2018F177.',
    18: 'V. Ostapenco, L. Lefèvre, A.-C. Orgerie, and B. Fichel, "Exploring RAPL as a power capping leverage for power-constrained infrastructures," in *Algorithms and Architectures for Parallel Processing (ICA3PP 2024)*, Lecture Notes in Computer Science. Singapore: Springer, 2025, pp. 323–333, doi: 10.1007/978-981-96-1542-1_19.',
    19: 'M. Jay, V. Ostapenco, L. Lefèvre, D. Trystram, A.-C. Orgerie, and B. Fichel, "An experimental comparison of software-based power meters: Focus on CPU and GPU," in *Proc. IEEE/ACM 23rd Int. Symp. Cluster, Cloud and Internet Computing (CCGrid)*, Bangalore, India, 2023, pp. 106–118, doi: 10.1109/CCGrid57682.2023.00020.',
    20: 'G. Raffin and D. Trystram, "Dissecting the software-based measurement of CPU energy consumption: A comparative analysis," *IEEE Trans. Parallel Distrib. Syst.*, vol. 36, no. 1, pp. 96–107, Jan. 2025, doi: 10.1109/TPDS.2024.3492336.',
    21: 'A. Lastovetsky and R. R. Manumachu, "Energy-efficient parallel computing: Challenges to scaling," *Information*, vol. 14, no. 4, p. 248, Apr. 2023, doi: 10.3390/info14040248.',
    22: 'T. A. Davis and Y. Hu, "The University of Florida sparse matrix collection," *ACM Trans. Math. Softw.*, vol. 38, no. 1, pp. 1–25, Nov. 2011, doi: 10.1145/2049662.2049663.',
    23: 'E. Cuthill and J. McKee, "Reducing the bandwidth of sparse symmetric matrices," in *Proc. 24th ACM National Conf.*, 1969, pp. 157–172, doi: 10.1145/800195.805928.',
    24: 'A. George and J. W. H. Liu, *Computer Solution of Large Sparse Positive Definite Systems*. Englewood Cliffs, NJ, USA: Prentice-Hall, 1981.',
}

CITE = re.compile(r"\[(\d{1,2})\]")


def main():
    src = open(os.path.join(HERE, "report_src.md"), encoding="utf-8").read()
    head, sep, body = src.partition("BEGIN REPORT")
    body_start = src.index("-->", len(head)) + 3 if sep else 0
    text = src[body_start:]
    # citations are only looked for outside fenced code blocks (code has x[0] etc.)
    parts = text.split("```")
    prose = "".join(parts[0::2])
    order = []
    for m in CITE.finditer(prose):
        k = int(m.group(1))
        if k in REFS and k not in order:
            order.append(k)
    unknown = sorted({int(m.group(1)) for m in CITE.finditer(prose)} - set(REFS))
    assert not unknown, f"citations without a reference entry: {unknown}"
    new = {old: i + 1 for i, old in enumerate(order)}
    sub = lambda seg: CITE.sub(lambda m: f"[{new[int(m.group(1))]}]" if int(m.group(1)) in new else m.group(0), seg)
    text = "```".join(sub(seg) if i % 2 == 0 else seg for i, seg in enumerate(parts))
    refs = "\n\n".join(f"[{new[k]}] {REFS[k]}" for k in order)
    text = text.replace("{{REFERENCES}}", refs)
    unused = [k for k in REFS if k not in new]
    out = src[:body_start] + text
    open(os.path.join(HERE, "PCAP_Final_Report.md"), "w", encoding="utf-8").write(out)
    print(f"{len(order)} references cited; unused source ids: {unused}")
    left = re.findall(r"\[\[FILL[^\]]*\]\]", out)
    print(f"{len(left)} [[FILL]] placeholders remaining")


if __name__ == "__main__":
    main()
