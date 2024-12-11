#include <iostream.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int i;
    int nitems = 10;
    int mynode, totalnodes;
    MPI_Status status;
    double *array;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &totalnodes);
    MPI_Comm_rank(MPI_COMM_WORLD, &mynode);

    double* array = new double[nitems];

    if (mynode == 0) {
        for (int i = 0; i < nitems; i++) {
            array[i] = (double)i;
        }

        for (int i = 1; i < totalnodes; i++) {
            MPI_Send(array, nitems, MPI_DOUBLE, i, 1, MPI_COMM_WORLD);
        }
    } else {
        MPI_Recv(array, nitems, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD,   
 MPI_STATUS_IGNORE);
    }

    for (int i = 0; i < nitems; i++) {
        std::cout << "Processor " << mynode << ": array[" << i << "] = " << array[i] << std::endl;
    }

    MPI_Finalize();

    return 0;

}
