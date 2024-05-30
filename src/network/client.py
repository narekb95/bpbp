
import socket

class Client:
    def __init__(self, host, port, outbound_callback):
        self.port = port
        self.host = host
        self.outbound_callback = outbound_callback
        self.start()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        self.socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
        self.outbound_callback(self.socket)