from ReadHash import find_hash_in_table


def manageReadingTable(n_processes, comm):
    path = input("Please provide the file path: ")
    pwd = input("Please type the hash you are looking for: ")
    find_hash_in_table(path, pwd)
