import time
import socket
import threading

class Server:
    def __init__(self, host, port, client_callback, accept_inbound_callback):
        self.port = port
        self.host = host
        self.client_callback = client_callback
        self.accept_inbound_callback = accept_inbound_callback
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

    def start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Server listening on {self.host}:{self.port}")
        
        while True:
            if not self.accept_inbound_callback():
                time.sleep(1)
                continue
            client_socket, client_address = self.socket.accept()
            self.client_callback(client_socket, client_address)

if __name__ == "__main__":
    server = Server()