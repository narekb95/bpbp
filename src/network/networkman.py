import struct
import hashlib


#todo move these from here
def sha256d(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def recv_message(sock):
    magic = sock.recv(4)
    if magic != b'\xf9\xbe\xb4\xd9':
        raise ValueError("Invalid magic bytes")
    command = sock.recv(12).strip(b'\x00')
    print('received command', command)
    length = struct.unpack('<I', sock.recv(4))[0]
    checksum = sock.recv(4)
    payload = sock.recv(length)
    if sha256d(payload)[:4] != checksum:
        raise ValueError("Invalid checksum")
    return command, payload

def send_message(sock, command, payload):
    magic = b'\xf9\xbe\xb4\xd9'  # Mainnet magic bytes
    command = command.ljust(12, b'\x00')
    length = struct.pack('<I', len(payload))
    checksum = sha256d(payload)[:4]
    message = magic + command + length + checksum + payload
    sock.sendall(message)

