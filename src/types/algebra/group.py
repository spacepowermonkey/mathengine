from ...model import ArrowType, Model
from .struct import Struct



class Group(object):
    def __init__(self, model=None):
        self.model = model if model is not None else Model()

        self._set_star()

        self.elements = []
        self.pairs = []
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
        self.pairs.append(xy)
        self.model.Arrow(xy.idx, xy.idx, ArrowType.equality)
        return xy
    

    def __mul__(self, other):
        prod_group = Group()
        
        m = len(self.elements)
        n = len(other.elements)
        k = m*n

        for i in range(k):
            prod_group.element(i)
        
        def prod_op(a, b):
            a_1 = a.data // n
            a_2 = a.data % n

            b_1 = b.data // n
            b_2 = b.data % n

            c_1 = self.model.get(1 + m + m*a_1 + b_1).data.data
            c_2 = other.model.get(1 + n + n*a_2 + b_2).data.data

            c = n * c_1 + c_2

            return c

        Struct.build_op(prod_group, prod_op)

        Struct.build_levels(prod_group, lambda a, b: a.data == b.data )

        return prod_group



def make_n_cyclic(n):
    cyclic_group = Group()

    for i in range(n):
        cyclic_group.element(i)

    Struct.build_op(cyclic_group, lambda a, b: (a.data + b.data) % n)
    
    Struct.build_levels(cyclic_group, lambda a, b: a.data == b.data)
    
    return cyclic_group
