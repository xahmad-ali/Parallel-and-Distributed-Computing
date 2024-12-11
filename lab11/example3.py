from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
mynode = comm.Get_rank()
totalnodes = comm.Get_size()

root = 0
vector = None
if mynode == root:
    vector = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype='i')
    padding_size = totalnodes - len(vector) % totalnodes if len(vector) % totalnodes != 0 else 0
    vector = np.pad(vector, (0, padding_size), mode='constant', constant_values=0)
    chunk_size = len(vector) // totalnodes
else:
    chunk_size = None

chunk_size = comm.bcast(chunk_size, root=root)
chunk = np.zeros(chunk_size, dtype='i')
comm.Scatter(vector, chunk, root=root)
partial_sum = np.sum(chunk)
total_sum = comm.reduce(partial_sum, op=MPI.SUM, root=root)

if mynode == root:
    print(f"Final sum of the vector: {total_sum}")
else:
    print(f"Process {mynode} computed partial sum: {partial_sum}")
