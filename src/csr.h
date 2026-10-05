#ifndef CSR_H
#define CSR_H

/* Compressed Sparse Row matrix, 0-based indices. */
typedef struct {
    int n;          /* rows == cols (square) */
    long nnz;
    long *rowptr;   /* n+1 */
    int *col;       /* nnz */
    double *val;    /* nnz */
} csr_t;

/* Load a matrix. spec is either a Matrix Market path (.mtx) or "poisson:M"
 * (5-point 2D Laplacian on an MxM grid, n = M*M), or a binary .csr file. Symmetric .mtx files are
 * expanded to full storage. A binary cache <path>.csr is written on first
 * load and reused afterwards. Returns 0 on success. */
int csr_load(const char *spec, csr_t *A);
void csr_free(csr_t *A);

/* Write A in the binary CSR format (loadable later via a spec ending in .csr). */
void csr_write(const char *path, const csr_t *A);

/* Make sure the binary cache for spec exists (no-op for poisson:). Call on one
 * rank, then barrier, before csr_load_part. */
int csr_prepare(const char *spec);

/* Load this part's contiguous row block, partitioned so each of nparts parts
 * gets ~equal nnz. A->n is the local row count; column indices stay GLOBAL.
 * bounds[0..nparts] receives the global row boundaries of every part. */
int csr_load_part(const char *spec, int nparts, int part, csr_t *A,
                  int *bounds, int *nglobal);

/* y = A x  (sequential) */
void csr_spmv(const csr_t *A, const double *x, double *y);

double wall_time(void);

#endif
