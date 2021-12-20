from ...model import ArrowType, Model



class Shape(object):
    def __init__(self, model=None):
        self.model = model if model is not None else Model()
        return


    def cell(self, dimension : int):
        cell = self.model.object(dimension)
        self.model.arrow(cell.key, cell.key, ArrowType.equality)
        return cell

    def glue(self, a, b):
        self.model.arrow(a.key, b.key, ArrowType.inclusion)
        self.model.arrow(b.key, a.key, ArrowType.restriction)
        return

    def equate(self, a, b):
        self.model.arrow(a.key, b.key, ArrowType.equality)
        self.model.arrow(b.key, a.key, ArrowType.equality)
        return
    

    def __add__(self, other, data_update=None):
        result = Shape()

        # For every object in our model, copy it over.
        for obj in self.model.objects():
            result_data = data_update(obj.data) if data_update is not None else obj.data
            result.model.object(result_data)
        for obj in other.object():
            result_data = data_update(obj.data) if data_update is not None else obj.data
            result.model.object(result_data)

        # Copy the arrows, with offset for the second model.
        for arr in self.model.arrows():
            result.model.arrow(
                arr.start, 
                arr.end, 
                arr.data
            )
        for arr in other.arrows():
            result.model.arrow(
                arr.start + self.model.size, 
                arr.end + self.model.size, 
                arr.data
            )
        
        return result

    def __mul__(self, other):
        result = Shape()

        for obj in self.model.objects():
            # Add a copy shifted by that dimensionality for each cell.
            result.__add__(other, data_update=lambda x: x + obj.data)
        
        for arr in self.model.arrows():
            # Add an arrow between matched cells in end-blocks.
            d_start = arr.start * other.model.size
            d_end = arr.start * other.model.size
            for obj in other.model.objects():
                result.model.arrow(obj.key + d_start, obj.key + d_end, obj.data)

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
