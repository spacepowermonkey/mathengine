from ...model import ArrowType, Model



class Struct:
    @staticmethod
    def build_op(struct, fn, name=None):
        for x in struct.elements:
            for y in struct.elements:
                z_idx = fn(x, y)
                z = struct.elements[z_idx]


                xy = struct.pair(z)

                if name is not None:
                    struct.pairs[name].append(xy)
                else:
                    struct.pairs.append(xy)

                struct.model.Arrow(x.idx, xy.idx, ArrowType.inclusion)
                struct.model.Arrow(y.idx, xy.idx, ArrowType.inclusion)
                struct.model.Arrow(xy.idx, z.idx, ArrowType.inclusion)

                struct.model.Arrow(xy.idx, x.idx, ArrowType.restriction)
                struct.model.Arrow(xy.idx, y.idx, ArrowType.restriction)
                struct.model.Arrow(z.idx, xy.idx, ArrowType.restriction)
        return
    
    @staticmethod
    def build_levels(struct, fn):
        if isinstance(struct.pairs, dict):
            for xk, xv in struct.pairs.items():
                for yk, yv in struct.pairs.items():
                    for xp in xv:
                        for yp in yv:
                            if fn(xp, yp):
                                struct.model.Arrow(xp.idx, yp.idx, ArrowType.equivalence)
        
        if isinstance(struct.pairs, list):
            for xp in struct.pairs:
                for yp in struct.pairs:
                    if fn(xp, yp):
                        struct.model.Arrow(xp.idx, yp.idx, ArrowType.equivalence)
        return