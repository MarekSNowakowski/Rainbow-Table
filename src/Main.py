from mpi4py import MPI


def send_data(n_processes, comm):
    data = [None] * n_processes  # Create data

    for i in range(1, n_processes):
        pass    # Split data for each process

    for i in range(len(data)):
        comm.isend(data[i], dest=i)  # Send data to worker processes

    print("Main process has sent the data")
    return NotImplemented


def calculate_hashes(comm, processId):
    request = comm.irecv(source=0)
    data = request.wait()
    print("Worker {} has received data".format(processId))
    hashData = []

    comm.isend(hashData, dest=0)

    return NotImplemented


def summarize(n_processes, comm):
    finalData = []

    for i in range(1, n_processes):
        request = comm.irecv(source=i)
        finalData.append(request.wait())    # put together hashes in chains

    print("Main process has received the calculated hashes")

    # Save results to the file and print results to the console

    return NotImplemented


def main():
    comm = MPI.COMM_WORLD
    processId = comm.Get_rank()
    n_processes = comm.Get_size()
    myHostName = MPI.Get_processor_name()

    if processId == 0:
        send_data(n_processes, comm)    # main process sends data
        summarize(n_processes, comm)    # and puts up together results
    else:
        calculate_hashes(comm, processId)          # workers calculate hashes


main()
