import numpy

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



class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self._data = numpy.zeros((Image.STRIDE, Image.STRIDE), dtype=numpy.byte)
        return

    def __setitem__(self, key, item):
        self._data[key] = item
    
    def __getitem__(self, key):
        return self._data[key]


class Image:
    STRIDE = 64

    def __init__(self):
        self._tiles = {}
        return
    
    def mark(self, x, y, data):
        bx = x // Image.STRIDE
        by = y // Image.STRIDE

        dx = x % Image.STRIDE
        dy = y % Image.STRIDE

        try:
            tile = self._tiles[(bx,by)]
        except KeyError:
            tile = Tile(bx, by)
            self._tiles[(bx,by)] = tile
        tile[dx,dy] = data
        return
    
    def to_arrows(self):
        arrows = []
        tiles = self._tiles.values()
        for tile in tiles:
            for x in range(Image.STRIDE):
                for y in range(Image.STRIDE):
                    data = tile[x,y]
                    print(f"... ... @{x},{y} : {data}")
                    if tile[x,y] == ArrowType.NONE:
                        continue
                    arrows.append(
                        Arrow(x, y, tile[x,y])
                    )
        return arrows



class Model:
    def __init__(self):
        self.size = 0
        self._objs = []

        self.complexity = 0
        self._image = Image()
        return
    

    def Obj(self, data):
        new_obj = Obj(self.size, data)
        self._objs.append(new_obj)
        self.size += 1
        return new_obj
    
    def Arrow(self, start, end, data):
        self._image.mark(start, end, data)
        self.complexity += 1
        return Arrow(start, end, data)


    def objects(self):
        return self._objs

    def arrows(self):
        return self._image.to_arrows()
