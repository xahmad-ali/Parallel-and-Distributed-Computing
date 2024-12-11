from mpi4py import MPI

# Initialize MPI
comm = MPI.COMM_WORLD
mynode = comm.Get_rank()  
totalnodes = comm.Get_size()  

datasize = 10  # Example size
root = 0 

databuffer = None
if mynode == root:
    databuffer = [i * 1.0 for i in range(datasize)]
else:

    databuffer = [0.0] * datasize

databuffer = comm.bcast(databuffer, root=root)

print(f"Process {mynode} received data: {databuffer}")
