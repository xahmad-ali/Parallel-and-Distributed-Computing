#include <stdio.h>
#include <omp.h>

int main()
{

    int arr[] = {1, 2, 3, 4, 5};
    int arrL = sizeof(arr) / sizeof(arr[0]);
    int sum = 0;

// Parallel for loop with reduction
// Reduction important in situations where multiple threads are modifying a shared variable
#pragma omp parallel for reduction(+ :sum)
    for (int i = 0; i < arrL; i++)
    {
        sum = sum + arr[i];
    }

    // The reduction clause ensures that multiple threads can independently 
    // compute their own partial results in parallel, and then these partial results 
    // are combined (or "reduced") into a final value after the parallel section completes
    
    printf("Total sum: %d\n", sum);

    return 0;
}