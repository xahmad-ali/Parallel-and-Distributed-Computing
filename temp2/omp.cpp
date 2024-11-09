#include <stdio.h>
#include <omp.h>

// void factorial(int num){
//     int i=1;
//     int result=1;

//     for(i=1; i<= num; i++){
//         result *= i;
//     }

//     printf("fact of %d is : %d\n", num,result);
// }

int main(){

     int a[2][3] = {{1, 2, 3}, {2, 3, 4}};
    int b[3][2] = {{2, 2}, {1, 1}, {3, 3}};
    int result[2][2];
    int m = 2, n = 3, p = 3, q = 2; // dimensions of matrices
    int i, j, k;
     // Initialize result matrix to 0
    for (i = 0; i < m; i++) {
        for (j = 0; j < q; j++) {
            result[i][j] = 0;
        }
    }

    #pragma omp parallel for collapse(2) private(i,j,k) shared(a,b,result)
    for(i=0; i<m; i++){
        for ( j=0; j < q; j++){
            for(k=0; k<n; k++){
                result[i][j] += a[i][k]*b[k][j];
            }
        }
    }

    for(i=0;i<m; i++){
        for(j=0; j<q; j++){
            printf(" %d",result[i][j]);
        }
        printf("\n");
    }

    


// printf("sum is : %d", sum);
    return 0;
}