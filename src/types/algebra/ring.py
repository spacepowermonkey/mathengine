from ...model import ArrowType, Model
from .struct import Struct



class Ring(object):
    def __init__(self, model=None):
        self.model = model if model is not None else Model()

        self._set_star()

        self.elements = []
        self.pairs = {
            'plus': [],
            'mult': []
        }
        return
    
    def _set_star(self):
        self.star = self.model.Obj(None)
        self.model.Arrow(self.star.idx, self.star.idx, ArrowType.equality)
        return


    def element(self, data=None):
        x = self.model.Obj(data)
        self.elements.append(x)
        self.model.Arrow(x.idx, x.idx, ArrowType.equality)
        self.model.Arrow(self.star.idx, x.idx, ArrowType.equivalence)
        self.model.Arrow(x.idx, self.star.idx, ArrowType.equivalence)
        return x
    
    def pair(self, data=None):
        xy = self.model.Obj(data)
        self.model.Arrow(xy.idx, xy.idx, ArrowType.equality)
        return xy



def make_n_cyclic(n):
    cyclic_ring = Ring()

    for i in range(n):
        cyclic_ring.element(i)

    Struct.build_op(cyclic_ring, lambda a, b: (a.data + b.data) % n, 'plus')
    Struct.build_op(cyclic_ring, lambda a, b: (a.data * b.data) % n, 'mult')

    
    Struct.build_levels(cyclic_ring, lambda a, b: a.data == b.data)
    
    return cyclic_ring
