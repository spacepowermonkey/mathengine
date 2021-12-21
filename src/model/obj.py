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
    def _datainit(db):
        db.execute(
            f"CREATE TABLE IF NOT EXISTS {Obj._table} (key PIRMARY KEY ON CONFLICT REPLACE, data)"
        )
        return
