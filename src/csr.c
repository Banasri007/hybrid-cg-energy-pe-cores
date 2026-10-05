#define _POSIX_C_SOURCE 200809L
#include "csr.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <time.h>

double wall_time(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + 1e-9 * t.tv_nsec;
}

void csr_free(csr_t *A) {
    free(A->rowptr); free(A->col); free(A->val);
    memset(A, 0, sizeof *A);
}

void csr_spmv(const csr_t *A, const double *x, double *y) {
    for (int i = 0; i < A->n; i++) {
        double s = 0.0;
        for (long k = A->rowptr[i]; k < A->rowptr[i + 1]; k++)
            s += A->val[k] * x[A->col[k]];
        y[i] = s;
    }
}

static int alloc_csr(csr_t *A, int n, long nnz) {
    A->n = n; A->nnz = nnz;
    A->rowptr = malloc((size_t)(n + 1) * sizeof(long));
    A->col = malloc((size_t)nnz * sizeof(int));
    A->val = malloc((size_t)nnz * sizeof(double));
    return (A->rowptr && A->col && A->val) ? 0 : -1;
}

static int build_poisson(int m, csr_t *A) {
    int n = m * m;
    if (alloc_csr(A, n, 5L * n)) return -1;
    long k = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < m; j++) {
            int r = i * m + j;
            A->rowptr[r] = k;
            if (i > 0)     { A->col[k] = r - m; A->val[k++] = -1.0; }
            if (j > 0)     { A->col[k] = r - 1; A->val[k++] = -1.0; }
            A->col[k] = r; A->val[k++] = 4.0;
            if (j < m - 1) { A->col[k] = r + 1; A->val[k++] = -1.0; }
            if (i < m - 1) { A->col[k] = r + m; A->val[k++] = -1.0; }
        }
    A->rowptr[n] = k;
    A->nnz = k;
    return 0;
}

static int read_cache(const char *path, csr_t *A) {
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    int n; long nnz; int ok = 0;
    if (fread(&n, sizeof n, 1, f) == 1 && fread(&nnz, sizeof nnz, 1, f) == 1 &&
        alloc_csr(A, n, nnz) == 0 &&
        fread(A->rowptr, sizeof(long), (size_t)n + 1, f) == (size_t)n + 1 &&
        fread(A->col, sizeof(int), (size_t)nnz, f) == (size_t)nnz &&
        fread(A->val, sizeof(double), (size_t)nnz, f) == (size_t)nnz)
        ok = 1;
    fclose(f);
    if (!ok) { csr_free(A); return -1; }
    return 0;
}

void csr_write(const char *path, const csr_t *A) {
    FILE *f = fopen(path, "wb");
    if (!f) return;
    fwrite(&A->n, sizeof A->n, 1, f);
    fwrite(&A->nnz, sizeof A->nnz, 1, f);
    fwrite(A->rowptr, sizeof(long), (size_t)A->n + 1, f);
    fwrite(A->col, sizeof(int), (size_t)A->nnz, f);
    fwrite(A->val, sizeof(double), (size_t)A->nnz, f);
    fclose(f);
}

static int read_mtx(const char *path, csr_t *A) {
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); return -1; }
    char line[1024], obj[64], fmt[64], field[64], sym[64];
    if (!fgets(line, sizeof line, f) ||
        sscanf(line, "%%%%MatrixMarket %63s %63s %63s %63s", obj, fmt, field, sym) != 4 ||
        strcasecmp(fmt, "coordinate") != 0) {
        fprintf(stderr, "%s: not a coordinate Matrix Market file\n", path);
        fclose(f); return -1;
    }
    if (strcasecmp(field, "real") != 0 && strcasecmp(field, "integer") != 0) {
        fprintf(stderr, "%s: unsupported field '%s'\n", path, field);
        fclose(f); return -1;
    }
    int symmetric = strcasecmp(sym, "symmetric") == 0;
    if (!symmetric && strcasecmp(sym, "general") != 0) {
        fprintf(stderr, "%s: unsupported symmetry '%s'\n", path, sym);
        fclose(f); return -1;
    }
    do {
        if (!fgets(line, sizeof line, f)) { fclose(f); return -1; }
    } while (line[0] == '%');
    int nr, nc; long ne;
    if (sscanf(line, "%d %d %ld", &nr, &nc, &ne) != 3 || nr != nc) {
        fprintf(stderr, "%s: bad size line or non-square\n", path);
        fclose(f); return -1;
    }
    int *I = malloc(ne * sizeof(int)), *J = malloc(ne * sizeof(int));
    double *V = malloc(ne * sizeof(double));
    long *cnt = calloc((size_t)nr + 1, sizeof(long));
    for (long e = 0; e < ne; e++) {
        if (fscanf(f, "%d %d %lf", &I[e], &J[e], &V[e]) != 3) {
            fprintf(stderr, "%s: truncated at entry %ld\n", path, e);
            fclose(f); return -1;
        }
        I[e]--; J[e]--;
        cnt[I[e] + 1]++;
        if (symmetric && I[e] != J[e]) cnt[J[e] + 1]++;
    }
    fclose(f);
    for (int i = 0; i < nr; i++) cnt[i + 1] += cnt[i];
    if (alloc_csr(A, nr, cnt[nr])) return -1;
    memcpy(A->rowptr, cnt, (size_t)(nr + 1) * sizeof(long));
    for (long e = 0; e < ne; e++) {
        long p = cnt[I[e]]++;
        A->col[p] = J[e]; A->val[p] = V[e];
        if (symmetric && I[e] != J[e]) {
            p = cnt[J[e]]++;
            A->col[p] = I[e]; A->val[p] = V[e];
        }
    }
    free(I); free(J); free(V); free(cnt);
    return 0;
}

