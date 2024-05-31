class Peer:
    def __init__(self, ip):
        self.ip = ip
        self.finished_handshake = False
        self.version_rec = False
        self.verack_rec = False
        self.last_ping = None
        self.last_pong = None
        self.round_trip = None