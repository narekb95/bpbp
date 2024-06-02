from database.db_man import SQLITE_DB

class DB:
    def __init__(self, db_data):
        self.db_man = SQLITE_DB(db_data)
    
    def fetch_all_headers(self):
        headers = self.db_man.find('headers',{})
        return headers    