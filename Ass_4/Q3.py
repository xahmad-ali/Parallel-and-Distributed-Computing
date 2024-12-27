from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
if rank == 0:
    n_intervals = int(input("Enter the number of intervals: "))
else:
    n_intervals = None
n_intervals = comm.bcast(n_intervals, root=0)

h = 1.0 / n_intervals  
local_sum = 0.0

for i in range(rank, n_intervals, size):
    x = -0.5 + i * h 
    midpoint = x + h / 2 
    local_sum += 4.0 / (1.0 + midpoint * midpoint) * h


total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

# Root process outputs the result
if rank == 0:
    print(f"Calculated value of PI: {total_sum}")
