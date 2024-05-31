from network.server import Server
from network.client import Client
import network.networkman as networkman

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
# import hashlib
import time
import threading
import struct

def encode_var_str(s):
    """Encode a variable length string (var_str)."""
    length = len(s)
    return struct.pack(f'<B{length}s', length, s)


def create_version_payload():
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

class Connman:
    def __init__(self, host, port, outbound_ips, max_inbound, client_only = False):
        self.selector = DefaultSelector()
        if not client_only:
            self.server = Server(host, port, self.inbound_callback, self.accept_inbound_callback)
        self.startOutboundConnections(outbound_ips, port)
        self.inbound = []
        self.max_inbound = max_inbound

    def startOutboundConnections(self, ips, port):
        for ip in ips:
            client = Client(ip, port, self.outbound_callback)
            self.outbound.append(client)
            
    def outbound_callback(self, socket):
        print(socket)
        try:
            # Send version message
            version_payload = create_version_payload()
            networkman.send_message(socket, b'version', version_payload)

            print('waiting for verack')
            # Receive verack message
            command, payload = networkman.recv_message(socket)
            if command == b'verack':
                print("Received verack from server")
            print('something received')
            
            # Receive version message from server
            command, payload = networkman.recv_message(socket)
            if command == b'version':
                print("Received version message from server")
                # Send verack message
                networkman.send_message(socket, b'verack', b'')
                print("Handshake complete")
            while True:
                query = input("Enter query (ping, time, or exit): ").strip().lower()
                if query == 'exit':
                    print("Closing connection")
                    break
                elif query == 'ping':
                    networkman.send_message(socket, b'ping', b'')
                    try:
                        command, payload = networkman.recv_message(socket)
                        print(f"Received {command.decode('utf-8')} message from server")
                    except socket.timeout:
                        pass
                else:
                    print("Unknown command")

        except socket.error as e:
            print(f"Socket error: {e}")
        finally:
            socket.close()
            print("Connection closed")

    def accept_inbound_callback(self):
        return len(self.inbound) < self.max_inbound

    def inbound_callback(self, client_socket, client_address):
            inbound_handler = threading.Thread(
                target=self.handle_inbound, 
                args=(client_socket, client_address)
            )
            self.inbound.append((inbound_handler, client_socket, client_address))
            inbound_handler.start()

    def handle_inbound(self, client_socket, client_address):
        print(f"Connection accepted from {client_address}")
        try:
            command, payload = networkman.recv_message(client_socket)
            if command == b'version':
                print("Received version message")
                # Send verack message
                networkman.send_message(client_socket, b'verack', b'')
                # Send version message back to client
                version_payload = struct.pack('<iQ', 70015, int(time.time()))
                networkman.send_message(client_socket, b'version', version_payload)
                # Receive verack message from client
                command, payload = networkman.recv_message(client_socket)
                if command == b'verack':
                    print("Handshake complete")
        
        except client_socket.error as e:
            print(f"Socket error with client {client_address}: {e}")
        
        finally:
            # Close the client socket
            client_socket.close()
            print(f"Connection with {client_address} closed")
