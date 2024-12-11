from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
########################stage2################
print(f"Process {rank}: Starting first stage of computation...")
stage1_result = rank * 2
print(f"Process {rank}: Finished first stage of computation.")

comm.Barrier()
if rank == 0:
    print("\nAll processes have reached the barrier.\n")

################stage2#################
print(f"Process {rank}: Starting second stage of computation...")
stage2_result = stage1_result + 2
print(f"Process {rank}: Finished second stage of computation.")

comm.Barrier()
if rank == 0:
    print("\nAll processes have done there tasks\n")
