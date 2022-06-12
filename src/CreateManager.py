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


def summarize(n_processes, comm, settings):
    finalData = []

    for i in range(1, n_processes):
        request = comm.irecv(source=i)
        data = request.wait()
        for e in data:
            finalData.append(e)  # put together hashes in chains

    print("Main process has received the calculated hashes")

    # Save results to the file and print results to the console
    print(finalData)
    save_to_file(finalData, settings)


def save_to_file(vector, settings):
    f = open("RT_C{}_D{}_L{}.txt".format(settings[0], settings[1], settings[2]), "w")
    for c in vector:
        for e in c:
            f.write(e + "\n")


def manageCreatingTable(n_processes, comm):
    C = input("Please type chain amount: ")
    D = input("Please type chain size: ")
    L = input("Please type password length: ")

    settings = [int(C), int(D), int(L)]

    send_data(n_processes, comm, settings)  # main process sends data
    summarize(n_processes, comm, settings)  # and puts up together results
