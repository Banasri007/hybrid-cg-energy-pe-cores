CC      = gcc
MPICC   = mpicc
CFLAGS  = -O3 -march=native -Wall -Wextra -std=c11
LDLIBS  = -lm

all: cg_seq cg_hybrid rcm rapl_idle hello_hybrid

cg_seq: cg_seq.c csr.c csr.h
	$(CC) $(CFLAGS) -o $@ cg_seq.c csr.c $(LDLIBS)

cg_hybrid: cg_hybrid.c csr.c csr.h rapl.c rapl.h
	$(MPICC) $(CFLAGS) -fopenmp -o $@ cg_hybrid.c csr.c rapl.c $(LDLIBS)

rcm: rcm.c csr.c csr.h
	$(CC) $(CFLAGS) -o $@ rcm.c csr.c $(LDLIBS)

rapl_idle: rapl_idle.c rapl.c rapl.h csr.c csr.h
	$(CC) $(CFLAGS) -o $@ rapl_idle.c rapl.c csr.c $(LDLIBS)

hello_hybrid: hello_hybrid.c
	$(MPICC) -O2 -fopenmp -o $@ $<

test: cg_seq
	./cg_seq poisson:64 1e-10
	./cg_seq poisson:256 1e-10

clean:
	rm -f cg_seq cg_hybrid rcm rapl_idle hello_hybrid

.PHONY: all test clean
