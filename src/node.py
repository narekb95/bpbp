import p2p.btc_prtocols as protocols
from p2p.peer import Peer
from network.connman import Connman
from network.parameters import DEFAULT_HOST, DEFAULT_PORT, MAX_INBOUND

from sys import argv

def load_options(file):
    outbound_ips = ['88.99.136.167']
    max_inbound = 10
    client_only = ('client' in argv)
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    return [outbound_ips, max_inbound, client_only, host, port]

class Node:
    def __init__(self, file):
        [self.outbound_ips, self.max_inbound, self.client_only, self.host, self.port] = load_options(file)
        self.connman = Connman(self.host, self.port, self.outbound_ips, self.max_inbound, self.client_only)
        self.peers = []
    
    def handle_command(self, command, ip, reply):
        peer = next(peer for peer in self.peers if peer.ip == ip)
        handler_name = 'handle_' + command + '_msg'
        if hasattr(protocols, handler_name):
            handler =  getattr(protocols, handler_name)
        else:
            raise ValueError(f"Unknown command {command}")
        handler(peer, reply)

    def on_connect(self, ip, send):
        self.peers.append(Peer(ip))
        send(protocols.create_version_msg(self.peers[-1]))


if __name__ == "__main__":
    node = Node(argv[1])