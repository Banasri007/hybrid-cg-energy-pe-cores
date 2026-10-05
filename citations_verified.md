# Citation verification (2026-10-03)

Source of truth: Crossref API metadata (publisher-deposited) + arXiv API. "Claim" = what the proposal says the paper shows; claims marked ⚠ were NOT checked against full text.

## Corrections — proposal is wrong

| Proposal says | Actually |
|---|---|
| **Kuhn et al.**, JPDC | **M. Wlotzka, V. Heuveline**, "Energy-efficient multigrid smoothers and grid transfer operators on multi-core and GPU clusters," *J. Parallel Distrib. Comput.*, vol. 100, pp. 181–192, Feb. 2017, doi:10.1016/j.jpdc.2016.05.006. Full text paywalled — "hybrid best for energy, not fastest" claim ⚠ still needs reading via MIT Manipal library access. |
| **Onodera** (JJIAM, Springer, 2025) | **K. Nakajima**, "Optimization of communication-computation overlapping in parallel multigrid methods by process/thread allocation," *Japan J. Ind. Appl. Math.*, vol. 42, no. 3, pp. 1029–1062, Sep. 2025, doi:10.1007/s13160-025-00732-3. ⚠ Confirm 12×4/6×8/3×16, A64FX, 8–21% claims match this paper. |
| **Wu & Taylor** (energy, NPB BT / LBM / GTC) | **C. Lively, X. Wu, V. Taylor, S. Moore, H.-C. Chang, K. W. Cameron**, "Energy and performance characteristics of different parallel implementations of scientific applications on multicore systems," *Int. J. High Perform. Comput. Appl.*, vol. 25, no. 3, pp. 342–350, Aug. 2011, doi:10.1177/1094342011414749. ⚠ claims |
| **E-Mapper**, arXiv:2406.18980 | arXiv title confirmed: "E-Mapper: Energy-Efficient Resource Allocation for Traditional Operating Systems on Heterogeneous Processors," T. Smejkal, R. Khasanov, J. Castrillon, H. Härtig, Jun. 2024. Same authors published **"HARP: Energy-Aware and Adaptive Management of Heterogeneous Processors,"** *Middleware '25*, pp. 270–284, Dec. 2025, doi:10.1145/3721462.3770774 — likely the peer-reviewed successor; prefer citing it if it covers the same results. ⚠ |
| **Raffin & Trystram (IEEE TPDS 2024)** | Year/vol: *IEEE Trans. Parallel Distrib. Syst.*, vol. 36, no. 1, pp. 96–107, **Jan. 2025**, doi:10.1109/TPDS.2024.3492336. Title: "Dissecting the Software-Based Measurement of CPU Energy Consumption: A Comparative Analysis." |
| **MDPI Information 14(4):248 "survey"** | **A. Lastovetsky, R. R. Manumachu**, "Energy-Efficient Parallel Computing: Challenges to Scaling," *Information*, vol. 14, no. 4, p. 248, Apr. 2023, doi:10.3390/info14040248. It's a position/challenges paper, not a survey — reword. ⚠ 37–84% claim |
| **Milyukova (Keldysh 2023; MMCS 2024)** | Keldysh preprint confirmed: O. Yu. Milyukova, "MPI+OpenMP methods for implementing the conjugate gradient method with the IC(0) preconditioner based on the use of grid node reordering," *Keldysh Inst. Preprints*, no. 35, 2023, doi:10.20948/prepr-2023-35. **No 2024 MMCS paper found** — closest is MMCS vol. 14, no. 3, pp. 367–380, 2022 (factorized implicit preconditioners, doi:10.1134/S2070048222030103). Drop the "2024" claim or find it. |

## Confirmed metadata (claims ⚠ unless noted)

