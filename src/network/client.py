import socket
from parameters import DEFAULT_PORT, DEFAULT_HOST

class client:
    def __init__(self, host = DEFAULT_HOST, port = DEFAULT_PORT):
        self.port = port
        self.host = host
        self.start()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        self.socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
    
        try:
            while True:
                query = input("Enter query (ping, time, or exit): ").strip().lower()

                if query == 'exit':
                    print("Closing connection")
                    break
                
                self.socket.send(query.encode('utf-8'))
                response = self.socket.recv(1024).decode('utf-8')
                print(f"Received from server: {response}")
        
        except socket.error as e:
            print(f"Socket error: {e}")
        finally:
            self.socket.close()
            print("Connection closed")

if __name__ == "__main__":
    client()
