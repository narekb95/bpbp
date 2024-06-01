import p2p.btc_prtocols as protocols
from p2p.peer import Peer
from network.connman import Connman
from network.parameters import DEFAULT_HOST, DEFAULT_PORT, MAX_INBOUND

from sys import argv

def get_option(option):
    op = next((arg for arg in argv if arg.startswith(f'--{option}=')), None)
    return op.split('=')[1] if op else None

def load_options(file):
    host = get_option('host') or DEFAULT_HOST
    port = int(get_option('port') or DEFAULT_PORT)
    max_inbound = int(get_option('max_inbound') or MAX_INBOUND)
    # outbound_ips = ['88.99.136.167']

    # if port is not specified in the outbound_ips, use the default port
    def get_ip_as_obj(ip):
        ip_list = ip.split(':')
        if(len(ip_list) == 1):
            ip_list.append(port)
        else:
            ip_list[1] = int(ip_list[1])
        return (ip_list[0], ip_list[1])
    
    outbound_ips = (get_option('outbound_ips') or '').split(',')
    outbound_ips = map(get_ip_as_obj, outbound_ips)
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