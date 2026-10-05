/* Hybrid MPI+OpenMP Conjugate Gradient (unpreconditioned).
 *
 * Usage: mpirun -np P cg_hybrid <matrix.mtx | poisson:M> [tol=1e-8] [maxit=10000]
 *   tol = 0  -> fixed-iteration mode: run exactly maxit iterations.
 *
 * MPI:    contiguous nnz-balanced row blocks; halo exchange of p for
 *         off-block columns (Isend/Irecv with neighbours only);
 *         2 MPI_Allreduce per iteration: p.Ap (alpha) and r.r (residual + beta).
 * OpenMP: threaded SpMV (schedule from OMP_SCHEDULE, e.g. "static" or
 *         "dynamic,64") and fused vector updates/reductions (static).
 *
 * RHS is b = A*1 (exact solution ones), x0 = 0. Only the iteration loop is
 * timed and energy-metered: rank 0 snapshots RAPL (package/core/uncore/psys),
 * package temperature and thermal-throttle counters right after the start
 * barrier and right after an end barrier. Energy fields are -1 if RAPL is not
 * readable. Output: one key=value line from rank 0. */
#define _GNU_SOURCE
#include "csr.h"
#include "rapl.h"
#include <math.h>
#include <mpi.h>
#include <omp.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int nloc, nghost;
    int nrecv, nsend;           /* neighbour counts */
    int *recv_rank, *recv_off, *recv_cnt;   /* into p[nloc + off] */
    int *send_rank, *send_off, *send_cnt;   /* into sendbuf */
    int *send_idx;              /* local row indices to pack, total = sum send_cnt */
    double *sendbuf;
    MPI_Request *req;
} halo_t;

static int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}

/* Find off-block columns, build send/recv lists, renumber A's columns to
 * local indexing: [0,nloc) owned rows, [nloc, nloc+nghost) ghosts. */
static void halo_setup(csr_t *A, const int *bounds, int rank, int size, halo_t *h) {
    int r0 = bounds[rank], r1 = bounds[rank + 1];
    h->nloc = A->n;

    long ng = 0;
    for (long k = 0; k < A->nnz; k++)
        if (A->col[k] < r0 || A->col[k] >= r1) ng++;
    int *ghost = malloc((ng ? ng : 1) * sizeof(int));
    ng = 0;
    for (long k = 0; k < A->nnz; k++)
        if (A->col[k] < r0 || A->col[k] >= r1) ghost[ng++] = A->col[k];
    qsort(ghost, ng, sizeof(int), cmp_int);
    long u = 0;
    for (long k = 0; k < ng; k++)
        if (u == 0 || ghost[k] != ghost[u - 1]) ghost[u++] = ghost[k];
    h->nghost = (int)u;

    /* ghosts are sorted, and ownership is contiguous, so they group by owner */
    int *rcnt = calloc(size, sizeof(int)), *scnt = malloc(size * sizeof(int));
    int owner = 0;
    for (int g = 0; g < h->nghost; g++) {
        while (ghost[g] >= bounds[owner + 1]) owner++;
        rcnt[owner]++;
    }
    MPI_Alltoall(rcnt, 1, MPI_INT, scnt, 1, MPI_INT, MPI_COMM_WORLD);

    int *rdis = malloc(size * sizeof(int)), *sdis = malloc(size * sizeof(int));
    int stot = 0, rtot = 0;
    for (int q = 0; q < size; q++) {
        rdis[q] = rtot; rtot += rcnt[q];
        sdis[q] = stot; stot += scnt[q];
    }
    h->send_idx = malloc((stot ? stot : 1) * sizeof(int));
    MPI_Alltoallv(ghost, rcnt, rdis, MPI_INT, h->send_idx, scnt, sdis, MPI_INT, MPI_COMM_WORLD);
    for (int k = 0; k < stot; k++) h->send_idx[k] -= r0;
    h->sendbuf = malloc((stot ? stot : 1) * sizeof(double));

    h->nrecv = h->nsend = 0;
    h->recv_rank = malloc(size * sizeof(int)); h->recv_off = malloc(size * sizeof(int));
    h->recv_cnt = malloc(size * sizeof(int));
    h->send_rank = malloc(size * sizeof(int)); h->send_off = malloc(size * sizeof(int));
    h->send_cnt = malloc(size * sizeof(int));
    for (int q = 0; q < size; q++) {
        if (rcnt[q]) {
            h->recv_rank[h->nrecv] = q; h->recv_off[h->nrecv] = rdis[q];
            h->recv_cnt[h->nrecv++] = rcnt[q];
        }
        if (scnt[q]) {
            h->send_rank[h->nsend] = q; h->send_off[h->nsend] = sdis[q];
            h->send_cnt[h->nsend++] = scnt[q];
        }
    }
    h->req = malloc((h->nrecv + h->nsend + 1) * sizeof(MPI_Request));

    /* renumber columns to local indexing */
    #pragma omp parallel for schedule(static)
    for (long k = 0; k < A->nnz; k++) {
        int c = A->col[k];
        if (c >= r0 && c < r1) A->col[k] = c - r0;
        else {
            int *pos = bsearch(&c, ghost, h->nghost, sizeof(int), cmp_int);
            A->col[k] = h->nloc + (int)(pos - ghost);
        }
    }
    free(ghost); free(rcnt); free(scnt); free(rdis); free(sdis);
}

