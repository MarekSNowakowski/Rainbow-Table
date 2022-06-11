import string

from mpi4py import MPI
from Cryptodome.Hash import SHA256


def send_data(n_processes, comm, info):
    data = [None] * n_processes  # Create data
    C = info[0]

    for i in range(1, n_processes):
        start = (i-1) * C // (n_processes - 1)
        end = i * C // (n_processes - 1)
        if i == n_processes:
            end = C
        data[i] = [start, end, info[1], info[2]]  # Split data for each process

    for i in range(len(data)):
        comm.isend(data[i], dest=i)  # Send data to worker processes

    print("Main process has sent the data")
    return NotImplemented


def calculate_hashes(comm, process_id):
    request = comm.irecv(source=0)
    data = request.wait()
    print("Worker {} has received data".format(process_id))
    table = []
    start = data[0]
    end = data[1]
    d = data[2]
    length = data[3]

    for s in range(start, end):
        first = gen_pwd(s, length)
        pwd = first

        for i in range(0, d):
            h = SHA256.SHA256Hash(bytes(pwd, 'utf-8')).hexdigest()
            pwd = gen_pwd(int(h, 16), length)
        print([first, pwd])
        table.append([first, pwd])
    comm.isend(table, dest=0)


def summarize(n_processes, comm):
    finalData = []

    for i in range(1, n_processes):
        request = comm.irecv(source=i)
        finalData.append(request.wait())  # put together hashes in chains

    print("Main process has received the calculated hashes")

    print(finalData)

    # Save results to the file and print results to the console


def save_to_file(vector):
    print(vector)


chars = string.ascii_letters + string.digits + "!@#$%^&*()?-+=_"
chars_len = len(chars)  # 77


def gen_pwd(num: float, length: int):
    pwd = ""
    while len(pwd) < length:
        pwd = pwd + chars[int(num % float(chars_len))]
        num = num // float(chars_len)
    return pwd


def main():
    comm = MPI.COMM_WORLD
    process_id = comm.Get_rank()
    n_processes = comm.Get_size()
    my_host_name = MPI.Get_processor_name()

    if process_id == 0:
        C = input("Please type chain amount: ")
        D = input("Please type chain size: ")
        L = input("Please type password length: ")

        send_data(n_processes, comm, [int(C), int(D), int(L)])  # main process sends data
        summarize(n_processes, comm)  # and puts up together results
    else:
        calculate_hashes(comm, process_id)  # workers calculate hashes


main()
