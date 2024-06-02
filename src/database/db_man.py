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
        name = db_data['name']
        self.conn = sqlite3.connect(f'{name}.db')
        self.cur = self.conn.cursor()
        if self.is_database_empty():
            tables, initial_data = db_data['tables'], db_data['initial-data']
            for table in tables:
                table_initial_data = initial_data.get(table['name']) or []
                self.create_table(table, table_initial_data)
        

    def is_database_empty(self):
        self.cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table'")
        table_count = self.cur.fetchone()[0]
        return table_count == 0

    def create_table(self, table, initial_data):
        name = table['name']
        keys = table['keys']
        columns = ', '.join([f"{key['name']} {key['type']}" for key in keys])
        command = f'CREATE TABLE IF NOT EXISTS {name} ({columns})'
        self.cur.execute(command)
        for row in initial_data:
            self.insert(name, row)


    def insert(self, table, data):
        keys = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        values = tuple(data.values())
        insert_command = f'INSERT INTO {table} ({keys}) VALUES ({placeholders})'
        print(insert_command)
        self.cur.execute(insert_command, values)
        self.conn.commit()


    def find(self, table, data):
        keys = ', '.join(data.keys())
        values = ', '.join(data.values())
        self.cur.execute(f'SELECT * FROM {table} WHERE {keys}={values}')
        return self.cur.fetchall()
    
