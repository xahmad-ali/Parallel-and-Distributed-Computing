from mpi4py import MPI

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank() 
world_size = comm.Get_size() 

array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
array_size = len(array)
chunk_size = array_size // world_size
start_index = world_rank * chunk_size
end_index = array_size if world_rank == world_size - 1 else start_index + chunk_size

partial_sum = sum(array[start_index:end_index])

print(f"Sum - Process {world_rank}:\n My contribution to the sum is {partial_sum}")


total_sum = comm.reduce(partial_sum, op=MPI.SUM, root=0)

if world_rank == 0:
    print(f"The total sum calculated by the master process is {total_sum}")
    print("Sum-Master: \nNormal end of execution.")
