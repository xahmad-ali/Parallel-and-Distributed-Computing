#include <stdio.h>
#include <omp.h>

int main(){

    #pragma omp parallel
    {
        #pragma omp sections
        {
            // section 1
            #pragma omp section
            {
                printf("Task 1 is being executed by thread : %d\n",omp_get_thread_num());
                // simulaing task1 :
            }
            // section 2
            #pragma omp section
            {
                printf("Task 2 is being executed by thread : %d\n",omp_get_thread_num());
                // simulaing task2 :
            }
            // section 3
            #pragma omp section
            {
                printf("Task 3 is being executed by thread : %d\n",omp_get_thread_num());
                // simulaing task3 :
            }
        }
    }

    return 0;
}