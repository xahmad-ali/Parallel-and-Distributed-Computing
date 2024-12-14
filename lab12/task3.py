from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size < 3:
    if rank == 0:
        print("This program requires at least 3 processes.")
    exit()

if rank == 0:  # Master process
    message1 = "Message 1"
    message2 = "Message 2"

    # Non-blocking sends
    request1 = comm.isend(message1, dest=1, tag=0)
    request2 = comm.isend(message2, dest=2, tag=0)

    # Wait for any send to complete
    requests = [request1, request2]
    completed_index = MPI.Request.Waitany(requests)

    # Print which message was sent first
    print(f"Message from rank {completed_index + 1} was sent first.")

elif rank == 1 or rank == 2:  # Worker processes
    # Receive the message
    received_message = comm.recv(source=0, tag=0)

    # Print the received message
    print(f"Process {rank} received: {received_message}")
