#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <time.h>

#define N 1000

int main(){

    int arr[N]={0};
    int long sum =0;
    

    srand(time(NULL));

    for(int i=0;i<N;i++){
        arr[i] = (rand()% 100)+1;
    }

    int a=0;
    int max=0;

    #pragma omp parallel 
    {
        #pragma omp for schedule(guided,10) reduction(max :max ) reduction(+ : sum)
        for(a=0; a<N; a++){
            sum += arr[a];
            if(max < arr[a]){
                max = arr[a];
                printf("%d\n",max);
            }
        }
    }


    printf("Maxmium value is %d \n",max);
    printf("sum value is %d \n",sum);

    
   
        // #pragma omp parallel for schedule(static,5)
        // for (int i = 0; i < 100; i++)
        // {
        //     arr[i]=a++;
        //     printf("thread %d is writing %d \n",omp_get_thread_num(),a);
        // }
            
    
    // for (int i = 0; i < n; i++)
    // {
    //     printf("%d \n", arr[i]);
    
    // }
    

    return 0;
}