class Header:
    def __init__(self, version, previous_hash, merkle_root, timestamp, nbits, nonce, hash, index = None):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.nbits = nbits
        self.nonce = nonce
        self.hash = hash
        self.index = index

    def __str__(self):
        if self.index:
            return f'Block {self.hash}, index {self.index}, previous hash {self.previous_hash}, timestamp {self.timestamp}'
        else:
            return f'Block {self.hash}, previous hash {self.previous_hash}, timestamp {self.timestamp}, no index assigned'