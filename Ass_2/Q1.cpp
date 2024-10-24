#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

int main() {
    int i = 0, istart = 0, iend = 10;
    int a[10], b[10];

    // Seed the random number generator
    srand(time(0));
    for (i = istart; i < iend; i++) {
        a[i] = rand() % 100; // Random values between 0 and 99
        b[i] = rand() % 100; // Random values between 0 and 99
    }

    printf("Initial values of a and b:\n");
    for (i = istart; i < iend; i++) {
        printf("a[%d] = %d, b[%d] = %d\n", i, a[i], i, b[i]);
    }

    #pragma omp parallel for
    for (i = istart; i < iend; i++) {
        a[i] = a[i] + b[i];
    }

    printf("\nValues of a after parallel addition:\n");
    for (i = istart; i < iend; i++) {
        printf("a[%d] = %d\n", i, a[i]);
    }

    return 0;
}
