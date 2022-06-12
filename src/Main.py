from mpi4py import MPI

from RainbowTable import calculate_hashes
from ReadHash import find_hash_in_table
from src.CreateManager import manageCreatingTable
from src.ReadManager import manageReadingTable


def main():
    comm = MPI.COMM_WORLD
    process_id = comm.Get_rank()
    n_processes = comm.Get_size()
    my_host_name = MPI.Get_processor_name()

    if process_id == 0:
        ans = input("Do you wish to create a new rainbow table [C] or search an existing one [R]?")
        comm.isend(ans)
        if ans == 'C':
            manageCreatingTable(n_processes, comm)
        elif ans == 'R':
            manageReadingTable(n_processes, comm)

    if process_id != 0:
        mode = comm.irecv()
        if mode == 'C':
            calculate_hashes(comm, process_id)  # workers calculate hashes
        elif mode == 'R':
            find_hash_in_table()
        else:
            exit()


main()
