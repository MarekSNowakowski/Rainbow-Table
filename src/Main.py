from mpi4py import MPI

from RainbowTable import calculate_hashes
from ReadHash import findHashInTable
from CreateManager import manageCreatingTable
from ReadManager import manageReadingTable


def main():
    comm = MPI.COMM_WORLD
    process_id = comm.Get_rank()
    n_processes = comm.Get_size()
    my_host_name = MPI.Get_processor_name()

    if process_id == 0:
        ans = input("Do you wish to create a new rainbow table [C] or search an existing one [R]? ")
        for i in range(1, n_processes):
            comm.isend(ans, dest=i)
        if ans == 'C':
            manageCreatingTable(n_processes, comm)
        elif ans == 'R':
            manageReadingTable(n_processes, comm)
    else:
        request = comm.irecv(source=0)
        mode = request.wait()
        if mode == 'C':
            calculate_hashes(comm, process_id)  # workers calculate hashes
        elif mode == 'R':
            findHashInTable(comm)
        else:
            exit()


main()
