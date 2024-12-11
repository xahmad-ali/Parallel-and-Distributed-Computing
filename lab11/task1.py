from mpi4py import MPI

# Initialize MPI
comm = MPI.COMM_WORLD
mynode = comm.Get_rank()  
totalnodes = comm.Get_size()  

root = 0
num  = 0

if mynode == root:
    num = 9

num = comm.bcast(num, root=root)

print(f"Process {mynode} has its new value {num}\n")