- L. Oliker, X. Li, P. Husbands, R. Biswas, "Effects of ordering strategies and programming paradigms on sparse matrix computations," *SIAM Rev.*, vol. 44, no. 3, pp. 373–393, 2002, doi:10.1137/S00361445003820. (SIAM, not IEEE.)
- G. Schubert, H. Fehske, G. Hager, G. Wellein, "Hybrid-parallel sparse matrix-vector multiplication with explicit communication overlap on current multicore-based systems," *Parallel Process. Lett.*, vol. 21, no. 3, pp. 339–358, 2011, doi:10.1142/S0129626411000254 (= arXiv:1106.5908). Cite this, not the arXiv.
- R. Iakymchuk, M. Barreda Vayá, S. Graillat, J. I. Aliaga, E. S. Quintana-Ortí, "Reproducibility of parallel preconditioned conjugate gradient in hybrid programming environments," *Int. J. High Perform. Comput. Appl.*, vol. 34, no. 5, pp. 502–518, 2020, doi:10.1177/1094342020932650.
- D. Li, B. R. de Supinski, M. Schulz, K. Cameron, D. S. Nikolopoulos, "Hybrid MPI/OpenMP power-aware computing," *Proc. IEEE IPDPS*, 2010, pp. 1–12, doi:10.1109/IPDPS.2010.5470463.
- M. Siahatgar, G. von Voigt, "Evaluation of sparse linear algebra operations in Trilinos," *Proc. ECCOMAS Congress 2016*, pp. 1381–1391, doi:10.7712/100016.1893.11500. (Conference proceedings, not a journal.)
- A. Krzywaniak, J. Proficz, P. Czarnul — two candidates; ⚠ check which has the 16–29% / 38–86% numbers:
  - "Analyzing energy/performance trade-offs with power capping for parallel applications on modern multi and many core processors," *FedCSIS 2018*, ACSIS vol. 15, pp. 339–346, doi:10.15439/2018F177.
  - "Extended investigation of performance-energy trade-offs under power capping in HPC environments," *HPCS 2019*, pp. 440–447, doi:10.1109/HPCS48598.2019.9188149.
- V. Ostapenco, L. Lefèvre, A.-C. Orgerie, B. Fichel, "Exploring RAPL as a power capping leverage for power-constrained infrastructures," *ICA3PP 2024*, LNCS, Springer, 2025, pp. 323–333, doi:10.1007/978-981-96-1542-1_19. ⚠ The "MAPE <2% vs external meter" claim may instead come from M. Jay, V. Ostapenco, et al., "An experimental comparison of software-based power meters: focus on CPU and GPU," *CCGrid 2023*, pp. 106–118, doi:10.1109/CCGRID57682.2023.00020 — check.
- D. Żytko, M. Badurowicz, "Analysis of performance and energy efficiency of processors with hybrid architecture," *J. Comput. Sci. Inst.*, vol. 34, pp. 54–59, Mar. 2025, doi:10.35784/jcsi.6690. ✓ matches proposal.
- N. Velugoti, J. Manzano, N. Tallent, K. Hale, "Effects of hybrid CPU and cache architectures on parallel HPC and cloud applications," arXiv:2608.23165 [cs.DC], Aug. 2026. **Full text read**: OpenMP only (miniVite, NPB SP/BT/LU/FT, CRONO, PARSEC), Alder Lake 12th gen, runtime only — **no MPI, no energy**. Gap survives.
- T. A. Davis, Y. Hu, "The University of Florida sparse matrix collection," *ACM Trans. Math. Softw.*, vol. 38, no. 1, pp. 1–25, 2011, doi:10.1145/2049662.2049663.
- Brown & Neri (LPC 2022), Intel hybrid whitepaper — not in Crossref (talk / grey literature); verify URLs manually.

## Recency (last 5 yrs = 2021+)
In window: Nakajima 2025, Ostapenco 2025, Raffin & Trystram 2025, Lastovetsky 2023, Velugoti 2026, Żytko 2025, E-Mapper 2024 / HARP 2025, Milyukova 2023 (and 2022 MMCS). = 8–9. Iakymchuk 2020 just misses.
