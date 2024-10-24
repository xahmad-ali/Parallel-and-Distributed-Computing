#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <time.h>
#define N 100000

int main()
{

    int arr[N] = {0};
    long int sum = 0;
    srand(time(NULL));

    for (int i = 0; i < N; i++)
    {
        
        arr[i] = (rand()% 100) + 1;
        // printf("%d ",arr[i]);
    }

#pragma omp parallel 
#pragma omp for schedule(guided, 10) reduction(+ : sum)
    for (int i = 0; i < N; i++)
    {
        sum += arr[i];
    }

printf("The sum is %ld",sum);
return 0;
}
