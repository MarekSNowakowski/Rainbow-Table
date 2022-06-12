from mpi4py import MPI
from Cryptodome.Hash import SHA256
from RainbowTable import calculate_hashes, gen_pwd
from ReadHash import findHashInTable, calculateHashInTable
from CreateManager import manageCreatingTable, send_data, summarize, save_to_file
from ReadManager import readTable, read_table_file
import time


path = "RT_C12_D1000_L5.txt"
target_hash = "dbdadbb0def120f144f73c040b6bdb5b0f3eba301154529b201da3766878aec7"
C = 20
D = 10000
L = 5


def parallelRead(process_id, comm, n_processes):
    if process_id != 0:
        findHashInTable(comm)
    if process_id == 0:
        start = time.time()
        readTable(path, target_hash, n_processes, comm)
        end = time.time()

        return end - start


def parallelCreate(process_id, comm, n_processes):
    if process_id != 0:
        calculate_hashes(comm, process_id)  # workers calculate hashes
    if process_id == 0:
        settings = [C, D, L]

        start = time.time()
        send_data(n_processes, comm, settings)  # main process sends data
        summarize(n_processes, comm, settings)
        end = time.time()

        return end - start


def sequentialCreate():
    start = time.time()
    table = []
    for s in range(0, C):
        first = gen_pwd(s, L)
        pwd = first

        for i in range(0, D):
            h = SHA256.SHA256Hash(bytes(pwd, 'utf-8')).hexdigest()
            pwd = gen_pwd(int(h, 16)+i, L)
        table.append([first, pwd])
    save_to_file(table, [C, D, L])
    end = time.time()

    return end - start


def sequentialRead():
    start = time.time()
    table = read_table_file(path)
    length = int("".join(c for c in path.split("_")[3] if c.isdigit()))
    chain_length = int("".join(c for c in path.split("_")[2] if c.isdigit()))
    C = int("".join(c for c in path.split("_")[1] if c.isdigit()))

    answer = calculateHashInTable(table[0], table[1], target_hash, length, chain_length)
    print("Sequential test found answer: {}".format(answer))
    end = time.time()

    return end - start


def calculateReadSpeedUp(process_id, comm, n_processes):
    if process_id == 0:
        print("Checking parallel read test time")

    parallelReadTime = parallelRead(process_id, comm, n_processes)
    if parallelReadTime is not None:
        print("Parallel read test time is: {} s".format(parallelReadTime))

    if process_id == 0:
        print("\nChecking sequential read test time")
        sequentialReadTime = sequentialRead()
        print("Sequential read test time is {} s".format(sequentialReadTime))
        print("\nCalculated speed up is {}".format((sequentialReadTime/parallelReadTime)))


def calculateCreateSpeedUp(process_id, comm, n_processes):
    if process_id == 0:
        print("Checking parallel create test time")

    parallelCreateTime = parallelCreate(process_id, comm, n_processes)
    if parallelCreateTime is not None:
        print("Parallel create test time is: {} s".format(parallelCreateTime))

    if process_id == 0:
        print("\nChecking sequential create test time")
        sequentialCreateTime = sequentialCreate()
        print("Sequential create test time is {} s".format(sequentialCreateTime))
        print("\nCalculated speed up is {}".format((sequentialCreateTime/parallelCreateTime)))


def main():
    comm = MPI.COMM_WORLD
    process_id = comm.Get_rank()
    n_processes = comm.Get_size()
    my_host_name = MPI.Get_processor_name()

    #calculateReadSpeedUp(process_id, comm, n_processes)
    calculateCreateSpeedUp(process_id, comm, n_processes)


main()
