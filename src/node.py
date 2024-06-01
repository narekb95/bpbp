from database.db_man import SQLITE_DB

import p2p.btc_prtocols as protocols
from p2p.peer import Peer
from network.connman import Connman

import json
from sys import argv


def load_json(file):
    f = open(file, 'r') if file else None
    return json.load(f) if f else {}

def get_option(option):
    op = next((arg for arg in argv if arg.startswith(f'--{option}=')), None)
    return op.split('=')[1] if op else None

def load_options(file):
    ops = load_json(file)

    host = get_option('host') or ops['DEFAULT_HOST']
    port = int(get_option('port') or ops['DEFAULT_PORT'])
    max_inbound = int(get_option('max_inbound') or ops['MAX_INBOUND'])

    # If port is not specified in the outbound_ips, use the default port
    def get_ip_as_obj(ip):
        ip_list = ip.split(':')
        if(len(ip_list) == 1):
            ip_list.append(port)
        else:
            ip_list[1] = int(ip_list[1])
        return (ip_list[0], ip_list[1])
    
    outbound_ips = get_option('outbound_ips')
    if outbound_ips:
        outbound_ips = (get_option('outbound_ips') or '').split(',')
        outbound_ips = map(get_ip_as_obj, outbound_ips)
    else:
        outbound_ips = []
    print(outbound_ips)
    return [outbound_ips, max_inbound, host, port]

class Node:
    def __init__(self, param_file = None, db_file = None):

        if not param_file:
            raise ValueError("No parameters file specified")
        if not db_file:
            raise ValueError("No database file specified")

        db_data = load_json(db_file)
        self.db = SQLITE_DB(db_data)

        self.peers = []

        [self.outbound_ips, self.max_inbound, self.host, self.port] = load_options(param_file)
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
        print('sending version message')
        send(protocols.create_version_msg(self.peers[-1]), self.peers[-1].socket)


if __name__ == "__main__":
    parameters_path = argv[1] if len(argv) > 1 else None
    db_path = argv[2] if len(argv) > 2 else None
    node = Node(parameters_path, db_path)