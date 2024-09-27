#include <stdio.h>
#include <omp.h>
# define N 5
int main() {
    int arr[N]={1,2,3,4,5};
    int i, result = 0;  

    #pragma omp parallel for lastprivate(result)
    for(i=0; i<N; i++){
        arr[i]=arr[i]*arr[i];
        result =arr[i];

        printf("The last itreatoin result is %d of %dth itreation\n",result,i);
    }

    return 0;
}