/* fill p[nloc .. nloc+nghost) from neighbours */
static void halo_exchange(halo_t *h, double *p) {
    int nr = 0;
    for (int i = 0; i < h->nrecv; i++)
        MPI_Irecv(p + h->nloc + h->recv_off[i], h->recv_cnt[i], MPI_DOUBLE,
                  h->recv_rank[i], 0, MPI_COMM_WORLD, &h->req[nr++]);
    int stot = h->nsend ? h->send_off[h->nsend - 1] + h->send_cnt[h->nsend - 1] : 0;
    #pragma omp parallel for schedule(static)
    for (int k = 0; k < stot; k++) h->sendbuf[k] = p[h->send_idx[k]];
    for (int i = 0; i < h->nsend; i++)
        MPI_Isend(h->sendbuf + h->send_off[i], h->send_cnt[i], MPI_DOUBLE,
                  h->send_rank[i], 0, MPI_COMM_WORLD, &h->req[nr++]);
    MPI_Waitall(nr, h->req, MPI_STATUSES_IGNORE);
}

static void spmv(const csr_t *A, const double *x, double *y) {
    #pragma omp parallel for schedule(runtime)
    for (int i = 0; i < A->n; i++) {
        double s = 0.0;
        for (long k = A->rowptr[i]; k < A->rowptr[i + 1]; k++)
            s += A->val[k] * x[A->col[k]];
        y[i] = s;
    }
}

