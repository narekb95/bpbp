import sqlite3
class DBMan:
    def __init__(self):
        pass
    def insert(self, table, data):
        pass
    def find(self, table, data):
        pass
    def delete(self, table, data):
        pass

class SQLITE_DB(DBMan):
    def __init__(self, db_data):
        name, tables = db_data['name'], db_data['tables']
        self.conn = sqlite3.connect(f'{name}.db')
        self.cur = self.conn.cursor()
        for table in tables:
            self.createTableIfNotExists(table)
        
    def createTableIfNotExists(self, table):
        table_name = table['name']
        keys = table['keys']
        data = ', '.join([f"{key['name']} {key['type']}" for key in keys])
        command = f'CREATE TABLE IF NOT EXISTS {table_name} ({data})'
        self.cur.execute(command)


    def insert(self, table, data):
        keys = ', '.join(data.keys())
        values = ', '.join(data.values())
        self.cur.execute(f'INSERT INTO {table} ({keys}) VALUES ({values})')

    def find(self, table, data):
        keys = ', '.join(data.keys())
        values = ', '.join(data.values())
        self.cur.execute(f'SELECT * FROM {table} WHERE {keys}={values}')
        return self.cur.fetchall()
    
