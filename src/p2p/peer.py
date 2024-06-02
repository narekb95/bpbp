class Peer:
    def __init__(self, socket, ip): # identified by socket not ip
        self.ip = ip
        self.socket = socket
        self.finished_handshake = False
        self.version_rec = False
        self.verack_rec = False
        self.last_ping = None
        self.last_pong = None
        self.round_trip = None
        self.raw_data = b''