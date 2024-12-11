from mpi4py import MPI
import numpy as np

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        total_data = []
        for source in range(1, size):
            data = np.empty(10, dtype='i')
            comm.Recv(data, source=source, tag=0)
            print(f"Node 0 received data from Node {source}: {data}")
            total_data.append(data)
    else:
        data_to_send = np.arange(rank * 10, (rank + 1) * 10, dtype='i')
        comm.Send(data_to_send, dest=0, tag=0)
        print(f"Node {rank} sent data: {data_to_send}")

if __name__ == "__main__":
    main()
