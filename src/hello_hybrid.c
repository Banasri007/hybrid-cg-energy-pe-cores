#define _GNU_SOURCE
#include <mpi.h>
#include <omp.h>
#include <sched.h>
#include <stdio.h>
int main(int argc, char **argv) {
    int prov, rank, size;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &prov);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    #pragma omp parallel
    printf("rank %d/%d thread %d/%d on cpu %d (thread level %d)\n",
           rank, size, omp_get_thread_num(), omp_get_num_threads(), sched_getcpu(), prov);
    MPI_Finalize();
    return 0;
}
