#include <stdio.h>
#include <omp.h> // Include the OpenMP library
# define N 5

int main(){

    int arr[N] = {10, 20, 10, 5, 15};
    int arrL = sizeof(arr) / sizeof(arr[0]);
    int sumArr[N] = {0};
    int i, j = 0;


    #pragma omp parallel for private(i)
    for(i=0; i<N; i++){
        for(int j=i; j>=0; j--){
            sumArr[i] += arr[j];
        }
    }

    for(int a =0; a<N; a++){
        printf("%d ",sumArr[a]);
    }


}



    
