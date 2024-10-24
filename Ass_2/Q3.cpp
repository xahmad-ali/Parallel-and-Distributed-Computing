#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(){

    omp_set_num_threads(4);
    #pragma omp parallel
    {
        int Id = omp_get_thread_num();
        printf("hello(%d)",Id);
        printf("world(%d)\n",Id);
    }
}