#include <stdio.h>
#include <mpi.h>
#include <time.h>

void timestamp() {
    time_t current_time;
    struct tm *time_info;

    time(&current_time);
    time_info = localtime(&current_time);
    printf("Timestamp: %s", asctime(time_info));
}

int main(int argc, char** argv) {
    int mynode, totalnodes;
    int sum, startval, endval, accum;
    MPI_Status status;

    MPI_Init(&argc, &argv);

    MPI_Comm_size(MPI_COMM_WORLD, &totalnodes);
    MPI_Comm_rank(MPI_COMM_WORLD, &mynode);

    if (mynode == 0) {
        printf("Start of parallel computation: ");
        timestamp();
    }

    sum = 0;
    startval = 1000 * mynode / totalnodes + 1;
    endval = 1000 * (mynode + 1) / totalnodes;

    for (int i = startval; i <= endval; i++) {
        sum += i;
    }

    if (mynode != 0) {
        MPI_Send(&sum, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
    } else {
        for (int j = 1; j < totalnodes; j++) {
            MPI_Recv(&accum, 1, MPI_INT, j, 1, MPI_COMM_WORLD, &status);
            sum += accum;
        }

        printf("The sum from 1 to 1000 is: %d\n", sum);
    }

    if (mynode == 0) {
        printf("End of parallel computation: ");
        timestamp();
    }

    MPI_Finalize();

    return 0;
}
