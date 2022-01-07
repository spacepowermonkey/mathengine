from .basic import Interval, Shape



class Cube(Shape):
    def __init__(self, dimension):
        line = Interval()
        self = line ^ dimension
        return
