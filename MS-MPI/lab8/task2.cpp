#include <mpi.h>
#include <iostream>

int main(int argc, char *argv[]) {
    int rank, size;
    int a, b;  // 'a' is the node ID, 'b' will store values received from other nodes
    int prefix_sum = 0;  // This will hold the accumulated prefix sum for each process

    MPI_Init(&argc, &argv);               // Initialize MPI environment
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // Get the rank of the process
    MPI_Comm_size(MPI_COMM_WORLD, &size);  // Get the total number of processes

    a = rank;   // Initialize 'a' with the node ID (rank)
    prefix_sum = a;  // Initialize prefix sum with the value of 'a'

    // Perform the prefix sum calculation
    for (int step = 1; step < size; ++step) {
        if (rank >= step) {
            // Receive from the left (rank - step)
            MPI_Recv(&b, 1, MPI_INT, rank - step, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            prefix_sum += b;  // Accumulate received value into prefix sum
        }
        if (rank + step < size) {
            // Send to the right (rank + step)
            MPI_Send(&prefix_sum, 1, MPI_INT, rank + step, 0, MPI_COMM_WORLD);
        }
    }

    // Print the prefix sum result for each process
    std::cout << "Process " << rank << " has prefix sum: " << prefix_sum << std::endl;

    MPI_Finalize();  // Finalize the MPI environment
    return 0;
}
