import p2p.btc_prtocols as protocols
from p2p.peer import Peer
from network.connman import Connman
from network.parameters import DEFAULT_HOST, DEFAULT_PORT, MAX_INBOUND

from sys import argv

def load_options(file):
    outbound_ips = ['88.99.136.167']
    max_inbound = 10
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    return [outbound_ips, max_inbound, host, port]

class Node:
    def __init__(self, file = None):

        self.peers = []
        
        [self.outbound_ips, self.max_inbound, self.host, self.port] = load_options(file)

        self.connman = Connman(
            self.host,
            self.port,
            self.outbound_ips,
            self.max_inbound,
            self.on_connect,
            self.handle_command)
        
    
    def handle_command(self, command, payload, socket, send):
        peer = next(peer for peer in self.peers if peer.socket == socket)
        handler_name = 'handle_' + command + '_msg'
        if hasattr(protocols, handler_name):
            handler =  getattr(protocols, handler_name)
        else:
            raise ValueError(f"Unknown command {command}")
        handler(payload, peer, send)

    def on_connect(self, socket, ip, send):
        self.peers.append(Peer(socket, ip))
        send(protocols.create_version_msg(self.peers[-1]), self.peers[-1].socket)


if __name__ == "__main__":
    node = Node(argv[1] if len(argv) > 1 else None)