#include <stdio.h>
#include <omp.h>  // Include the OpenMP library

int main() {
    // Set the number of threads (optional)
    int num_threads = 4;
    omp_set_num_threads(num_threads);

    // Parallel region begins here
    #pragma omp parallel
    {
        // Each thread gets its ID
        int thread_id = omp_get_thread_num();
        int total_threads = omp_get_num_threads();

        // Print message from each thread
        printf("Hello from thread %d out of %d threads\n", thread_id, total_threads);
    }

    return 0;
}
