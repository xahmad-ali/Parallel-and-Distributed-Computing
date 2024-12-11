#include <mpi.h>
#include <iostream>
#include <vector>
using namespace std;

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank); 
    MPI_Comm_size(MPI_COMM_WORLD, &world_size); // Get total number of ps

    vector<int> array = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int array_size = array.size();
    int chunk_size = array_size / world_size;
    int start_index = world_rank * chunk_size;
    int end_index = (world_rank == world_size - 1) ? array_size : start_index + chunk_size;

    double partial_sum = 0;
    for (int i = start_index; i < end_index; i++) {
        partial_sum += array[i];
    }

    cout << "Number of Processes available is " << world_size <<"\n";
    cout << "\nSUM - Process " << world_rank << ": \n\t My contribution to the sum is " << partial_sum << "\n";
    double total_sum = 0;
    MPI_Reduce(&partial_sum, &total_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    if (world_rank == 0) {
        cout << "SUM - Master process: \n\t The total sum is " << total_sum << "\n";
        cout << "SUM - Master process: \n\t Normal end of execution.\n";
    }
    MPI_Finalize();
    return 0;
}
