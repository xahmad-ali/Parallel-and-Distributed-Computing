from mpi4py import MPI
import numpy as np

#initialize
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    vector_length = int(input("Enter the length of the vector: "))
    vector = np.arange(1, vector_length + 1)  # Example vector [1, 2, ..., vector_length]
    if vector_length % size != 0:
        raise ValueError("The vector length must be divisible by the number of processes.")
    chunk_size = vector_length // size
else:
    vector = None
    chunk_size = None

chunk_size = comm.bcast(chunk_size, root=0)

local_chunk = np.zeros(chunk_size, dtype=int)

comm.Scatter(vector, local_chunk, root=0)

partial_sum = np.sum(local_chunk)

partial_sums = None
if rank == 0:
    partial_sums = np.zeros(size, dtype=int)
comm.Gather(partial_sum, partial_sums, root=0)

if rank == 0:
    total_sum = np.sum(partial_sums)
    print(f"Vector: {vector}")
    print(f"Partial sums: {partial_sums}")
    print(f"Total sum: {total_sum}")
