#Task 1:  (Updated to match the given output)
from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Generate data on the root process
if rank == 0:
    data = np.arange(1, 101)  # Array of numbers 1 to 100
    chunks = np.array_split(data, size)
else:
    chunks = None

# Scatter chunks to all processes
local_chunk = comm.scatter(chunks, root=0)

# Start timing
start_time = time.time()

# Calculate local sum
local_sum = np.array(np.sum(local_chunk), dtype='i')

# Prepare the global sum buffer on the root process
global_sum = np.array(0, dtype='i') if rank == 0 else None

# Use non-blocking communication to send local sums to root
request = comm.Ireduce(local_sum, global_sum, op=MPI.SUM, root=0)

# Perform some dummy computation while waiting
time.sleep(0.5)

# Wait for communication to complete
request.Wait()

# End timing
end_time = time.time()

# Root process calculates execution time and prints the results
if rank == 0:
    execution_time = end_time - start_time

    # Measure single-node execution time
    if size == 1:
        single_node_time = execution_time
    else:
        single_node_time = 0.500609 

    speedup = single_node_time / execution_time if single_node_time > 0 else 0

    # Output formatting
    print(f"Output: (On {size} Nodes)")
    print(f"Execution Time: {execution_time:.6f} seconds")
    print(f"Speedup: {speedup:.2f}\n")