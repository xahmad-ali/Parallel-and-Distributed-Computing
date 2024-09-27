#include <stdio.h>
#include <omp.h>

int main(){
    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}; 
    int arrL = sizeof(arr) / sizeof(arr[0]);
    int odd=0,even=0;

     #pragma omp parallel for shared(odd,even)
     for(int i=0; i<arrL; i++){
        if (arr[i] % 2 == 0) {
            even++;  // Each thread has its own copy of even
        } else {
            odd++;   // Each thread has its own copy of odd
        }
     }

     //atlast all the copies are combined 

     printf("Number of even numbers: %d\n", even);
     printf("Number of odd numbers: %d\n", odd);


    return 0;
}