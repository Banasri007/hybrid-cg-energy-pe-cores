/* Sequential (unpreconditioned) Conjugate Gradient — correctness reference
 * and single-core baseline.
 *
 * Usage: cg_seq <matrix.mtx | poisson:M> [tol=1e-8] [maxit=10000]
 * RHS is b = A*1, so the exact solution is x* = ones; x0 = 0.
 * Only the solve loop is timed (load and setup excluded). */
#include "csr.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double dot(int n, const double *a, const double *b) {
    double s = 0.0;
    for (int i = 0; i < n; i++) s += a[i] * b[i];
    return s;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <matrix.mtx | poisson:M> [tol] [maxit]\n", argv[0]);
        return 1;
    }
    double tol = argc > 2 ? atof(argv[2]) : 1e-8;
    int maxit = argc > 3 ? atoi(argv[3]) : 10000;

    csr_t A;
    if (csr_load(argv[1], &A)) return 1;
    int n = A.n;

    double *x = calloc(n, sizeof *x), *b = malloc(n * sizeof *b);
    double *r = malloc(n * sizeof *r), *p = malloc(n * sizeof *p), *Ap = malloc(n * sizeof *Ap);
    for (int i = 0; i < n; i++) x[i] = 1.0;
    csr_spmv(&A, x, b);                       /* b = A * ones */
    for (int i = 0; i < n; i++) { x[i] = 0.0; r[i] = b[i]; p[i] = b[i]; }

    double bnorm = sqrt(dot(n, b, b));
    double rr = dot(n, r, r);
    int it = 0;

    double t0 = wall_time();
    while (it < maxit && sqrt(rr) > tol * bnorm) {
        csr_spmv(&A, p, Ap);
        double alpha = rr / dot(n, p, Ap);
        for (int i = 0; i < n; i++) { x[i] += alpha * p[i]; r[i] -= alpha * Ap[i]; }
        double rr_new = dot(n, r, r);
        double beta = rr_new / rr;
        for (int i = 0; i < n; i++) p[i] = r[i] + beta * p[i];
        rr = rr_new;
        it++;
    }
    double t1 = wall_time();

    /* true residual and error vs known solution */
    csr_spmv(&A, x, Ap);
    double tr = 0.0, err = 0.0;
    for (int i = 0; i < n; i++) {
        double d = b[i] - Ap[i];
        tr += d * d;
        if (fabs(x[i] - 1.0) > err) err = fabs(x[i] - 1.0);
    }
    printf("matrix=%s n=%d nnz=%ld iters=%d converged=%d rel_res=%.3e true_rel_res=%.3e "
           "max_err=%.3e time_s=%.6f\n",
           argv[1], n, A.nnz, it, sqrt(rr) <= tol * bnorm, sqrt(rr) / bnorm,
           sqrt(tr) / bnorm, err, t1 - t0);

    free(x); free(b); free(r); free(p); free(Ap);
    csr_free(&A);
    return 0;
}
