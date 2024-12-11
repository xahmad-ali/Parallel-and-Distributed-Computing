#include <mpi.h>
#include <iostream>

int main(int argc, char *argv[]) {
    int rank, size, left, right;
    int send_value, recv_value;

    MPI_Init(&argc, &argv);                  
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);    
    MPI_Comm_size(MPI_COMM_WORLD, &size);    

    left = (rank == 0) ? size - 1 : rank - 1;   
    right = (rank + 1) % size;                   

    send_value = rank;  
    MPI_Request request[2];
    MPI_Status status[2];

    
    MPI_Isend(&send_value, 1, MPI_INT, right, 0, MPI_COMM_WORLD, &request[0]);
    MPI_Irecv(&recv_value, 1, MPI_INT, left, 0, MPI_COMM_WORLD, &request[1]);

    
    MPI_Waitall(2, request, status);

    std::cout << "Node " << rank << " received message " << recv_value 
              << " from Node " << left << std::endl;

    MPI_Finalize();  
    return 0;
}
