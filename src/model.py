from dataclasses import dataclass
from typing import Any



@dataclass
class Obj:
    idx : int
    data : Any


@dataclass
class Arrow:
    start : int
    end : int
    data : Any

@dataclass
class ArrowType:
    NONE        : int = 0
    equality    : int = 1
    inclusion   : int = 2
    restriction : int = 3
    equivalence : int = 5 # -- because it's 2+3



class Model:
    def __init__(self):
        self.size = 0
        self._objs = []

        self.complexity = 0
        self._arrows = {}
        return
    

    def Obj(self, data):
        new_obj = Obj(self.size, data)
        self._objs.append(new_obj)
        self.size += 1
        return new_obj
    
    def Arrow(self, start, end, data):
        new_arr = Arrow(start, end, data)

        try:
            current_arr = self._arrows[start][end]

            if (
                new_arr.data == ArrowType.inclusion and current_arr.data == ArrowType.restriction
            ) or (
                new_arr.data == ArrowType.restriction and current_arr.data == ArrowType.inclusion
            ) or (
                new_arr.data == ArrowType.equivalence or current_arr.data == ArrowType.equivalence
            ):
                new_arr.data = ArrowType.equivalence
            
            if current_arr.data == ArrowType.equality:
                new_arr.data = ArrowType.equality
        except KeyError:
            current_arr = None
            self.complexity += 1
        
        try:
            self._arrows[start][end] = new_arr
        except KeyError:
            self._arrows[start] = {end : new_arr}
        
        return new_arr


    def get(self, x1, x2=None):
        if x2 is None:
            return self._objs[x1]
        else:
            return self._arrows[x1][x2]


    def objects(self):
        return self._objs


    def _make_arrow_gen(self):
        for row, cols in self._arrows.items():
            for col, arrow in cols.items():
                yield arrow

    def arrows(self):
        return self._make_arrow_gen()
