from mpi4py import MPI
import numpy as np  

# Initialize MPI
comm = MPI.COMM_WORLD
mynode = comm.Get_rank()  
totalnodes = comm.Get_size()  

root = 0  
datasize = 10  


senddata = np.array([mynode + i for i in range(datasize)], dtype='i') 

recvdata = None
if mynode == root:
    recvdata = np.zeros(datasize, dtype='i')  


comm.Reduce(senddata, recvdata, op=MPI.SUM, root=root)


if mynode == root:
    print(f"Process {root} received reduced data: {recvdata}")
