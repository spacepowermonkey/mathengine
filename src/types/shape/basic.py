from ...model import ArrowType, Model



class Shape(object):
    def __init__(self, model=None):
        self.model = model if model is not None else Model()
        return


    def cell(self, dimension : int):
        cell = self.model.Obj(dimension)
        self.model.Arrow(cell.idx, cell.idx, ArrowType.equality)
        return cell

    def glue(self, a, b):
        self.model.Arrow(a.idx, b.idx, ArrowType.inclusion)
        self.model.Arrow(b.idx, a.idx, ArrowType.restriction)
        return

    def equate(self, a, b):
        self.model.Arrow(a.idx, b.idx, ArrowType.equality)
        self.model.Arrow(b.idx, a.idx, ArrowType.equality)
        return
    

    def __add__(self, other, data_update=None):
        result = Shape()

        # For every object in our model, copy it over.
        for obj in self.model.objects():
            result_data = data_update(obj.data) if data_update is not None else obj.data
            result.model.Obj(result_data)
        for obj in other.model.objects():
            result_data = data_update(obj.data) if data_update is not None else obj.data
            result.model.Obj(result_data)

        # Copy the arrows, with offset for the second model.
        for arr in self.model.arrows():
            result.model.Arrow(
                arr.start, 
                arr.end, 
                arr.data
            )
        for arr in other.model.arrows():
            result.model.Arrow(
                arr.start + self.model.size, 
                arr.end + self.model.size, 
                arr.data
            )
        
        return result

    def __mul__(self, other):
        result = Shape()

        for obj in self.model.objects():
            # Add a copy shifted by that dimensionality for each cell.
            result = result.__add__(other, data_update=lambda x: x + obj.data)
        
        for arr in self.model.arrows():
            # Add an arrow between matched cells in end-blocks.
            d_start = arr.start * other.model.size
            d_end = arr.end * other.model.size
            for obj in other.model.objects():
                result.model.Arrow(obj.idx + d_start, obj.idx + d_end, obj.data)

        return result

    def __pow__(self, n):
        result = Point()

        for n in range(n):
            result = self * result

        return result



class Point(Shape):
    def __init__(self):
        super().__init__()

        self.star = self.cell(0)
        return


class Interval(Shape):
    def __init__(self):
        super().__init__()

        self.start = self.cell(0)
        self.end = self.cell(0)
        self.middle = self.cell(1)

        self.glue(self.start, self.middle)
        self.glue(self.end, self.middle)
        return


class Loop(Shape):
    def __init__(self):
        super().__init__()

        self.start = self.cell(0)
        self.end = self.cell(0)
        self.middle = self.cell(1)

        self.glue(self.start, self.middle)
        self.glue(self.end, self.middle)

        self.equate(self.start, self.end)
        return
