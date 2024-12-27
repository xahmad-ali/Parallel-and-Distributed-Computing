from mpi4py import MPI
import numpy as np

# Initialize the MPI environment
comm = MPI.COMM_WORLD

# Get the total number of processes and the rank of the current process
totalnodes = comm.Get_size()
mynode = comm.Get_rank()

# Configuration
datasize = 100                  # Number of data units to be sent/received
sender = 0                      # Updated sender process number
receiver = 2                    # Updated receiver process number
tag = 0                         # Message tag

# Allocate memory for the data buffer
databuffer = np.zeros(datasize, dtype='d')  # Double precision float array

print(f"Process {mynode} started.")

# Sender process: Send data
if mynode == sender:
    print(f"Process {sender} is sending data to process {receiver}.")
    comm.Send([databuffer, MPI.DOUBLE], dest=receiver, tag=tag)

# Receiver process: Receive data
elif mynode == receiver:
    print(f"Process {receiver} is waiting to receive data from process {sender}.")
    comm.Recv([databuffer, MPI.DOUBLE], source=sender, tag=tag)
    print(f"Process {receiver} received data.")


# comm.Recv([datasize,MPI.DOUBLE], source= sender, tag=tag)