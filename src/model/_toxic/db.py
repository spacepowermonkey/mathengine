import sqlite3 as sql



class DB(object):
    def __init__(self, filename):
        self.filename = filename
        self.connection = sql.connect(self.filename)
        return
    
    def execute(self, statement):
        with self.connection as con:
            con.execute(
                statement
            )
        return