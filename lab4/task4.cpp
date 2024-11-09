#include <stdio.h>
#include <omp.h>


long long factorial(int num){
    if(num <= 1){
        return 1;
    }
    return num * factorial(num-1);
}


void fibonacci(int fibnum) {
    int first = 0, second = 1, next;
    
    printf("The fibonacci series of %d is :",fibnum);

    for(int i = 0; i < fibnum; i++) {
        if (i <= 1) {
            next = i;  // First two numbers are 0 and 1
        } else {
            next = first + second;
            first = second;
            second = next;
        }
        printf("%d  ", next);
    }
}




int main(){
    int num=20;
    long long fac=0;
    int fibnum=10;
    

     #pragma omp parallel
    {
         #pragma omp sections
         {
            #pragma omp section
            {
                fibonacci(fibnum);
            }

            #pragma omp section
            {
                fac = factorial(num);
                printf("The factorial of %d is %lld \n",num,fac);
            }
         }
    }


    return 0;
}

// #pragma omp sections
//         {
//             #pragma omp section
//             {
//                 fac = factorial(num);
//                 printf("The factorial of %d is %lld \n",num,fac);
//             }

//              #pragma omp section
//             {
//                 fibonacci(fibnum);
//             }
        
//         }