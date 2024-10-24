#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

int main(){

    int m, n;
    // Take input for matrix dimensions
    printf("Enter number of rows (m): ");
    scanf("%d", &m);
    printf("Enter number of columns (n): ");
    scanf("%d", &n);

    int matrix[m][n] = {0};

    srand(time(0));
    for (int i=0; i<m; i++) {
        for (int j = 0; j < n; j++) {
            matrix[i][j] = rand() % 100;
        }
    }

    for(int i=0; i<m; i++){
        for(int j=0; j<n; j++){
            printf(" %d",matrix[i][j]);
        }
        printf("\n");
    }

    int totalEven = 0;
    int totalSum = 0;

    #pragma omp parallel for shared(totalEven, totalSum)
    for(int i=0; i<m; i++){
        int localEven = 0;
        int localSum = 0;
        for(int j=0; j<n ; j++){
            int a = matrix[i][j];
            if(a%2 == 0){
                localEven++;
            }

            localSum += matrix[i][j];
        }

        // Update shared variables using critical section for mutual exclusion
        #pragma omp critical
        {
            totalEven += localEven;
            totalSum += localSum;
        }
    }

    printf("Total number of even numbers in matrix is  %d\n",totalEven);
    printf("Total sum numbers in matrix is  %d",totalSum);



    return 0;
}