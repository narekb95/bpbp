import selectors
import time
import socket
import threading

class Server:
    def __init__(self, host, port, client_callback, accept_inbound_callback, inbound_request_callback):
        self.port = port
        self.host = host
        self.client_callback = client_callback
        self.accept_inbound_callback = accept_inbound_callback
        self.inbound_request_callback = inbound_request_callback
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

    def start_server(self):
        self.selector = selectors.DefaultSelector()
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.server_socket.setblocking(False)
        self.selector.register(self.server_socket, selectors.EVENT_READ, lambda server_socket: self.accept(server_socket, self.selector))

        print(f"Server listening on {self.host}:{self.port}")
        
        while True:
            if not self.accept_inbound_callback():
                time.sleep(1)
                continue
            client_socket, client_address = self.socket.accept()
            self.client_callback(client_socket, client_address)
        
    def accept(self, server_socket, selector):
        assert(server_socket == self.server_socket)
        inbound_socket, inbound_address = server_socket.accept()
        inbound_socket.setblocking(False)
        selector.register(inbound_socket, selectors.EVENT_READ, lambda inbound_socket: self.read(inbound_socket, selector))
        print(f"Accepted connection from {inbound_address}")

if __name__ == "__main__":
    server = Server()