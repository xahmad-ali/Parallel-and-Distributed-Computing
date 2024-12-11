#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define ARRAY_SIZE 10

int main(int argc, char** argv) {
    int rank, size;
    int array[ARRAY_SIZE];
    int *recv_buffer = NULL;
    MPI_Status status;

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    for (int i = 0; i < ARRAY_SIZE; i++) {
        array[i] = rank * 100 + i;
    }

    printf("Process %d sending array: ", rank);
    for (int i = 0; i < ARRAY_SIZE; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");

    if (rank == 0) {
        recv_buffer = (int*) malloc(size * ARRAY_SIZE * sizeof(int));
        if (recv_buffer == NULL) {
            fprintf(stderr, "Memory allocation failed for recv_buffer.\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }

        for (int i = 1; i < size; i++) {
            MPI_Recv(&recv_buffer[i * ARRAY_SIZE], ARRAY_SIZE, MPI_INT, i, 0, MPI_COMM_WORLD, &status);
        }

        for (int i = 0; i < ARRAY_SIZE; i++) {
            recv_buffer[i] = array[i];
        }

        printf("Root process %d received arrays:\n", rank);
        for (int i = 0; i < size * ARRAY_SIZE; i++) {
            printf("%d ", recv_buffer[i]);
        }
        printf("\n");

        free(recv_buffer);
    } else {
        MPI_Send(array, ARRAY_SIZE, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();

    return 0;
}
