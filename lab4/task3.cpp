#include <stdio.h>
#include <omp.h>

void funcA(){
    printf("In function A : This section is being exected by thread %d\n",omp_get_thread_num());
}
void funcB(){
    printf("In function A : This section is being exected by thread %d\n",omp_get_thread_num());
}


int main(){

    #pragma omp parallel
    {
        #pragma omp sections
        {
            #pragma omp section
            {
                funcA();
            }
             #pragma omp section
            {
                funcB();
            }
        
        }
    }
        

    return 0;
}