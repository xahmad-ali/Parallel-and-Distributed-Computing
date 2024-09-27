#include <stdio.h>
#include <omp.h>
# define N 5

int main(){
    int arr1[N]={1,2,3,4,5};
    int arr2[N]={2,2,2,2,2};
    int arrSum[N];
    int i=0;

     #pragma omp for nowait
     for(i=0; i<N; i++){
        arrSum[i]=arr1[i]+arr2[i];
     }

      printf("The sum of the two arrays is:\n");
    for (int i = 0; i < N; i++) {
        printf("%d + %d = %d\n", arr1[i], arr2[i], arrSum[i]);
    }

    return 0;
}