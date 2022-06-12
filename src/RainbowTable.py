from Cryptodome.Hash import SHA256
import string

chars = string.ascii_letters + string.digits + "!@#$%^&*()?-+=_"
chars_len = len(chars)  # 77


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


def gen_pwd(num: float, length: int):
    pwd = ""
    while len(pwd) < length:
        pwd = pwd + chars[int(num % float(chars_len))]
        num = num // float(chars_len)
    return pwd
