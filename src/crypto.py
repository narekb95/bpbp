
from hashlib import sha256

def sha256d(data):
    return sha256(sha256(data).digest()).digest()

def parse_hash(hash):
    b_arr =  bytearray.fromhex(hash[2:])
    b_arr.reverse()
    return bytes(b_arr)