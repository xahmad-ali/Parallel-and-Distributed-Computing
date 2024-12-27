from mpi4py import MPI

# Initialize the MPI environment
comm = MPI.COMM_WORLD

# Get the total number of processes and the rank of the current process
totalnodes = comm.Get_size()
mynode = comm.Get_rank()

# Variables
sum_local = 0   # Local sum for each process
sum_global = 0  # Global sum (only valid at root)
start = mynode + 1
step = totalnodes

# Calculate partial sum on each process
for i in range(start, 1001, step):  # Process-specific ranges
    sum_local += i

# Gather the sums at the root process (rank 0)
if mynode == 0:
    sum_global = sum_local
    for j in range(1, totalnodes):
        sum_from_process = comm.recv(source=j, tag=1)
        sum_global += sum_from_process

    # Print the final result at the root process
    print(f"The sum from 1 to 1000 is: {sum_global}")
else:
    # Send the local sum to the root process
    comm.send(sum_local, dest=0, tag=1)

# Finalize the MPI environment
MPI.Finalize()
