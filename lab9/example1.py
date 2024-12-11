from mpi4py import MPI

def calculate_sum(rank, size, n):
    locals_sum = 0
    for i in range(rank, n, size):
        locals_sum += 2.5
    return locals_sum

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    n = 1000

    local_sum = calculate_sum(rank, size, n)
    total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

    if rank == 0:
        print("Total sum:",total_sum )

if __name__ == "__main__":
    main()