static double dot_all(int n, const double *a, const double *b, double *t_red) {
    double s = 0.0, g;
    #pragma omp parallel for schedule(static) reduction(+:s)
    for (int i = 0; i < n; i++) s += a[i] * b[i];
    double t = MPI_Wtime();
    MPI_Allreduce(&s, &g, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    *t_red += MPI_Wtime() - t;
    return g;
}

int main(int argc, char **argv) {
    int prov, rank, size;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &prov);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    if (prov < MPI_THREAD_FUNNELED) {
        if (!rank) fprintf(stderr, "MPI_THREAD_FUNNELED not supported\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    if (argc < 2) {
        if (!rank) fprintf(stderr, "usage: %s <matrix.mtx | poisson:M> [tol] [maxit]\n", argv[0]);
        MPI_Finalize();
        return 1;
    }
    const char *spec = argv[1];
    double tol = argc > 2 ? atof(argv[2]) : 1e-8;
    int maxit = argc > 3 ? atoi(argv[3]) : 10000;

    int err = rank == 0 ? csr_prepare(spec) : 0;
    MPI_Bcast(&err, 1, MPI_INT, 0, MPI_COMM_WORLD);
    if (err) MPI_Abort(MPI_COMM_WORLD, 1);

    csr_t A;
    int *bounds = malloc((size + 1) * sizeof(int)), nglob;
    if (csr_load_part(spec, size, rank, &A, bounds, &nglob)) MPI_Abort(MPI_COMM_WORLD, 1);
    long nnz_loc = A.nnz, nnz_glob;
    MPI_Allreduce(&nnz_loc, &nnz_glob, 1, MPI_LONG, MPI_SUM, MPI_COMM_WORLD);

    halo_t h;
    halo_setup(&A, bounds, rank, size, &h);
    int n = h.nloc, next = h.nloc + h.nghost;

    double *x = malloc(n * sizeof *x), *b = malloc(n * sizeof *b);
    double *r = malloc(n * sizeof *r), *Ap = malloc(n * sizeof *Ap);
    double *p = malloc((next ? next : 1) * sizeof *p);   /* owned + ghost entries */

    /* b = A*ones: ghosts of ones are ones, so no exchange needed */
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < next; i++) p[i] = 1.0;
    spmv(&A, p, b);
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < n; i++) { x[i] = 0.0; r[i] = b[i]; p[i] = b[i]; }

    double t_halo = 0.0, t_red = 0.0;
    double bnorm2 = dot_all(n, b, b, &t_red), rr = bnorm2;
    double thresh2 = tol * tol * bnorm2;
    int it = 0;
    t_red = 0.0;

    rapl_t rapl;
    unsigned long long e0[RAPL_MAXDOM], e1[RAPL_MAXDOM];
    int have_rapl = rank == 0 ? rapl_init(&rapl) : 0;
    double temp0 = 0.0, temp1 = 0.0;
    long thr0 = 0, thr1 = 0;
    if (rank == 0) { temp0 = pkg_temp_c(); thr0 = throttle_events(); }

    MPI_Barrier(MPI_COMM_WORLD);
    if (have_rapl && rapl_read(&rapl, e0)) have_rapl = 0;
    double t0 = MPI_Wtime();
    while (it < maxit && rr > thresh2 && rr > 0.0) {
        double t = MPI_Wtime();
        halo_exchange(&h, p);
        t_halo += MPI_Wtime() - t;
        spmv(&A, p, Ap);
        double alpha = rr / dot_all(n, p, Ap, &t_red);

        double s = 0.0;
        #pragma omp parallel for schedule(static) reduction(+:s)
        for (int i = 0; i < n; i++) {
            x[i] += alpha * p[i];
            r[i] -= alpha * Ap[i];
            s += r[i] * r[i];
        }
        double rr_new;
        t = MPI_Wtime();
        MPI_Allreduce(&s, &rr_new, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
        t_red += MPI_Wtime() - t;

        double beta = rr_new / rr;
        #pragma omp parallel for schedule(static)
        for (int i = 0; i < n; i++) p[i] = r[i] + beta * p[i];
        rr = rr_new;
        it++;
    }
    double t_solve = MPI_Wtime() - t0, t_max, t_halo_max, t_red_max;
    MPI_Barrier(MPI_COMM_WORLD);
    if (have_rapl && rapl_read(&rapl, e1)) have_rapl = 0;
    if (rank == 0) { temp1 = pkg_temp_c(); thr1 = throttle_events(); }

    /* where each OpenMP thread is running at the end of the solve */
    int nthr = omp_get_max_threads();
    int *mycpu = malloc(nthr * sizeof(int)), *allcpu = malloc((size_t)nthr * size * sizeof(int));
    #pragma omp parallel num_threads(nthr)
    mycpu[omp_get_thread_num()] = sched_getcpu();
    MPI_Gather(mycpu, nthr, MPI_INT, allcpu, nthr, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Reduce(&t_solve, &t_max, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    MPI_Reduce(&t_halo, &t_halo_max, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    MPI_Reduce(&t_red, &t_red_max, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    /* true residual ||b - Ax|| and max error vs ones */
    memcpy(p, x, n * sizeof *x);
    halo_exchange(&h, p);
    spmv(&A, p, Ap);
    double tr = 0.0, e = 0.0, tr_g, e_g;
    for (int i = 0; i < n; i++) {
        double d = b[i] - Ap[i];
        tr += d * d;
        if (fabs(x[i] - 1.0) > e) e = fabs(x[i] - 1.0);
    }
    MPI_Reduce(&tr, &tr_g, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    MPI_Reduce(&e, &e_g, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    int ghost_max, ghost_loc = h.nghost;
    MPI_Reduce(&ghost_loc, &ghost_max, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        omp_sched_t kind; int chunk;
        omp_get_schedule(&kind, &chunk);
        kind &= ~omp_sched_monotonic;
        const char *kn = kind == omp_sched_static ? "static" : kind == omp_sched_dynamic ? "dynamic"
                       : kind == omp_sched_guided ? "guided" : "auto";
        const char *dn[4] = {"package-0", "core", "uncore", "psys"};
        double ej[4];
        for (int d = 0; d < 4; d++) {
            int k = have_rapl ? rapl_find(&rapl, dn[d]) : -1;
            ej[d] = k >= 0 ? rapl_joules(&rapl, k, e0[k], e1[k]) : -1.0;
        }
        printf("matrix=%s n=%d nnz=%ld ranks=%d threads=%d sched=%s,%d iters=%d converged=%d "
               "rel_res=%.3e true_rel_res=%.3e max_err=%.3e ghost_max=%d "
               "time_s=%.6f halo_s=%.6f allreduce_s=%.6f "
               "e_pkg_j=%.3f e_core_j=%.3f e_uncore_j=%.3f e_psys_j=%.3f "
               "temp_start_c=%.1f temp_end_c=%.1f throttle_delta=%ld cpu_map=",
               spec, nglob, nnz_glob, size, nthr, kn, chunk, it,
               rr <= thresh2, sqrt(rr / bnorm2), sqrt(tr_g / bnorm2), e_g, ghost_max,
               t_max, t_halo_max, t_red_max, ej[0], ej[1], ej[2], ej[3],
               temp0, temp1, thr0 >= 0 && thr1 >= 0 ? thr1 - thr0 : -1);
        for (int q = 0; q < size; q++)
            for (int t = 0; t < nthr; t++)
                printf("%d%s", allcpu[q * nthr + t], t < nthr - 1 ? "." : q < size - 1 ? "/" : "\n");
    }

    free(x); free(b); free(r); free(Ap); free(p); free(bounds); free(mycpu); free(allcpu);
    csr_free(&A);
    MPI_Finalize();
    return 0;
}
