#include <stdio.h>
#include <omp.h>  // Include the OpenMP library

int main(){

     // Define matrices A and B
    int a[2][3] = {{1, 2, 3}, {2, 3, 4}};
    int b[3][2] = {{2, 2}, {1, 1}, {3, 3}};
    int result[2][2];
    int m = 2, n = 3, p = 3, q = 2; // dimensions of matrices
    int i, j, k;

     // Initialize result matrix to 0
    for (i = 0; i < m; i++) {
        for (j = 0; j < q; j++) {
            result[i][j] = 0;
        }
    }


     // Perform matrix multiplication using OpenMP
     // The collapse(2) clause in OpenMP is used to combine multiple (2 loops)
     //nested loops into a single iteration space for parallelization.
     //  Each thread would work on a different i, but the j loop would still be sequential
     // for this both i and j loop are collapsed to single loop, on which multiple threads can work
    #pragma omp parallel for collapse(2) private(i, j, k) shared(a, b, result)
    for (i = 0; i < m; i++) {
        for (j = 0; j < q; j++) {
            for (k = 0; k < n; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
            // Print thread info for each outer loop iteration
            printf("Thread %d calculates result[%d][%d]\n", omp_get_thread_num(), i, j);
        }
    }

    for(i=0;i<m; i++){
        for(j=0; j<q; j++){
            printf(" %d",result[i][j]);
        }
        printf("\n");
    }

    return 0;
}