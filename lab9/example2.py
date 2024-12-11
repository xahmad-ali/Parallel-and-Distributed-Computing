from mpi4py import MPI

def main():
    mynode = MPI.COMM_WORLD.Get_rank()
    totalnodes = MPI.COMM_WORLD.Get_size()
    sum_val = 0

    startval = 1000 * mynode // totalnodes + 1
    endval = 1000 * (mynode + 1) // totalnodes

    for i in range(startval, endval + 1):
        sum_val += i

    if mynode != 0:
        MPI.COMM_WORLD.send(sum_val, dest=0, tag=1)
    else:
        for j in range(1, totalnodes):
            accum = MPI.COMM_WORLD.recv(source=j, tag=1)
            sum_val += accum

        print("The sum from 1 to 1000 is:", sum_val)

if __name__ == "__main__":
    main()
    MPI.Finalize()
