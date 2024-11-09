#include <iostream>
#include <mpi.h>

int main(int argc, char** argv) {
    int mynode, totalnodes;
    int sum, startval, endval, accum;
    MPI_Status status;

    // Initialize MPI environment
    MPI_Init(&argc, &argv);

    // Get the total number of processes and the rank of the current process
    MPI_Comm_size(MPI_COMM_WORLD, &totalnodes);
    MPI_Comm_rank(MPI_COMM_WORLD, &mynode);

    // Initialize sum and calculate range for each process
    sum = 0;
    startval = 1000 * mynode / totalnodes + 1;
    endval = 1000 * (mynode + 1) / totalnodes;

    // Each process calculates the sum of a range of numbers
    for (int i = startval; i <= endval; i++) {
        sum += i;
    }

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int mynode, totalnodes;
    MPI_Comm_rank(MPI_COMM_WORLD, &mynode);
    MPI_Comm_size(MPI_COMM_WORLD, &totalnodes);

    int sum = 0, accum;
    MPI_Status status;

    // Calculate partial sum on each process
    for (int i = mynode + 1; i <= 1000; i += totalnodes) {
        sum += i;
    }

    // Send the sum from each process to the root (rank 0)
    if (mynode != 0) {
        MPI_Send(&sum, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
    } else {
        // Root process (rank 0) receives sums from all other processes
        for (int j = 1; j < totalnodes; j++) {
            MPI_Recv(&accum, 1, MPI_INT, j, 1, MPI_COMM_WORLD, &status);
            sum += accum;
        }

        // Print the final result
        std::cout << "The sum from 1 to 1000 is: " << sum << std::endl;
    }

    MPI_Finalize();
    return 0;
}
