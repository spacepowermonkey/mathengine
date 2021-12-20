from typing import Any



class Obj(object):
    _table : str = "objs"

    def __init__(self, key : int, data : Any):
        self.key = key
        self.data = data
        return


    def save(self, db):
        with db.connection as con:
            con.execute(
                f"INSERT INTO {Obj._table} VALUES ({self.key}, {self.bytes}, {self.x}, {self.y})"
            )
        return

    @staticmethod
    def _datainit(db):
        with db.connection as con:
            con.execute(
                f"CREATE TABLE IF NOT EXISTS {Obj._table} (key PIRMARY KEY, data)"
            )
        return
