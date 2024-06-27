from crypto import parse_hash

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

    def update_headers(self, headers):
        for header in headers:
            self.headers[header['hash']] = Header(header['version'], header['prev_hash'], header['merkle_root'], header['timestamp'], header['bits_difficulty'], header['nonce'], header['hash'], header['height'], header['id'], header['prev_id'])

    def __str__(self) -> str:
        return '\n'.join(map(lambda header: \
                f'Hash: {header.hash}, Height: {header.height} Timestamp: {header.timestamp}' , self.headers.values()))