from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    print(f"Enter {size} numbers:")
    input_numbers = [int(input()) for _ in range(size)]
else:
    input_numbers = None

local_value = comm.scatter(input_numbers, root=0)

prefix_sum = comm.scan(local_value, op=MPI.SUM)

print(f"Process {rank}: local value = {local_value}, prefix sum = {prefix_sum}")
