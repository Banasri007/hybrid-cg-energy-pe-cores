/* Reverse Cuthill-McKee reordering: B = P A P^T, written as a binary .csr.
 *
 * Usage: rcm <in: matrix.mtx | .csr | poisson:M> <out.csr>
 *
 * Symmetric permutation keeps A SPD and keeps b = A*1 -> x* = 1, so CG
 * results are directly comparable. Reports bandwidth and, for row-block
 * partitions into 2/4/8/12/16 parts, the max halo (ghost) size per part. */
#include "csr.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const int *g_deg;
static int cmp_deg(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (g_deg[x] > g_deg[y]) - (g_deg[x] < g_deg[y]);
}

/* BFS from s over unvisited nodes; returns number of levels, fills last
 * level's min-degree node in *far. Uses stamp[] to avoid clearing. */
static int bfs_levels(const csr_t *A, const int *deg, const char *done, int s,
                      int *stamp, int tag, int *queue, int *lvl, int *far) {
    int head = 0, tail = 0, nlev = 0;
    queue[tail++] = s; stamp[s] = tag; lvl[s] = 0;
    while (head < tail) {
        int u = queue[head++];
        if (lvl[u] + 1 > nlev) nlev = lvl[u] + 1;
        for (long k = A->rowptr[u]; k < A->rowptr[u + 1]; k++) {
            int v = A->col[k];
            if (!done[v] && stamp[v] != tag) {
                stamp[v] = tag; lvl[v] = lvl[u] + 1; queue[tail++] = v;
            }
        }
    }
    int best = -1;
    for (int i = 0; i < tail; i++) {
        int u = queue[i];
        if (lvl[u] == nlev - 1 && (best < 0 || deg[u] < deg[best])) best = u;
    }
    *far = best;
    return nlev;
}

static void rcm_order(const csr_t *A, int *perm) {
    int n = A->n;
    int *deg = malloc(n * sizeof(int)), *stamp = malloc(n * sizeof(int));
    int *queue = malloc(n * sizeof(int)), *lvl = malloc(n * sizeof(int));
    char *done = calloc(n, 1);
    int *nbr = NULL; size_t nbrcap = 0;
    for (int i = 0; i < n; i++) { deg[i] = (int)(A->rowptr[i + 1] - A->rowptr[i]); stamp[i] = 0; }
    g_deg = deg;
    int tag = 0, pos = 0;

    for (int s0 = 0; s0 < n; s0++) {
        if (done[s0]) continue;
        /* George-Liu pseudo-peripheral node */
        int s = s0, far, nlev = bfs_levels(A, deg, done, s, stamp, ++tag, queue, lvl, &far);
        for (int rep = 0; rep < 8; rep++) {
            int far2, nl2 = bfs_levels(A, deg, done, far, stamp, ++tag, queue, lvl, &far2);
            if (nl2 <= nlev) break;
            s = far; nlev = nl2; far = far2;
        }
        /* Cuthill-McKee BFS, neighbours in increasing degree */
        int head = pos;
        perm[pos++] = s; done[s] = 1;
        while (head < pos) {
            int u = perm[head++];
            size_t cnt = 0;
            long d = A->rowptr[u + 1] - A->rowptr[u];
            if ((size_t)d > nbrcap) { nbrcap = d; nbr = realloc(nbr, nbrcap * sizeof(int)); }
            for (long k = A->rowptr[u]; k < A->rowptr[u + 1]; k++) {
                int v = A->col[k];
                if (!done[v]) { done[v] = 1; nbr[cnt++] = v; }
            }
            qsort(nbr, cnt, sizeof(int), cmp_deg);
            memcpy(perm + pos, nbr, cnt * sizeof(int));
            pos += (int)cnt;
        }
    }
    for (int i = 0; i < n / 2; i++) { int t = perm[i]; perm[i] = perm[n - 1 - i]; perm[n - 1 - i] = t; }
    free(deg); free(stamp); free(queue); free(lvl); free(done); free(nbr);
}

static void permute(const csr_t *A, const int *perm, csr_t *B) {
    int n = A->n;
    int *inv = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) inv[perm[i]] = i;
    B->n = n; B->nnz = A->nnz;
    B->rowptr = malloc((n + 1) * sizeof(long));
    B->col = malloc(A->nnz * sizeof(int));
    B->val = malloc(A->nnz * sizeof(double));
    long k = 0;
    for (int i = 0; i < n; i++) {
        B->rowptr[i] = k;
        int o = perm[i];
        long start = k;
        for (long q = A->rowptr[o]; q < A->rowptr[o + 1]; q++) {
            /* insertion sort by new column index */
            int c = inv[A->col[q]]; double v = A->val[q];
            long j = k++;
            while (j > start && B->col[j - 1] > c) { B->col[j] = B->col[j - 1]; B->val[j] = B->val[j - 1]; j--; }
            B->col[j] = c; B->val[j] = v;
        }
    }
    B->rowptr[n] = k;
    free(inv);
}

static long bandwidth(const csr_t *A) {
    long bw = 0;
    for (int i = 0; i < A->n; i++)
        for (long k = A->rowptr[i]; k < A->rowptr[i + 1]; k++) {
            long d = labs((long)A->col[k] - i);
            if (d > bw) bw = d;
        }
    return bw;
}

/* max over parts of distinct off-block columns, nnz-balanced row blocks */
static long max_ghosts(const csr_t *A, int nparts) {
    int n = A->n, *stamp = calloc(n, sizeof(int));
    long total = A->rowptr[n], worst = 0;
    int r0 = 0;
    for (int p = 0; p < nparts; p++) {
        int r1 = r0;
        long target = total * (p + 1) / nparts;
        while (r1 < n && (p == nparts - 1 || A->rowptr[r1] < target)) r1++;
        long g = 0;
        for (long k = A->rowptr[r0]; k < A->rowptr[r1]; k++) {
            int c = A->col[k];
            if ((c < r0 || c >= r1) && stamp[c] != p + 1) { stamp[c] = p + 1; g++; }
        }
        if (g > worst) worst = g;
        r0 = r1;
    }
    free(stamp);
    return worst;
}

static void report(const char *tag, const csr_t *A) {
    printf("%-8s bandwidth=%-8ld max_ghosts(P=2,4,8,12,16)=", tag, bandwidth(A));
    int ps[] = {2, 4, 8, 12, 16};
    for (int i = 0; i < 5; i++) printf("%ld%s", max_ghosts(A, ps[i]), i < 4 ? "," : "\n");
}

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: %s <in> <out.csr>\n", argv[0]); return 1; }
    csr_t A, B;
    if (csr_load(argv[1], &A)) return 1;
    printf("%s n=%d nnz=%ld rows_per_part(P=8)=%d\n", argv[1], A.n, A.nnz, A.n / 8);
    report("original", &A);
    int *perm = malloc(A.n * sizeof(int));
    double t = wall_time();
    rcm_order(&A, perm);
    permute(&A, perm, &B);
    printf("rcm_time_s=%.2f\n", wall_time() - t);
    report("rcm", &B);
    csr_write(argv[2], &B);
    free(perm); csr_free(&A); csr_free(&B);
    return 0;
}
