
from hashlib import sha256

def sha256d(data):
    return sha256(sha256(data).digest()).digest()