/* A spec ending in ".csr" is itself a binary CSR file; otherwise the cache
 * lives next to the .mtx as <spec>.csr */
static int is_csr(const char *spec) {
    size_t l = strlen(spec);
    return l > 4 && strcmp(spec + l - 4, ".csr") == 0;
}

static void cache_path(const char *spec, char *buf, size_t len) {
    if (is_csr(spec)) snprintf(buf, len, "%s", spec);
    else snprintf(buf, len, "%s.csr", spec);
}

int csr_prepare(const char *spec) {
    if (strncmp(spec, "poisson:", 8) == 0) return 0;
    char cache[4096];
    cache_path(spec, cache, sizeof cache);
    FILE *f = fopen(cache, "rb");
    if (f) { fclose(f); return 0; }
    csr_t A;
    if (csr_load(spec, &A)) return -1;
    csr_free(&A);
    return 0;
}

int csr_load_part(const char *spec, int nparts, int part, csr_t *A,
                  int *bounds, int *nglobal) {
    memset(A, 0, sizeof *A);
    csr_t F = {0};
    FILE *f = NULL;
    long *rp;
    int n;
    off_t base = sizeof(int) + sizeof(long);   /* cache header */
    if (strncmp(spec, "poisson:", 8) == 0) {
        if (build_poisson(atoi(spec + 8), &F)) return -1;
        n = F.n; rp = F.rowptr;
    } else {
        char cache[4096];
        cache_path(spec, cache, sizeof cache);
        long nnz;
        f = fopen(cache, "rb");
        if (!f || fread(&n, sizeof n, 1, f) != 1 || fread(&nnz, sizeof nnz, 1, f) != 1) {
            fprintf(stderr, "%s: missing/corrupt cache (call csr_prepare first)\n", cache);
            if (f) fclose(f);
            return -1;
        }
        rp = malloc((size_t)(n + 1) * sizeof(long));
        if (fread(rp, sizeof(long), (size_t)n + 1, f) != (size_t)n + 1) { fclose(f); return -1; }
    }

    /* nnz-balanced contiguous row blocks */
    long total = rp[n];
    int r = 0;
    bounds[0] = 0;
    for (int p = 1; p < nparts; p++) {
        long target = total * p / nparts;
        while (r < n && rp[r] < target) r++;
        bounds[p] = r;
    }
    bounds[nparts] = n;
    *nglobal = n;

    int r0 = bounds[part], r1 = bounds[part + 1];
    long k0 = rp[r0], k1 = rp[r1];
    int ok = alloc_csr(A, r1 - r0, k1 - k0) == 0;
    if (ok) {
        for (int i = 0; i <= r1 - r0; i++) A->rowptr[i] = rp[r0 + i] - k0;
        if (f) {
            off_t colpos = base + (off_t)(n + 1) * sizeof(long);
            off_t valpos = colpos + (off_t)total * sizeof(int);
            ok = fseeko(f, colpos + (off_t)k0 * sizeof(int), SEEK_SET) == 0 &&
                 fread(A->col, sizeof(int), (size_t)(k1 - k0), f) == (size_t)(k1 - k0) &&
                 fseeko(f, valpos + (off_t)k0 * sizeof(double), SEEK_SET) == 0 &&
                 fread(A->val, sizeof(double), (size_t)(k1 - k0), f) == (size_t)(k1 - k0);
        } else {
            memcpy(A->col, F.col + k0, (size_t)(k1 - k0) * sizeof(int));
            memcpy(A->val, F.val + k0, (size_t)(k1 - k0) * sizeof(double));
        }
    }
    if (f) { fclose(f); free(rp); }
    else csr_free(&F);
    if (!ok) { csr_free(A); return -1; }
    return 0;
}

int csr_load(const char *spec, csr_t *A) {
    memset(A, 0, sizeof *A);
    if (strncmp(spec, "poisson:", 8) == 0)
        return build_poisson(atoi(spec + 8), A);
    char cache[4096];
    cache_path(spec, cache, sizeof cache);
    if (read_cache(cache, A) == 0) return 0;
    if (is_csr(spec)) { fprintf(stderr, "%s: cannot read\n", spec); return -1; }
    if (read_mtx(spec, A)) return -1;
    csr_write(cache, A);
    return 0;
}
