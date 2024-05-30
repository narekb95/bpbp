from network.connman import Connman
from network.parameters import DEFAULT_HOST, DEFAULT_PORT, MAX_INBOUND

from sys import argv

if __name__ == "__main__":
    connman = None
    if 'client' in argv:
        # connman = Connman(DEFAULT_HOST, DEFAULT_PORT, ['seed.bitcoin.sipa.be'], MAX_INBOUND, True)
        connman = Connman(DEFAULT_HOST, DEFAULT_PORT, ['88.99.136.167'], MAX_INBOUND, True)
    else:
        connman = Connman(DEFAULT_HOST, DEFAULT_PORT, [], MAX_INBOUND)