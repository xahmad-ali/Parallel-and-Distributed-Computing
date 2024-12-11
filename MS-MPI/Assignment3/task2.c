#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>

int IncOrder(const void *e1, const void *e2);
void CompareSplit(int nlocal, int *elmnts, int *relmnts, int *wspace, int keepsmall);

int main(int argc, char *argv[]) {
    int n;
    int npes;
    int myrank;
    int nlocal;
    int *elmnts;
    int *relmts;
    int oddrank;
    int evenrank;
    int *wspace;
    int i;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &npes);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    n = atoi(argv[1]);
    nlocal = n / npes;
    
    elmnts = (int *)malloc(nlocal * sizeof(int));
    relmts = (int *)malloc(nlocal * sizeof(int));
    wspace = (int *)malloc(nlocal * sizeof(int));

    srand(myrank);
    
    for (i = 0; i < nlocal; i++){
        elmnts[i] = rand();}

        qsort(elmnts, nlocal, sizeof(int), IncOrder);
//////////////////////////
    if (myrank % 2 == 0) {
        oddrank = myrank - 1;
        evenrank = myrank + 1;
    } else {
        oddrank = myrank + 1;
        evenrank = myrank - 1;
    }
    ////////////////////////////
    if (oddrank == -1 || oddrank == npes)
        oddrank = MPI_PROC_NULL;
    if (evenrank == -1 || evenrank == npes)
        evenrank = MPI_PROC_NULL;

    for (i = 0; i < npes - 1; i++) {
        if (i % 2 == 1)
        MPI_Sendrecv(elmnts, nlocal, MPI_INT, oddrank, 1,
                        relmts, nlocal, MPI_INT, oddrank, 1,
                        MPI_COMM_WORLD, &status);
        else
        MPI_Sendrecv(elmnts, nlocal, MPI_INT, evenrank, 1,
                        relmts, nlocal, MPI_INT, evenrank, 1,
                        MPI_COMM_WORLD, &status);

        CompareSplit(nlocal, elmnts, relmts, wspace, myrank < status.MPI_SOURCE);
    }

free(elmnts);
free(relmts);
free(wspace);
MPI_Finalize();
return 0;
}

void CompareSplit(int nlocal, int *elmnts, int *relmnts, int *wspace, int keepsmall) {
    int i, j, k;

    for (i = 0; i < nlocal; i++)
        wspace[i] = elmnts[i];

    if (keepsmall) {
    for (i = j = k = 0; k < nlocal; k++) {
        if (j == nlocal || (i < nlocal && wspace[i] < relmnts[j]))
            elmnts[k] = wspace[i++];
        else
            elmnts[k] = relmnts[j++];
    }
    } else {
    for (i = nlocal - 1, k = nlocal - 1, j = nlocal - 1; k >= 0; k--) {
        if (j < 0 || (i >= 0 && wspace[i] >= relmnts[j]))
            elmnts[k] = wspace[i--];
        else
            elmnts[k] = relmnts[j--];
    }
    }
}

int IncOrder(const void *e1, const void *e2) {
    return (*((int *)e1) - *((int *)e2));
}