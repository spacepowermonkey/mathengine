from typing import Any



class Obj(object):
    _table : str = "objs"

    def __init__(self, key : int, data : Any):
        self.key = key
        self.data = data
        return


    def save(self, db):
        db.execute(
            f"INSERT INTO {Obj._table} VALUES ({self.key}, {self.data})"
        )
        return
    
    @staticmethod
    def getall(db):
        objs = []

        rows = db.execute(
            f"SELECT * FROM {Obj._table}", fetch=True
        )
        for row in rows:
            objs.append(Obj(row[0], row[1]))

        return objs


    @staticmethod
    def _datainit(db):
        db.execute(
            f"CREATE TABLE IF NOT EXISTS {Obj._table} (key PRIMARY KEY ON CONFLICT REPLACE, data)"
        )
        return
