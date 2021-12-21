from uuid import uuid4


from .obj import Obj
from .arrow import Arrow
from .image import Image

from ._toxic.db import DB



class Model(object):
    _suffix : str = "model"

    def __init__(self, name=None):
        self.name = name if name is not None else str(uuid4())

        self.size = 0
        self.complexity = 0

        self._data = DB(f"{self.name}.{self._suffix}")
        self._datainit(self._data)
        Obj._datainit(self._data)
        Image._datainit(self._data)

        self.image = Image()
        return


    @staticmethod
    def _datainit(db):
        return
    

    def object(self, data):
        obj = Obj(self.size, data)
        obj.save(self._data)
        self.size +=1
        return obj
    
    def arrow(self, start, end, data):
        arr = Arrow(start, end, data)
        self.image.mark(start, end, data)
        self.complexity += 1
        return arr


    def objects(self):
        return iterator
    
    def arrows(self):
        return iterator
