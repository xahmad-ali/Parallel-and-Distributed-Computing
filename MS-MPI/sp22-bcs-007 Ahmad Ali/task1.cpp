#include <iostream>
#include <mpi.h>

int main(int argc, char** argv) {
    int mynode, totalnodes;
    int datasize;              // Number of data units to be sent/received
    int sender = 2;            // Process number of the sending process
    int receiver = 4;          // Process number of the receiving process
    int tag;                   // Integer message tag
    MPI_Status status;         // Variable to contain status information

    // Initialize MPI environment
    MPI_Init(&argc, &argv);

    // Get the total number of processes and the rank of the current process
    MPI_Comm_size(MPI_COMM_WORLD, &totalnodes);
    MPI_Comm_rank(MPI_COMM_WORLD, &mynode);

    // Allocate memory for the data buffer
    double* databuffer = new double[datasize];

    // Sender process: Send data
    if (mynode == sender) {
        MPI_Send(databuffer, datasize, MPI_DOUBLE, receiver, tag, MPI_COMM_WORLD);
    }

    // Receiver process: Receive data
    if (mynode == receiver) {
        MPI_Recv(databuffer, datasize, MPI_DOUBLE, sender, tag, MPI_COMM_WORLD, &status);
    }

    // Finalize the MPI environment
    MPI_Finalize();

    // Clean up the allocated memory
    delete[] databuffer;

    return 0;
}