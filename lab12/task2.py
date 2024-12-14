from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:  # Master process
    messages = ["Hello from Master"] * 2
    requests = []
    for i in range(1, 3):  # Sending messages to ranks 1 and 2
        message = messages[i - 1].encode('utf-8')  # Encode string to bytes
        req = comm.Isend([message, MPI.CHAR], dest=i, tag=i)
        requests.append(req)
    MPI.Request.Waitall(requests)
    print("Master: All messages sent!")
else:  # Worker processes
    data = bytearray(20)  # Allocate buffer for received data
    comm.Recv([data, MPI.CHAR], source=0, tag=rank)
    print(f"Worker {rank}: Received message '{data.decode('utf-8').strip()}'")



