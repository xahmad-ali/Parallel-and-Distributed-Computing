from mpi4py import MPI

# Initialize MPI environment
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Master process gets the number of intervals
if rank == 0:
    n_intervals = int(input("Enter the number of intervals: "))
else:
    n_intervals = None

# Broadcast the number of intervals to all processes
n_intervals = comm.bcast(n_intervals, root=0)

# Compute the integral in parallel
h = 1.0 / n_intervals  # Width of each interval
local_sum = 0.0

for i in range(rank, n_intervals, size):
    x = -0.5 + i * h  # Start point of the subinterval
    midpoint = x + h / 2  # Midpoint of the interval
    local_sum += 4.0 / (1.0 + midpoint * midpoint) * h



# Reduce all local sums to a total sum at the root process
total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

# Root process outputs the result
if rank == 0:
    print(f"Calculated value of PI: {total_sum}")
