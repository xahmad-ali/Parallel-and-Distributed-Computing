#include <stdio.h>
#include <omp.h>

int main(){
    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}; 
    int arrL = sizeof(arr) / sizeof(arr[0]);
    int result[arrL];
    int i=0;


    #pragma omp parallel for private(i)
    for(i = 0; i < arrL; i++){
        result[i] = arr[i] * arr[i];
    }

    printf("The squares of the elements are:\n");
    for (int i = 0; i < arrL; i++) {
        printf("%d^2 = %d\n", arr[i], result[i]);
    }


return 0;
}