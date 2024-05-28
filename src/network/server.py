import datetime
import socket
from parameters import DEFAULT_PORT, DEFAULT_HOST

import socket
import threading

class Server:
    def __init__(self, host = DEFAULT_HOST, port = DEFAULT_PORT):
        self.port = port
        self.host = host
        self.start_server()

    def handle_client(self, client_socket, client_address):
        print(f"Connection accepted from {client_address}")
        try:
            while True:
                # Receive a message from the client
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    # If message is empty, client has closed the connection
                    print(f"Client {client_address} disconnected")
                    break
                
                print(f"Received from {client_address}: {message}")
                
                # Process the message and prepare the response
                if message.lower() == 'ping':
                    response = 'pong'
                elif message.lower() == 'time':
                    time = datetime.datetime.now()
                    response = str(int(time.timestamp()))
                else:
                    response = 'Unknown command'
                
                # Send the response back to the client
                client_socket.send(response.encode('utf-8'))
        
        except socket.error as e:
            print(f"Socket error with client {client_address}: {e}")
        
        finally:
            # Close the client socket
            client_socket.close()
            print(f"Connection with {client_address} closed")

    def start_server(self):
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

        self.socket.listen(10)
        print(f"Server listening on {self.host}:{self.port}")
        
        while True:
            # Accept a connection
            client_socket, client_address = self.socket.accept()
            
            # Handle the client connection in a new thread
            client_handler = threading.Thread(
                target=self.handle_client, 
                args=(client_socket, client_address)
            )
            client_handler.start()

if __name__ == "__main__":
    server = Server()