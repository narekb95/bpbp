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

    # If port is not specified in the outbound-ips, use the default port
    def get_ip_as_obj(ip):
        ip_list = ip.split(':')
        if(len(ip_list) == 1):
            ip_list.append(port)
        else:
            ip_list[1] = int(ip_list[1])
        return (ip_list[0], ip_list[1])
    
    outbound_ips = get_option('outbound-ips')
    if outbound_ips:
        outbound_ips = outbound_ips.split(',')
        outbound_ips = map(get_ip_as_obj, outbound_ips)
    else:
        outbound_ips = []
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

        [outbound_ips, max_inbound, host, port] = load_options(param_file)
        self.connman = Connman(
            host,
            port,
            outbound_ips,
            max_inbound,
            self.on_connect,
            self.handle_command)
        
        

    
    def handle_command(self, input, socket, send):
        peer = next(peer for peer in self.peers if peer.socket == socket)
        peer.raw_data += input
        while True:
            command, peer.raw_data = protocols.parse_single_command(peer.raw_data)
            if not command:
                break
            try:
                protocols.handle_single_command(command, peer, send)
            except ValueError as e:
                print(e)
                # TODO send reject
    def on_connect(self, socket, ip, send):
        self.peers.append(Peer(socket, ip))
        print('sending version message')
        send(protocols.create_version_msg(self.peers[-1]), self.peers[-1].socket)


if __name__ == "__main__":
    parameters_path = argv[1] if len(argv) > 1 else None
    db_path = argv[2] if len(argv) > 2 else None
    node = Node(parameters_path, db_path)