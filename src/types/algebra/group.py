from ...other import ArrowType, Model



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
        self.model.Arrow(self.star.idx, x.idx, ArrowType.inclusion)
        self.model.Arrow(x.idx, self.star.idx, ArrowType.inclusion)
        return x
    
    def pair(self, data=None):
        xy = self.model.Obj(data)
        self.pairs.append(xy)
        self.model.Arrow(xy.idx, xy.idx, ArrowType.equality)
        return xy



def make_n_cyclic(n):
    cyclic_group = Group()

    for i in range(n):
        cyclic_group.element(i)

    for x in cyclic_group.elements:
        for y in cyclic_group.elements:
            z = (x.data + y.data) % n
            z = cyclic_group.elements[z]
            
            xy = cyclic_group.pair(z)

            cyclic_group.model.Arrow(x.idx, xy.idx, ArrowType.inclusion)
            cyclic_group.model.Arrow(y.idx, xy.idx, ArrowType.inclusion)
            cyclic_group.model.Arrow(xy.idx, z.idx, ArrowType.inclusion)
    
    pair_count = len(cyclic_group.pairs)
    for i in range(pair_count):
        for j in range(i, pair_count):
            if cyclic_group.pairs[i].data == cyclic_group.pairs[j].data:
                cyclic_group.model.Arrow(cyclic_group.pairs[i].idx, cyclic_group.pairs[j].idx, ArrowType.equality)
                cyclic_group.model.Arrow(cyclic_group.pairs[j].idx, cyclic_group.pairs[i].idx, ArrowType.equality)
    
    return cyclic_group
