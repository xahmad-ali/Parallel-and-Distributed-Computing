#include <mpi.h>
#include <iostream>
#include <vector>
#include <numeric>
#include <chrono>

int main(int argc, char *argv[]) {
    int rank, size;
    const int N = 1000000;  // Size of the array
    std::vector<int> array(N, 1);  // Initialize an array with all elements as 1
    int local_sum = 0;
    int total_sum = 0;

    MPI_Init(&argc, &argv);                  // Initialize MPI environment
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);    // Get the rank of the process
    MPI_Comm_size(MPI_COMM_WORLD, &size);    // Get the total number of processes

    // Determine the portion of the array for each process
    int chunk_size = N / size;
    int start = rank * chunk_size;
    int end = (rank == size - 1) ? N : start + chunk_size;

    // Measure the start time on the master node
    auto start_time = std::chrono::high_resolution_clock::now();

    // Each process calculates the sum of its portion of the array
    local_sum = std::accumulate(array.begin() + start, array.begin() + end, 0);

    // Use MPI_Reduce to sum up all local sums into total_sum on the root node (rank 0)
    MPI_Reduce(&local_sum, &total_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // Measure the end time on the master node
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    // On the root process, print the result and execution time
    if (rank == 0) {
        std::cout << "Output (On " << size << " Nodes):\n";
        std::cout << "Total Sum: " << total_sum << "\n";
        std::cout << "Execution Time: " << elapsed.count() << " seconds\n";
        // You can calculate the speedup by comparing it with single-node execution time
    }

    MPI_Finalize();  // Finalize the MPI environment
    return 0;
}
