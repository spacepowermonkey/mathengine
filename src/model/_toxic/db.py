import sqlite3 as sql



class DB(object):
    def __init__(self, filename):
        self.filename = filename
        self.connection = sql.connect(self.filename)
        return
    
    def execute(self, statement, fetch=False):
        with self.connection.cursor() as cur:
            cur.execute(
                statement
            )
            if fetch:
                return cur.fetchall()
        return
