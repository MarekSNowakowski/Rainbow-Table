from Cryptodome.Hash import SHA256
from src.RainbowTable import gen_pwd


def findHashInTable(comm):
    request = comm.irecv(source=0)
    data = request.wait()
    table_part = data[0]
    hash = data[1]

    # 1.check if string you got from hash with reduction#999 is in last column (at the ends of rows)
    # 2.if not then check with reduction#998 then hash, then reduction#999
    # 3.continue in the same pattern until you go arrive at reduction#0 if you didn't find the answer, the attack failed
    # 4.if you find the answer somewhere along the way get the start of the chain where you found the hash
    # 5.remake the chain in its entirety until you find the pwd that makes the hash


def hash_to_pwd(h, length, index):
    return gen_pwd(int(h, 16) + index, length)
