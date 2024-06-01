from network.server import Server
from crypto import sha256d

# import hashlib
import time
import threading
import struct
import socket
import selectors

class Connman:
    def __init__(self, host, port, outbound_ips, max_inbound, on_connect, handle_command):
        self.max_inbound = max_inbound
        self.host = host
        self.port = port
        self.max_inbound = max_inbound
        self.on_connect = on_connect
        self.handle_command = handle_command

        self.sockets = []
        self.selector = selectors.DefaultSelector()

        self.run_server()
        
        for host in outbound_ips:
            self.connect_to_ip(host)

        try:
            while True:
                events = self.selector.select(timeout=None)
                for key, _ in events:
                    callback = key.data
                    try:
                        callback(key.fileobj)
                    except Exception as e:
                        print(f"Caught exception: {e}")

        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.selector.close()


        # self.server = Server(host, port, self.inbound_callback, self.accept_inbound_callback)
        self.sockets = []

    # the following function recieve a msg from a bitcoin node and decode it

    def run_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.server_socket.setblocking(False)
        self.selector.register(self.server_socket, selectors.EVENT_READ, self.accept_conn)

    def accept_conn(self, server_socket):
        assert(server_socket == self.server_socket)
        peer_socket, peer_ip = server_socket.accept()
        peer_socket.setblocking(False)
        self.sockets.append(peer_socket)
        self.selector.register(peer_socket, selectors.EVENT_READ, self.recv_message)
        print(f"Accepted connection from {peer_ip}")
        self.on_connect(peer_socket, peer_ip, self.send_message)


    def recv_message(self, sock):
        magic = sock.recv(4)
        if magic != b'\xf9\xbe\xb4\xd9':
            raise ValueError("Invalid magic bytes")
        command = sock.recv(12).strip(b'\x00')
        length = struct.unpack('<I', sock.recv(4))[0]
        checksum = sock.recv(4)
        payload = sock.recv(length)
        if sha256d(payload)[:4] != checksum:
            raise ValueError("Invalid checksum")
        command = command.decode('ascii')
        print(f'received {command} message')
        self.handle_command(command, payload, sock, self.send_message)


    def connect_to_ip(self, host):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        print(host)
        peer_socket.connect((host))
        peer_socket.setblocking(False)
        self.sockets.append(peer_socket)

        self.selector.register(peer_socket, selectors.EVENT_READ, self.recv_message)
        print(f"Connected to server at {self.host}:{self.port}")
        self.on_connect(peer_socket, host, self.send_message)

    # def accept_inbound_callback(self):
    #     return len(self.inbound) < self.max_inbound

    def inbound_callback(self, client_socket, client_address):
            inbound_handler = threading.Thread(
                target=self.handle_inbound, 
                args=(client_socket, client_address)
            )
            self.inbound.append((inbound_handler, client_socket, client_address))
            inbound_handler.start()

    def send_message(self, message, sock):
        sock.send(message)