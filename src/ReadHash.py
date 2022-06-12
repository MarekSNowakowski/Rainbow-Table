from Cryptodome.Hash import SHA256
from src.RainbowTable import gen_pwd


def findHashInTable(comm):
    request = comm.irecv(source=0)
    data = request.wait()
    answer = calculateHashInTable(data[0], data[1], data[2], data[3])
    comm.isend(answer, dest=0)


def calculateHashInTable(table_column_start, table_column_end, target_hash, length):
    for i in range(999, -1, -1):
        string = ""
        working_hash = target_hash
        index = -1
        for j in range(i, 1000):
            string = hash_to_pwd(working_hash, length, j)
            working_hash = SHA256.SHA256Hash(bytes(string, 'utf-8')).hexdigest()
        if string in table_column_end:
            index = table_column_end.index(string)
        if index != -1:
            string = table_column_start[index]
            for k in range(0, 1000):
                working_hash = SHA256.SHA256Hash(bytes(string, 'utf-8')).hexdigest()
                if working_hash == target_hash:
                    return string
                string = hash_to_pwd(working_hash, length, k)
    return ""


def hash_to_pwd(h, length, index):
    return gen_pwd(int(h, 16) + index, length)
