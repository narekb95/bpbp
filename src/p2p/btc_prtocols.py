import struct
import time
from crypto import sha256d


# CompactSize Unsigned Integer
def encode_var_int(value):
    if value < 0xfd:
        return struct.pack('<B', value)
    elif value <= 0xffff:
        return struct.pack('<BH', 0xfd, value)
    elif value <= 0xffffffff:
        return struct.pack('<BI', 0xfe, value)
    else:
        return struct.pack('<BQ', 0xff, value)
    
def encode_var_str(s):
    length = len(s)
    return struct.pack(f'<B{length}s', length, s)


def decode_var_int(data):
    first_byte = data[0]
    if first_byte < 0xfd:
        return struct.unpack('<B', data)[0], data[1:]
    elif first_byte == 0xfd:
        return struct.unpack('<H', data[1:3])[0], data[3:]
    elif first_byte == 0xfe:
        return struct.unpack('<I', data[1:5])[0], data[5:]
    else:
        return struct.unpack('<Q', data[1:9])[0], data[9:]

def version_payload():
    version = 70015
    services = 0
    timestamp = int(time.time())
    addr_recv_services = 0
    addr_recv_ip = b'\x00' * 16
    addr_recv_port = 8333
    addr_trans_services = 0
    addr_trans_ip = b'\x00' * 16
    addr_trans_port = 8333
    nonce = 0
    user_agent = b'/mybitcoinclient:0.1.0/'
    user_agent_bytes = encode_var_str(user_agent)
    start_height = 0
    relay = 1
    payload = struct.pack(
        '<iQQ26s26sQ',
        version,
        services,
        timestamp,
        struct.pack('>Q16sH', addr_recv_services, addr_recv_ip, addr_recv_port),
        struct.pack('>Q16sH', addr_trans_services, addr_trans_ip, addr_trans_port),
        nonce,
    ) + user_agent_bytes + struct.pack('<Ib', start_height, relay)
    return payload

def getheaders_payload(block_locator_hashes=[], hash_stop= b'\x00' * 32):
    version = 70015
    payload = struct.pack('<i', version)  # version
    payload += encode_var_int(len(block_locator_hashes))  # hash count
    for hash in block_locator_hashes:
        payload += hash[::-1]  # block locator hashes (reversed)
    payload += hash_stop[::-1]  # hash_stop (reversed)
    return payload


# [TODO]
def inv_payload(inventory):
    return
    payload = encode_var_int(len(inventory))  # count
    for inv_type, inv_hash in inventory:
        payload += struct.pack('<I', inv_type)  # type
        payload += inv_hash[::-1]  # hash (reversed)
    return payload
    


def create_msg(command, payload, peer):
    magic = b'\xf9\xbe\xb4\xd9'  # Mainnet magic bytes
    command = command.ljust(12, b'\x00')
    length = struct.pack('<I', len(payload))
    checksum = sha256d(payload)[:4]
    message = magic + command + length + checksum + payload
    return message

def create_version_msg(peer):
    payload = version_payload()
    return create_msg(b'version', payload, peer)

def create_getheaders_msg(peer, block_locator_hashes=[], hash_stop= b'\x00' * 32):
    return create_msg(b'getheaders', getheaders_payload(block_locator_hashes, hash_stop), peer)

def create_verack_msg(peer):
    return create_msg(b'verack', b'', peer)
    pass

def create_ping_msg(peer):
    pass

def create_pong_msg(peer):
    pass

def post_handshake(peer, send):
    headers = create_getheaders_msg(peer)
    print('sneding getheaders request')
    send(headers, peer.socket)

def handle_version_msg(payload, peer, send):
    peer.version_rec = True
    send(create_verack_msg(peer), peer.socket)
    if peer.verack_rec:
        peer.finished_handshake = True
        post_handshake(peer, send)

def handle_verack_msg(payload, peer, send):
    peer.verack_rec = True
    if peer.version_rec:
        peer.finished_handshake = True
        post_handshake(peer, send)

# [TODO]
def handle_ping_msg(payload, peer, send):
    return
    if not peer.finished_handshake:
        return
    print('sending pong')
    send(create_pong_msg(peer), peer.socket)

def handle_pong_msg(payload, peer, send):
    peer.last_pong = time.time()
    peer.round_trip = peer.last_pong - peer.last_ping

# [TODO]
def decode_nbits(nbits):
    exponent = nbits >> 24
    coefficient = nbits & 0xffffff
    target = coefficient * (256 ** (exponent - 3))
    return target

# [TODO]
def check_header_meets_target(header, nbits):
    return
    block_hash = sha256d(header[::-1])  
    print(block_hash.hex())
    target = decode_nbits(nbits)
    print(target)
    hash_int = int.from_bytes(block_hash, byteorder='big')
    return hash_int <= target

def decode_block_header(data):
    [version, previous_block_hash, merkle_root, timestamp, bits, nonce] = struct.unpack('<I32s32sIII', data)
    header = {
        'version': version,
        'previous_block_hash': previous_block_hash.hex(),
        'merkle_root': merkle_root.hex(),
        'timestamp': timestamp,
        'nbits': bits,
        'nonce': nonce,
        'block_hash': sha256d(data[:80:-1]).hex()
    }
    return header, data[81:]
    
def decode_headers_msg(payload):
    headers = []
    count, payload = decode_var_int(payload)
    for _ in range(count):
        header, payload = decode_block_header(payload)
        headers.append(decode_block_header(header))
    return headers


def handle_headers_message(payload, peer, send):
    headers = decode_headers_msg(payload)
    print(len(headers))
    return headers

