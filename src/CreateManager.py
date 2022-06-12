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


def summarize(n_processes, comm):
    finalData = []

    for i in range(1, n_processes):
        request = comm.irecv(source=i)
        finalData.append(request.wait())  # put together hashes in chains

    print("Main process has received the calculated hashes")

    # Save results to the file and print results to the console
    print(finalData)
    save_to_file(finalData)


def save_to_file(vector):
    f = open("rainbow_table.txt", "w")
    f.writeLines(vector)


def manageCreatingTable(n_processes, comm):
    C = input("Please type chain amount: ")
    D = input("Please type chain size: ")
    L = input("Please type password length: ")

    send_data(n_processes, comm, [int(C), int(D), int(L)])  # main process sends data
    summarize(n_processes, comm)  # and puts up together results
