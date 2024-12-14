#Example Task 1  (updated)
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define the data size and initialize variables
datasize = 100
data = None
local_sum = 0

# Start timing
start_time = MPI.Wtime()

# Root process generates the data
if rank == 0:
    data = np.arange(1, datasize + 1)  # Array of numbers 1 to 100
    chunks = np.array_split(data, size)
else:
    chunks = None

# Scatter chunks to all processes
local_chunk = comm.scatter(chunks, root=0)

# Compute local sum
local_sum = np.sum(local_chunk)

# Prepare the result variable on the root process
global_sum = np.array(0, dtype='i') if rank == 0 else None

# Use non-blocking reduce to compute the global sum
req = comm.Ireduce(np.array(local_sum, dtype='i'), global_sum, op=MPI.SUM, root=0)

# Perform some dummy computation to simulate overlap
_ = [x**2 for x in range(1000)]  # Dummy work

# Wait for non-blocking communication to complete
req.Wait()

# Stop timing
end_time = MPI.Wtime()

# Root process prints the result and execution time
if rank == 0:
    print(f"Total Sum: {global_sum}")  # No need to index
    print(f"Execution Time: {end_time - start_time} seconds")