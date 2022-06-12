import string
import re


def collectAnswer(n_processes, comm):
    final_data = []
    found = False
    for i in range(1, n_processes):
        request = comm.irecv(source=i)
        final_data.append(request.wait())
    for i in range(len(final_data)):
        if final_data[i] != "":
            found = True
            print("Answer found: " + final_data[i])
    if not found:
        print("Answer not found.")


def read_table_file(file_name: string):
    file = open(file_name, "r")
    lines = file.readlines()
    start = []
    end = []
    for i, line in lines:
        if i % 2 == 0:
            start.append(line)
        else:
            end.append(line)
    return [start, end]


def manageReadingTable(n_processes, comm):
    path = input("Please provide the file path: ")
    target_hash = input("Please type the hash you are looking for: ")
    table = read_table_file(path)
    length = "".join(c for c in path.split("_")[2] if c.isdigit())
    print(length)
    data = [table[0], table[1], target_hash, int(length)]
    for i in range(1, n_processes):
        comm.isend(data, dest=i)    # this should split data so that only a part is passed
    collectAnswer(n_processes, comm)
