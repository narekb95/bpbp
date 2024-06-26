from database.db_man import SQLITE_DB

class DB:
    def __init__(self, db_data):
        self.db_man = SQLITE_DB(db_data)
    
    def fetch_all_headers(self):
        headers = self.db_man.find('headers',{})
        return headers
    
    def write_headers(self, headers):
        for header in headers:
            SQLITE_DB.insert('headers', {
                'version': header.version,
                'height': header.height,
                'previous_hash': header.previous_hash,
                'merkle_root': header.merkle_root,
                'timestamp': header.timestamp,
                'nbits': header.nbits,
                'nonce': header.nonce,
                'hash': header.hash
            })