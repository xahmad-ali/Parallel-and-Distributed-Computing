#include <stdio.h>
#include <omp.h>

int main()
{

    int n = 100;
    int result[n];

#pragma omp parallel
    {

#pragma omp for schedule(static,5)
        for (int i = 0; i < n; i++)
        {
            int thread_id = omp_get_thread_num();
            result[i] = thread_id * n +i;
        }
    }

    printf("result with dynamic scheduling: \n");
    for (int i = 0; i < n; i++)
    {
        printf("%d \n", result[i]);
    
    }
    printf("\n");

    return 0;
}