#include <stdio.h>
#include <omp.h>


// Function to compute factorial
// void factorial(int a)
// {
//     int fac = 1;
//     for (int i = 1; i <= a; i++)
//     {
//         fac *= i;
//     }
//     printf("Factorial of %d is %d\n", a, fac);
// }

void factorial(int a){
    int fprivate = a;
    int result=1;

    for(int i=1; i<=a; i++){
        result *= i; 
    }    

    printf("Factorial of %d is %d\n", fprivate, result);
}

int main()
{
    int arr[] = {1, 2, 3, 4, 5};
    int arrL = sizeof(arr) / sizeof(arr[0]);
    int i = 0;

    #pragma omp parallel firstprivate(arr)
    for( i=0; i<arrL; i++){
        factorial(arr[i]);
    }
        

    // firstprivate(var): A private copy of var is created for each thread,
    // and each copy is initialized with the value of var from the master thread before
    // entering the parallel region.

    return 0;
}