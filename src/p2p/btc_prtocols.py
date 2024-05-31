import struct
import time
from hashlib import sha256

def sha256d(data):
    return sha256(sha256(data).digest()).digest()

def encode_var_str(s):
    length = len(s)
    return struct.pack(f'<B{length}s', length, s)

def create_version_msg_payload():
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

def create_msg(command, payload, peer):
    magic = b'\xf9\xbe\xb4\xd9'  # Mainnet magic bytes
    command = command.ljust(12, b'\x00')
    length = struct.pack('<I', len(payload))
    checksum = sha256d(payload)[:4]
    message = magic + command + length + checksum + payload
    return message

def create_version_msg(peer):
    payload = create_version_msg_payload()
    return create_msg(b'version', payload, peer)

def create_verack_msg(peer):
    return create_msg(b'verack', b'', peer)
    pass

def create_ping_msg(peer):
    pass

def create_pong_msg(peer):
    pass

def handle_version_msg(peer, send):
    peer.version_rec = True
    if peer.verack_rec:
        peer.finished_handshake = True
    send(create_verack_msg())


def handle_verack_msg(peer, send):
    if not peer.finished_handshake:
        return
    peer.verack_rec = True
    if peer.version_rec:
        peer.finished_handshake = True

def handle_ping_msg(peer, send):
    if not peer.finished_handshake:
        return
    send(create_pong_msg())

def handle_pong_msg(peer, send):
    peer.last_pong = time.time()
    peer.round_trip = peer.last_pong - peer.last_ping