class Header:
    def __init__(self, version, previous_hash, merkle_root, timestamp, bits, nonce, hash, height = None, id = None, prev_id = None):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.hash = hash
        self.height = height
        self.id = id
        self.prev_id = prev_id

class Blockchain:
    def __init__(self, headers = None):
        if headers == None:
            self.headers = {}
        else:
            self.headers = headers