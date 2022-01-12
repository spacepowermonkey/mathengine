import numpy



from .arrow import Arrow, ArrowType



class Tile(object):
    _table:     str = "tiles"
    _stride:    int = 64


    def __init__(self, x, y):
        self.x = self.find_base(x)
        self.y = self.find_base(y)

        self.key = self.make_key(self.x,self.y)

        self.data = numpy.zeros((Tile._stride, Tile._stride), dtype=numpy.byte)
        self._bytes = None
        return
    

    def save(self, db):
        self._bytes = self.data.tobytes()
        db.execute(
            f"INSERT INTO {Tile._table} VALUES ({self.key}, {self._bytes}, {self.x}, {self.y})"
        )
        return
    
    @staticmethod
    def _datainit(db):
        db.execute(
            f"CREATE TABLE IF NOT EXISTS {Tile._table} (key PRIMARY KEY ON CONFLICT REPLACE, bytes, x INTEGER, y INTEGER)"
        )
        return


    @staticmethod
    def find_base(x):
        return x - (x % Tile._stride)

    @staticmethod
    def make_key(x, y):
        tile_x = Tile.find_base(x)
        tile_y = Tile.find_base(y)
        return f"tile-{tile_x:D.6}-{tile_y:D.6}"



class Image(object):

    def __init__(self):
        self._tiles = {}
        return


    def save(self, db):
        for tile in self._tiles.values():
            tile.save(db)
        return
    
    @staticmethod
    def _datainit(db):
        Tile._datainit(db)
        return
    

    def mark(self, x, y, data):
        key = Tile.make_key(x, y)
        dx = x % Tile._stride
        dy = y % Tile._stride
        
        try:
            tile = self._tiles[key]
        except KeyError:
            tile = Tile(x,y)
            self._tiles[key] = tile
        
        tile[dx,dy] = data
        return
    
    def to_arrows(self):
        arrows = []

        for tile in self._tiles:
            base_x = tile.x
            base_y = tile.y
            for x in range(Tile._stride):
                for y in range(Tile._stride):
                    if tile[x,y] == ArrowType.NONE:
                        continue
                    arrows.append(
                        Arrow(base_x + x, base_y + y, tile[x,y])
                    )

        return arrows